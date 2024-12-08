# Class to test db connection and manually add stuff to db

from auth import app, db, bcrypt, User  # Import app, db, bcrypt, and User from auth.py

def populate_sample_users():
    # Ensure the app context is available for db operations
    with app.app_context():  # Use the app from auth.py
        # Create sample users
        sample_users = [
            {"email": "testuser1@example.com", "password": "password123"},
            {"email": "testuser2@example.com", "password": "password456"},
        ]

        for user_data in sample_users:
            # Hash the password before saving it
            hashed_password = bcrypt.generate_password_hash(user_data["password"]).decode('utf-8')
            # Create new User objects
            user = User(email=user_data["email"], password=hashed_password)
            # Add to the session and commit to the database
            db.session.add(user)
        
        # Commit changes to the database
        db.session.commit()
        print("Sample users added successfully.")

if __name__ == "__main__":
    populate_sample_users()
