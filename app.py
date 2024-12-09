# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# import pandas as pd
# import os
# import google.generativeai as genai
# from dotenv import load_dotenv
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required
# from werkzeug.utils import secure_filename

# # Load environment variables from .env
# load_dotenv()

# GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# if not GEMINI_API_KEY:
#     raise ValueError("GEMINI_API_KEY is not set in the environment.")

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app, origins=["http://localhost:3000"])

# # Set up Flask extensions
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Initialize the extensions
# db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)
# jwt = JWTManager(app)

# # Set the upload folder for images and allowed extensions
# app.config['UPLOAD_FOLDER'] = 'uploads'
# app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# # Create the upload folder if it doesn't exist
# if not os.path.exists(app.config['UPLOAD_FOLDER']):
#     os.makedirs(app.config['UPLOAD_FOLDER'])

# # User model for SQLAlchemy
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(255), nullable=False)

# # Community Post model
# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     caption = db.Column(db.String(255), nullable=False)
#     image_path = db.Column(db.String(255), nullable=True)

# # Create the database tables (both users and posts)
# with app.app_context():
#     db.create_all()

# # Function to check if the file is allowed
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# # User login endpoint
# @app.route('/login', methods=['POST'])
# def login():
#     print("login being hit")
#     email = request.json.get('email')
#     password = request.json.get('password')

#     # Retrieve the user from the database
#     user = User.query.filter_by(email=email).first()
    
#     if user and bcrypt.check_password_hash(user.password, password):
#         access_token = create_access_token(identity=user.id)
#         return jsonify({"message": "Login successful", "token": access_token}), 200
#     else:
#         return jsonify({"message": "Invalid credentials"}), 401

# # Load the CSV file
# data_path = 'backend/venv/data/greenhouse-gas-emissions-per-kilogram-of-food-product.csv'
# emission_data = pd.read_csv(data_path)

# # Configure Gemini API
# genai.configure(api_key=GEMINI_API_KEY)

# # Function to get AI-generated emission estimates and suggestions
# def get_ai_emission_and_suggestions(food_item):
#     prompt = f"""
#     The user has entered the food item '{food_item}', but we don't have data on its carbon emissions.
#     1. Estimate the carbon emissions (in kg CO₂ per kilogram) for '{food_item}'.
#     2. Suggest three alternative food items that are more eco-friendly with lower emissions.
#     Provide the estimates and brief explanations for each alternative.
#     """

#     try:
#         model = genai.GenerativeModel('gemini-pro')
#         response = model.generate_content(prompt)
#         return response.text
#     except Exception as e:
#         return f"Error with Gemini API: {str(e)}"

# # Endpoint to get emissions for a specific food item
# @app.route('/get-emission', methods=['POST'])
# def get_emission():
#     food_item = request.json.get('food', '').strip().lower()

#     # Search for the food item in the CSV data
#     matching_data = emission_data[emission_data['Entity'].str.lower() == food_item]

#     if not matching_data.empty:
#         emission_value = matching_data.iloc[0]['GHG emissions per kilogram (Poore & Nemecek, 2018)']
#         response = {
#             'food': food_item,
#             'emission': emission_value,
#             'recommendations': None
#         }
#     else:
#         ai_response = get_ai_emission_and_suggestions(food_item)
#         response = {
#             'food': food_item,
#             'emission': 'Data not available in CSV',
#             'recommendations': ai_response
#         }

#     return jsonify(response)

# # Community Post Endpoints

# # Endpoint to create a post
# @app.route('/community-post', methods=['POST'])
# def create_post():
#     data = request.get_json()
#     caption = data.get('caption')
#     image_path = data.get('image_path')

#     if not caption:
#         return jsonify({"message": "No caption provided"}), 400

#     # Save the post in the database
#     post = Post(caption=caption, image_path=image_path)
#     db.session.add(post)
#     db.session.commit()

#     return jsonify({
#         "caption": caption,
#         "image_path": image_path
#     }), 201

# # Endpoint to fetch all posts
# @app.route('/community-posts', methods=['GET'])
# def get_posts():
#     posts = Post.query.all()
#     return jsonify([{'caption': post.caption, 'image_path': post.image_path} for post in posts])

# @app.route('/community-post/<int:post_id>', methods=['DELETE'])
# def delete_post(post_id):
#     post = Post.query.get(post_id)
    
#     if post:
#         db.session.delete(post)
#         db.session.commit()
#         return jsonify({"message": "Post deleted successfully"}), 200
#     else:
#         return jsonify({"message": "Post not found"}), 404

# # New endpoint for image upload
# @app.route('/upload-image', methods=['POST'])
# def upload_image():
#     if 'file' not in request.files:
#         return jsonify({"message": "No file part"}), 400
#     file = request.files['file']
    
#     if file.filename == '':
#         return jsonify({"message": "No selected file"}), 400
    
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(file_path)
        
#         # Optionally, you can save the file path to the database (e.g., Post model)
#         # For example, add the image_path to the Post model when creating a post.

#         return jsonify({"message": "File uploaded successfully", "file_url": f'/uploads/{filename}'}), 200

#     return jsonify({"message": "Invalid file format"}), 400

# # Serve uploaded files
# @app.route('/uploads/<filename>', methods=['GET'])
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# if __name__ == "__main__":
#     app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 4444)))
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
import google.generativeai as genai
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

# Load environment variables from .env
load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the environment.")


# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

# Set up Flask extensions
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# for authentication
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Using the same secret key as in auth.py
jwt = JWTManager(app)

# User model for SQLAlchemy
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Community Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(255), nullable=False)

# Create the database tables (both users and posts)
with app.app_context():
    db.create_all()

# User login endpoint
@app.route('/login', methods=['POST'])
def login():
    print("login being hit")
    email = request.json.get('email')
    password = request.json.get('password')

    # Retrieve the user from the database
    user = User.query.filter_by(email=email).first()
    
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({"message": "Login successful", "token": access_token}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


# Load the CSV file
data_path = 'backend/venv/data/greenhouse-gas-emissions-per-kilogram-of-food-product.csv'
emission_data = pd.read_csv(data_path)

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Function to get AI-generated emission estimates and suggestions
def get_ai_emission_and_suggestions(food_item):
    prompt = f"""
    The user has entered the food item '{food_item}', but we don't have data on its carbon emissions.
    1. Estimate the carbon emissions (in kg CO₂ per kilogram) for '{food_item}'.
    2. Suggest three alternative food items that are more eco-friendly with lower emissions.
    Provide the estimates and brief explanations for each alternative.
    """

    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error with Gemini API: {str(e)}"

# Endpoint to get emissions for a specific food item
@app.route('/get-emission', methods=['POST'])
def get_emission():
    # Get food item from request
    food_item = request.json.get('food', '').strip().lower()

    # Search for the food item in the CSV data
    matching_data = emission_data[emission_data['Entity'].str.lower() == food_item]

    if not matching_data.empty:
        # If found, get the emission value
        emission_value = matching_data.iloc[0]['GHG emissions per kilogram (Poore & Nemecek, 2018)']
        response = {
            'food': food_item,
            'emission': emission_value,
            'recommendations': None
        }
    else:
        # If not found, use the Gemini API to estimate emissions and suggest alternatives
        ai_response = get_ai_emission_and_suggestions(food_item)
        response = {
            'food': food_item,
            'emission': 'Data not available in CSV',
            'recommendations': ai_response
        }

    return jsonify(response)


# Community Post Endpoints

# Endpoint to create a post
@app.route('/community-post', methods=['POST'])
def create_post():
    data = request.get_json()
    caption = data.get('caption')

    if not caption:
        return jsonify({"message": "No caption provided"}), 400

    # Save the post in the database
    post = Post(caption=caption)
    db.session.add(post)
    db.session.commit()

    return jsonify({
        "caption": caption
    }), 201


# Endpoint to fetch all posts
@app.route('/community-posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([{'caption': post.caption} for post in posts])


if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 4444)))