# app/scripts/create_admin.py

import sys
import os

# Add the parent directory (project root) to the system path
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from app import create_app  # Now the import should work
from app.models.user import db, User

app = create_app()

with app.app_context():
    # Check if the admin user already exists
    admin_user = User.query.filter_by(email='admin@example.com').first()
    
    if admin_user is None:
        # Create the admin user
        admin_user = User(
            username='admin',
            email='admin@example.com',
            role='admin'
        )
        admin_user.set_password('adminpassword')  # Use a strong password in production
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created successfully!")
    else:
        print("Admin user already exists.")
