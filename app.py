from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
import pandas as pd
import os
import google.generativeai as genai
from dotenv import load_dotenv
from fuzzywuzzy import fuzz
import json
#TESTING
# from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the environment.")

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

# Configure Flask extensions
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  
app.config['SECRET_KEY'] =  'your_secret_key'
print("SECRET_KEY:", os.getenv('SECRET_KEY'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialize Flask extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Load training data for Gemini (optional)
with open('gemini/gemini_training_data.json', 'r') as f:
    training_data = json.load(f)

valid_inputs = [item['input'] for item in training_data]

# Helper function for fuzzy matching
def find_best_match(query):
    best_match = max(valid_inputs, key=lambda x: fuzz.ratio(x.lower(), query.lower()))
    similarity_score = fuzz.ratio(best_match.lower(), query.lower())
    return best_match if similarity_score > 70 else None

# Helper functions for querying Gemini
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

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(255), nullable=False)

# History
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Associate with the user
    food_item = db.Column(db.String(255), nullable=False)
    emission = db.Column(db.String(255), nullable=False)
    recommendations = db.Column(db.String(255), nullable=True)

    user = db.relationship('User', backref=db.backref('histories', lazy=True))  # Relationship with User

# Create database tables
with app.app_context():
    db.create_all()

# Load emission data
data_path = 'backend/venv/data/greenhouse-gas-emissions-per-kilogram-of-food-product.csv'
emission_data = pd.read_csv(data_path)

# # Authentication endpoints
# @app.route('/login', methods=['POST'])
# def login():
#     email = request.json.get('email')
#     password = request.json.get('password')
#     user = User.query.filter_by(email=email).first()
#     if user and bcrypt.check_password_hash(user.password, password):
#         access_token = create_access_token(identity=user.id)
#         return jsonify({"message": "Login successful", "token": access_token}), 200
#     else:
#         return jsonify({"message": "Invalid credentials"}), 401

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=str(user.id))  # Convert user ID to string
        print(f"Generated token for user {user.id}: {access_token}")  # Debugging
        return jsonify({"message": "Login successful", "token": access_token}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


#TESTING
# Endpoint to register a new user
@app.route('/register', methods=['POST'])
def register():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    # Check if the email already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "User already exists"}), 409

    # Hash the password and save the user
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# Endpoint to delete a user
@app.route('/delete-user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    # Retrieve the user from the database
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    # Delete the user
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": f"User with ID {user_id} has been deleted successfully"}), 200




# Endpoint to get emission data
@app.route('/get-emission', methods=['POST'])
@jwt_required()  # Ensure the user is authenticated
def get_emission():
    food_item = request.json.get('food', '').strip().lower()
    best_match = find_best_match(food_item)
    response = ""
    try:
        if best_match:
            matched_output = next(
                (item['output'] for item in training_data if item['input'].lower() == best_match.lower()), None
            )
            alternatives = query_gemini_for_alternatives(food_item)
            response = ({
                'food': food_item,
                'emission': matched_output,
                'recommendations': alternatives
            })
        else:
            emission = query_gemini_for_emission(food_item)
            alternatives = query_gemini_for_alternatives(food_item)
            response = ({
                'food': food_item,
                'emission': emission,
                'recommendations': alternatives
            })
        user_id = get_jwt_identity()
        print("The resulting emission", response['emission'])
        # Insert the food item and emission data into the History table
        new_history_record = History(
            user_id=user_id,  # Link the history to the current user
            food_item=food_item,
            emission=response['emission'],  # Ensure emission is a float
            # emission = emission,
            recommendations=response['recommendations']
        )

        try:
            # Add the new record to the session and commit it to the database
            db.session.add(new_history_record)
            db.session.commit()
            print(f"History entry added for user {user_id} with food item: {food_item}")
        except Exception as e:
            db.session.rollback()  # Rollback in case of an error
            print(f"Error saving history: {e}")
            return jsonify({"error": "Failed to save history record"}), 500

    except Exception as e:
        print("stuff is going wrong")

    # Get user ID from the JWT token
    
    return jsonify(response)

# # Endpoint to get emissions for a specific food item
# @app.route('/get-emission', methods=['POST'])
# @jwt_required()  # Ensure the user is authenticated
# def get_emission():
#     # Get food item from request
#     food_item = request.json.get('food', '').strip().lower()

#     # Search for the food item in the CSV data
#     matching_data = emission_data[emission_data['Entity'].str.lower() == food_item]

#     if not matching_data.empty:
#         # If found, get the emission value
#         emission_value = matching_data.iloc[0]['GHG emissions per kilogram (Poore & Nemecek, 2018)']
#         response = {
#             'food': food_item,
#             'emission': emission_value,
#             'recommendations': None
#         }
#     else:
#         # If not found, use the Gemini API to estimate emissions and suggest alternatives
#         ai_response = get_ai_emission_and_suggestions(food_item)
#         response = {
#             'food': food_item,
#             'emission': 'Data not available in CSV',
#             'recommendations': ai_response
#         }

#     # Get user ID from the JWT token
#     user_id = get_jwt_identity()

#     # Insert the food item and emission data into the History table
#     new_history_record = History(
#         user_id=user_id,  # Link the history to the current user
#         food_item=food_item,
#         emission=float(response['emission']) if isinstance(response['emission'], (int, float)) else 0.0,  # Ensure emission is a float
#         recommendations=response['recommendations']
#     )

#     try:
#         # Add the new record to the session and commit it to the database
#         db.session.add(new_history_record)
#         db.session.commit()
#         print(f"History entry added for user {user_id} with food item: {food_item}")
#     except Exception as e:
#         db.session.rollback()  # Rollback in case of an error
#         print(f"Error saving history: {e}")
#         return jsonify({"error": "Failed to save history record"}), 500

#     return jsonify(response)




@app.route('/profile', methods=['GET'])
@jwt_required()  # Protect the route, ensuring the user is authenticated
def get_user_history():
    user_id = get_jwt_identity()  # Get the logged-in user's ID from the JWT token
    history_records = History.query.filter_by(user_id=user_id).all()  # Query user's history
    if not history_records:
        return jsonify({"message": "No history found."}), 404

    history_list = [
        {
            "food_item": record.food_item,
            "emission": record.emission,
            "recommendations": record.recommendations
        }
        for record in history_records
    ]

    return jsonify(history_list), 200


    
# Endpoint for community posts
@app.route('/community-post', methods=['POST'])
def create_post():
    caption = request.json.get('caption')
    if not caption:
        return jsonify({"message": "No caption provided"}), 400
    post = Post(caption=caption)
    db.session.add(post)
    db.session.commit()
    return jsonify({"caption": caption}), 201

@app.route('/community-posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([{'caption': post.caption} for post in posts])

# Validate query endpoint
@app.route('/validate_query', methods=['POST'])
def validate_query():
    query = request.json.get('query', '').strip().lower()
    best_match = find_best_match(query)
    if best_match:
        return jsonify({'valid': True, 'best_match': best_match})
    else:
        return jsonify({'valid': False, 'message': "Invalid query."}), 400

# Run the app
if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 4444)))
