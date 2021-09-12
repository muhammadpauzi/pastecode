from flask import Blueprint, request, flash, render_template, redirect, url_for
from flask_login.utils import login_required
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, current_user, logout_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    errors = {}
    isError = False
    username = ''
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        
        if len(username) < 1:
            errors['username'] = "Username must be required."
            isError = True
        if len(password) < 1:
            errors['password'] = "Password must be required."
            isError = True
        
        if isError == False:
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Login failed, try again!', category='error')

    return render_template('login.html', errors=errors, username=username, user=current_user)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    errors = {}
    isError = False
    username = ''
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        
        user = User.query.filter_by(username=username).first()

        if user:
            errors['username'] = "Username already registered."
            isError = True
        if len(username) < 1:
            errors['username'] = "Username must be required."
            isError = True
        if len(password) < 1:
            errors['password'] = "Password must be required."
            isError = True
        
        if isError == False:
            new_user = User(username=username, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('register.html', errors=errors, username=username, user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', category='success')
    return redirect(url_for('auth.login'))