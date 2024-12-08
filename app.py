# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import pandas as pd
# import os

# app = Flask(__name__)
# CORS(app)

# #Load the CSV file
# data_path = 'backend/venv/data/greenhouse-gas-emissions-per-kilogram-of-food-product.csv'
# emission_data = pd.read_csv(data_path)

# #Endpoint to get emissions for a specific food item
# @app.route('/get_emission', methods=['POST'])
# def get_emission():
#     #Get food item from request
#     food_item = request.json.get('food', '').strip().lower()

#     #Search for the food item in the CSV data
#     matching_data = emission_data[emission_data['Entity'].str.lower() == food_item]

#     if not matching_data.empty:
#         #If found, get the emission value
#         emission_value = matching_data.iloc[0]['GHG emissions per kilogram (Poore & Nemecek, 2018)']
#         response = {
#             'food': food_item,
#             'emission': emission_value
#         }
#     else:
#         #If not found, return an error message
#         response = {
#             'error': f"No emission data found for '{food_item}'. Please check your input."
#         }

#     return jsonify(response)

# if __name__=="__main__":
#     app.run(host=os.getenv('IP', '0.0.0.0'),
#             port=int(os.getenv('PORT', 4444)))

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
# CORS(app)
CORS(app, origins=["http://localhost:3000"])

# Set up Flask extensions
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Change to your preferred database URI
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# for authentication
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Use the same secret key as in auth.py
jwt = JWTManager(app)

# User model for SQLAlchemy
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()


# User login endpoint
@app.route('/login', methods=['POST'])
# @app.route('/login', methods=['POST'])
def login():
    print("login being hit")
    email = request.json.get('email')
    password = request.json.get('password')

    # Retrieve the user from the database
    user = User.query.filter_by(email=email).first()
    
    if user:
        print(f"User found: {user.email}")  # Ensure the user is found
        print(f"Stored hashed password: {user.password}")  # Show the stored hashed password
        print(f"Input password: {password}")  # Show the input password for comparison

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({"message": "Login successful", "token": access_token}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401



# Load the CSV file
data_path = 'backend/venv/data/greenhouse-gas-emissions-per-kilogram-of-food-product.csv'
emission_data = pd.read_csv(data_path)

# Configure Gemini API
# Replace with your actual API key
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
# @jwt_required()
def get_emission():
    # Get food item from request
    food_item = request.json.get('food', '').strip().lower()

    # Search for the food item in the CSV data
    matching_data = emission_data[emission_data['Entity'].str.lower(
    ) == food_item]

    if not matching_data.empty:
        # If found, get the emission value
        emission_value = matching_data.iloc[0][
            'GHG emissions per kilogram (Poore & Nemecek, 2018)']
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


if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'),
            port=int(os.getenv('PORT', 4444)))
