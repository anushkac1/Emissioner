from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from dotenv import load_dotenv
from fuzzywuzzy import fuzz
import json
#TESTING
from flask_jwt_extended import jwt_required


# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

# Configure Flask extensions
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] =  'your_secret_key'
print("SECRET_KEY:", os.getenv('SECRET_KEY'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv(
    'JWT_SECRET_KEY', 'your_jwt_secret_key')

# Initialize Flask extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Debug prints for environment variables
print("SECRET_KEY:", app.config['SECRET_KEY'])
print("JWT_SECRET_KEY:", app.config['JWT_SECRET_KEY'])

# Models


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Ensure this field exists


    def to_dict(self):
        return {
            'id': self.id,
            'caption': self.caption,
            'user_id': self.user_id,
            # 'created_at': self.created_at.isoformat(),
            'author_email': User.query.get(self.user_id).email
        }


# History
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Associate with the user
    food_item = db.Column(db.String(255), nullable=False)
    emission = db.Column(db.String(255), nullable=False)
    recommendations = db.Column(db.String(255), nullable=True)

    user = db.relationship('User', backref=db.backref('histories', lazy=True))  # Relationship with User

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

# Authentication Endpoints

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
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if User.query.filter_by(email=email).first():
            return jsonify({"message": "Email already registered"}), 400

        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Registration successful"}), 201
    except Exception as e:
        return jsonify({"message": "Registration failed", "error": str(e)}), 500

# @app.route('/login', methods=['POST'])
# def login():
#     try:
#         data = request.json
#         user = User.query.filter_by(email=data.get('email')).first()

#         if user and bcrypt.check_password_hash(user.password, data.get('password')):
#             access_token = create_access_token(identity=user.id)
#             return jsonify({
#                 "message": "Login successful",
#                 "token": access_token,
#                 "user_id": user.id,
#                 "email": user.email
#             }), 200
#         return jsonify({"message": "Invalid credentials"}), 401
#     except Exception as e:
#         return jsonify({"message": "Login failed", "error": str(e)}), 500


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        user = User.query.filter_by(email=data.get('email')).first()

        if user and bcrypt.check_password_hash(user.password, data.get('password')):
            access_token = create_access_token(
                identity=str(user.id))  # Convert user ID to string
            return jsonify({
                "message": "Login successful",
                "token": access_token,
                "user_id": user.id,
                "email": user.email
            }), 200
        return jsonify({"message": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"message": "Login failed", "error": str(e)}), 500

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
@jwt_required()
def create_post():
    try:
        # Debugging prints
        print("Token identity:", get_jwt_identity())
        print("Request payload:", request.json)

        current_user_id = get_jwt_identity()
        data = request.json
        caption = data.get('caption')

        if not caption:
            return jsonify({"message": "No caption provided"}), 400

        post = Post(caption=caption, user_id=current_user_id)
        db.session.add(post)
        db.session.commit()

        return jsonify(post.to_dict()), 201
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"message": "Internal server error", "error": str(e)}), 500


@app.route('/community-posts', methods=['GET'])
def get_posts():
    try:
        print("Fetching posts from the database...")
        posts = Post.query.order_by(Post.created_at.desc()).all()
        print(f"Fetched posts: {[post.to_dict() for post in posts]}")
        return jsonify([post.to_dict() for post in posts])
    except Exception as e:
        print(f"Error fetching posts: {str(e)}")  # Log the error
        return jsonify({"message": "Error fetching posts", "error": str(e)}), 500



@app.route('/community-post/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    try:
        current_user_id = get_jwt_identity()
        print("Token identity:", current_user_id)  # Debugging statement
        post = Post.query.get_or_404(post_id)
        print("Post User ID:", post.user_id)       # Debugging statement

        if post.user_id != int(current_user_id):
            return jsonify({"message": "Unauthorized"}), 403

        data = request.json
        post.caption = data.get('caption', post.caption)
        db.session.commit()
        return jsonify(post.to_dict()), 200
    except Exception as e:
        print(f"Error updating post: {str(e)}")
        return jsonify({"message": "Error updating post", "error": str(e)}), 500



@app.route('/community-post/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    try:
        current_user_id = get_jwt_identity()
        print("Token identity (delete):", current_user_id)  # Debugging

        post = Post.query.get_or_404(post_id)
        print("Post User ID:", post.user_id, type(post.user_id))  # Debugging
        print("Current User ID:", current_user_id, type(current_user_id))  # Debugging

        if post.user_id != int(current_user_id):
            print("Unauthorized attempt to delete post")  # Debugging
            return jsonify({"message": "Unauthorized"}), 403

        db.session.delete(post)
        db.session.commit()
        print("Post deleted successfully")  # Debugging
        return jsonify({"message": "Post deleted successfully"}), 200

    except Exception as e:
        print("Error deleting post:", str(e))
        return jsonify({"message": "Error deleting post", "error": str(e)}), 500



# Run the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4444, debug=True)
