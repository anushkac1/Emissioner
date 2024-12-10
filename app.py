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
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')

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

# Create database tables
with app.app_context():
    db.create_all()

# Load emission data
data_path = 'backend/venv/data/greenhouse-gas-emissions-per-kilogram-of-food-product.csv'
emission_data = pd.read_csv(data_path)

# Authentication endpoints
@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({"message": "Login successful", "token": access_token}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# Endpoint to get emission data
@app.route('/get-emission', methods=['POST'])
def get_emission():
    food_item = request.json.get('food', '').strip().lower()
    best_match = find_best_match(food_item)

    if best_match:
        matched_output = next(
            (item['output'] for item in training_data if item['input'].lower() == best_match.lower()), None
        )
        alternatives = query_gemini_for_alternatives(food_item)
        return jsonify({
            'food': food_item,
            'emission': matched_output,
            'recommendations': alternatives
        })
    else:
        emission = query_gemini_for_emission(food_item)
        alternatives = query_gemini_for_alternatives(food_item)
        return jsonify({
            'food': food_item,
            'emission': emission,
            'recommendations': alternatives
        })

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
