from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
import pandas as pd
import os
import google.generativeai as genai
from dotenv import load_dotenv
from fuzzywuzzy import fuzz
import json
from datetime import datetime

# Load environment variables from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the environment.")

# Initialize the Flask application
app = Flask(__name__)

# Allow requests from our specific frontend origins (our front end uses port 3000)
CORS(app, origins=["http://localhost:3000"])

# Configure the database and security settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Using an SQLite database
app.config['SECRET_KEY'] = 'your_secret_key'  # Secret key for app security with JWT tokens
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To Disable unnecessary warnings
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')  # Our JWT secret key, will change it to something more secure for production

# Initializing our Flask extensions for database, encryption, and authentication
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Configure the Gemini API with the provided key
genai.configure(api_key=GEMINI_API_KEY)

# Load training data for Gemini queries
with open('gemini/gemini_training_data.json', 'r') as f:
    training_data = json.load(f)
valid_inputs = [item['input'] for item in training_data]  # Extract valid inputs for fuzzy matching

# Helper function to find the best matching food item using fuzzy logic
def find_best_match(query):
    best_match = max(valid_inputs, key=lambda x: fuzz.ratio(x.lower(), query.lower()))
    similarity_score = fuzz.ratio(best_match.lower(), query.lower())
    return best_match if similarity_score > 70 else None

# Helper function to query Gemini API for carbon emissions data
def query_gemini_for_emission(food_item):
    prompt = f"""
    The user has entered the food item '{food_item}'.
    Provide only the carbon emissions value (in kg CO₂ per kilogram) for '{food_item}'.
    Respond in the format: "{food_item} emits approximately X kg CO₂ per kilogram."
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error with Gemini API: {str(e)}"

# Helper function to query Gemini API for eco-friendly alternatives
def query_gemini_for_alternatives(food_item):
    prompt = f"""
    The user has entered the food item '{food_item}'.
    Suggest three alternative food items that are more eco-friendly with lower emissions.
    Provide the alternatives as a numbered list.
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error with Gemini API: {str(e)}"

# Database logic: Defining the tables needed to store information for our application

# Defining the User model for storing user information
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique user ID
    email = db.Column(db.String(120), unique=True, nullable=False)  # User email
    password = db.Column(db.String(255), nullable=False)  # Encrypted password
    posts = db.relationship('Post', backref='author', lazy=True)  # Link to user's posts

# Defining the Post model for community posts
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique post ID
    caption = db.Column(db.String(255), nullable=False)  # Post caption
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Link to user
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of post creation

    # Convert post details to a dictionary for easy use in APIs
    def to_dict(self):
        return {
            'id': self.id,
            'caption': self.caption,
            'user_id': self.user_id,
            'author_email': User.query.get(self.user_id).email,
            'created_at': self.created_at.isoformat()
        }

# Defining the History model for tracking user activities
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique history entry ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Link to user
    food_item = db.Column(db.String(255), nullable=False)  # Food item name
    emission = db.Column(db.String(255), nullable=False)  # Emission data
    recommendations = db.Column(db.String(255), nullable=True)  # Eco-friendly alternatives

    # Relationship to access user details easily
    user = db.relationship('User', backref=db.backref('histories', lazy=True))

# Create the database tables
with app.app_context():
    db.create_all()

# Loading the emission data from a CSV file
data_path = 'backend/venv/data/greenhouse-gas-emissions-per-kilogram-of-food-product.csv'
emission_data = pd.read_csv(data_path)

# Backend Endpoint: Register a new user
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        # Check if the email is already registered
        if User.query.filter_by(email=email).first():
            return jsonify({"message": "Email already registered"}), 400

        # Encrypt the password and save the user
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Registration successful"}), 201
    except Exception as e:
        return jsonify({"message": "Registration failed", "error": str(e)}), 500

# Backend Endpoint: User login
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        user = User.query.filter_by(email=data.get('email')).first()

        # Verify email and password
        if user and bcrypt.check_password_hash(user.password, data.get('password')):
            access_token = create_access_token(identity=str(user.id))
            return jsonify({
                "message": "Login successful",
                "token": access_token,
                "user_id": user.id,
                "email": user.email
            }), 200
        return jsonify({"message": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"message": "Login failed", "error": str(e)}), 500


# Backend Endpoint to calculate and return emission data for an inputted food item
@app.route('/get-emission', methods=['POST'])
@jwt_required()  # To Ensure only authenticated users can access this endpoint
def get_emission():
    # Get the food item input from the request and clean it
    food_item = request.json.get('food', '').strip().lower()
    best_match = find_best_match(food_item)  # Find the closest match using fuzzy logic
    response = ""
    try:
        if best_match:
            # Get the emission data for the matched item from training data
            matched_output = next(
                (item['output'] for item in training_data if item['input'].lower() == best_match.lower()), None
            )
            # Fetch alternative recommendations for the food item
            alternatives = query_gemini_for_alternatives(food_item)
            # Prepare the response with emission and recommendations
            response = ({
                'food': food_item,
                'emission': matched_output,
                'recommendations': alternatives
            })
        else:
            # Get the emission data and alternatives from the external system
            emission = query_gemini_for_emission(food_item)
            alternatives = query_gemini_for_alternatives(food_item)
            # Prepare the response with emission and recommendations
            response = ({
                'food': food_item,
                'emission': emission,
                'recommendations': alternatives
            })
        # Get the user's ID from the JWT token
        user_id = get_jwt_identity()
        print("The resulting emission", response['emission'])

        # Save the history of the food item and emission to the database
        new_history_record = History(
            user_id=user_id,  # Link the record to the user
            food_item=food_item,
            emission=response['emission'],  # Convert emission to float if necessary
            recommendations=response['recommendations']
        )

        try:
            # Add the new history record to the database and save it
            db.session.add(new_history_record)
            db.session.commit()
            print(f"History entry added for user {user_id} with food item: {food_item}")
        except Exception as e:
            db.session.rollback()  # Undo database changes in case of an error
            print(f"Error saving history: {e}")
            return jsonify({"error": "Failed to save history record"}), 500

    except Exception as e:
        print("An error occurred:", str(e))

    # Return the response with emission data and recommendations!
    return jsonify(response)

# Helper function to find the best match for a food item using fuzzy matching
def find_best_match(query):
    # Compare the query with valid inputs and return the best match if similarity is high
    best_match = max(valid_inputs, key=lambda x: fuzz.ratio(x.lower(), query.lower()))
    similarity_score = fuzz.ratio(best_match.lower(), query.lower())
    return best_match if similarity_score > 70 else None

# Backend Endpoint to retrieve a user's history of food items and emissions
@app.route('/profile', methods=['GET'])
@jwt_required()  # Ensures the user is authenticated
def get_user_history():
    user_id = get_jwt_identity()  # Get the logged-in user's ID
    history_records = History.query.filter_by(user_id=user_id).all()  # Query the database for the specific user's history
    if not history_records:
        return jsonify({"message": "No history found."}), 404

    # Convert the history records into a list of dictionaries
    history_list = [
        {
            "food_item": record.food_item,
            "emission": record.emission,
            "recommendations": record.recommendations
        }
        for record in history_records
    ]

    # Return the user's history as JSON
    return jsonify(history_list), 200

# Backend Endpoint to create a community post
@app.route('/community-post', methods=['POST'])
@jwt_required()
def create_post():
    try:
        # Get the current user's ID and the request data
        current_user_id = get_jwt_identity()
        data = request.json
        caption = data.get('caption')

        # Ensure the caption was retreived successfully
        if not caption:
            return jsonify({"message": "No caption provided"}), 400

        # Create a new post and save it to the database
        post = Post(caption=caption, user_id=current_user_id)
        db.session.add(post)
        db.session.commit()

        # Return the created post as JSON
        return jsonify(post.to_dict()), 201
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"message": "Internal server error", "error": str(e)}), 500

# Backend Endpoint to fetch all community posts
@app.route('/community-posts', methods=['GET'])
def get_posts():
    try:
        # Fetch all posts from the database in descending order of creation time
        posts = Post.query.order_by(Post.created_at.desc()).all()
        return jsonify([post.to_dict() for post in posts])
    except Exception as e:
        print(f"Error fetching posts: {str(e)}")  # Log the error
        return jsonify({"message": "Error fetching posts", "error": str(e)}), 500

# Backend Endpoint to update a specific community post
@app.route('/community-post/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    try:
        # Get the current user's ID and the post to be updated
        current_user_id = get_jwt_identity()
        post = Post.query.get_or_404(post_id)

        # Ensure the user owns the post before updating
        if post.user_id != int(current_user_id):
            return jsonify({"message": "Unauthorized"}), 403

        # Update the post with new data
        data = request.json
        post.caption = data.get('caption', post.caption)
        db.session.commit()

        # Return the updated post as JSON
        return jsonify(post.to_dict()), 200
    except Exception as e:
        print(f"Error updating post: {str(e)}")
        return jsonify({"message": "Error updating post", "error": str(e)}), 500

# Backend Endpoint to delete a specific community post
@app.route('/community-post/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    try:
        # Get the current user's ID and the post to be deleted
        current_user_id = get_jwt_identity()
        post = Post.query.get_or_404(post_id)

        # Ensure the user owns the post before deleting
        if post.user_id != int(current_user_id):
            return jsonify({"message": "Unauthorized"}), 403

        # Delete the post from the database
        db.session.delete(post)
        db.session.commit()
        return jsonify({"message": "Post deleted successfully"}), 200
    except Exception as e:
        print("Error deleting post:", str(e))
        return jsonify({"message": "Error deleting post", "error": str(e)}), 500

# To Run the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4444, debug=True)  
