# app/services/user_service.py

from app.models.user import User, db
from flask import flash


def create_user(username, email, password, role='user'):
    """Create a new user and add them to the database."""
    existing_user = User.query.filter_by(email=email).first()
    
    if existing_user:
        flash('A user with this email already exists.', 'danger')
        return None
    
    new_user = User(username=username, email=email, role=role)
    new_user.set_password(password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        flash(f'User {username} created successfully!', 'success')
        return new_user
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        flash('Error creating user.', 'danger')
        print(f"Error: {e}")
        return None

def get_all_users():
    return User.query.all()
