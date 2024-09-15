# app/routes/user_routes.py

from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.models.user import User, db
from app.services.user_service import get_all_users, create_user

user_routes = Blueprint('user_routes', __name__)

# Login Page
@user_routes.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        print(user)
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            
            # Redirect based on role
            if user.role == 'admin':
                return redirect(url_for('user_routes.users_page'))
            else:
                return redirect(url_for('event_routes.events_page'))
        else:
            flash('Login failed. Check email and password.', 'danger')
    
    return render_template('login.html', title='Login')


# Logout Route
@user_routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('user_routes.login_page'))


# Admin Create User Page (GET) - Requires login
# @user_routes.route('/admin/create_user_page', methods=['GET'])
# @login_required
# def create_user_page():
#     if current_user.role != 'admin':
#         return redirect(url_for('user_routes.user_dashboard'))
    
#     return render_template('admin.html', title='Create User')


# User Dashboard (GET) - Simple User Page after Login
@user_routes.route('/user/dashboard', methods=['GET'])
@login_required
def user_dashboard():
    return render_template('user_dashboard.html', title='User Dashboard')


# View all users (admin-only)
@user_routes.route('/admin/users_page', methods=['GET'])
@login_required
def users_page():
    if current_user.role != 'admin':
        return redirect(url_for('event_routes.events_page'))
    
    users = get_all_users()
    return render_template('users.html', title='All Users', users=users)

@user_routes.route('/admin/create_user', methods=['GET'])
@login_required
def create_user_page():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('event_routes.events_page'))
    
    return render_template('create_user.html', title='Create User')

# Admin route to handle user creation (POST)
@user_routes.route('/admin/create_user', methods=['POST'])
@login_required
def create_user_submit():
    if current_user.role != 'admin':
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('event_routes.events_page'))

    # Get form data
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')
    
    # Ensure that all fields are provided
    if not username or not email or not password or not role:
        flash('All fields are required.', 'danger')
        return redirect(url_for('user_routes.users_page'))  # Reload the form with error

    # Call the service layer to create the user
    try:
        user = create_user(username=username, email=email, password=password, role=role)
    except Exception as e:
        flash(f'Error creating user: {str(e)}', 'danger')
        return redirect(url_for('user_routes.users_page'))

    # Redirect based on success
    if user:
        flash('User created successfully!', 'success')
        return redirect(url_for('user_routes.users_page'))
    else:
        flash('Error creating user.', 'danger')
        return redirect(url_for('user_routes.users_page'))
