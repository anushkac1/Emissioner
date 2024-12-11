# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required
# import os

# app = Flask(__name__)

# # # Set up Flask extensions
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Change to your preferred database URI
# # app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')
# # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # # Initialize the extensions
# # db = SQLAlchemy(app)
# # bcrypt = Bcrypt(app)
# # jwt = JWTManager(app)

# from flask_cors import CORS

# # CORS(app)
# CORS(app, origins=["http://localhost:3000"])

# # # User model for SQLAlchemy
# # class User(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     email = db.Column(db.String(120), unique=True, nullable=False)
# #     password = db.Column(db.String(255), nullable=False)

# # # Create the database tables
# # with app.app_context():
# #     db.create_all()


# # # User login endpoint
# # @app.route('/login', methods=['POST'])
# # # @app.route('/login', methods=['POST'])
# # def login():
# #     print("login being hit")
# #     email = request.json.get('email')
# #     password = request.json.get('password')

# #     # Retrieve the user from the database
# #     user = User.query.filter_by(email=email).first()
    
# #     if user:
# #         print(f"User found: {user.email}")  # Ensure the user is found
# #         print(f"Stored hashed password: {user.password}")  # Show the stored hashed password
# #         print(f"Input password: {password}")  # Show the input password for comparison

# #     if user and bcrypt.check_password_hash(user.password, password):
# #         access_token = create_access_token(identity=user.id)
# #         return jsonify({"message": "Login successful", "token": access_token}), 200
# #     else:
# #         return jsonify({"message": "Invalid credentials"}), 401


# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=4444)
