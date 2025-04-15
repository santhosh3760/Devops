from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
import os

import logging
from logging.handlers import RotatingFileHandler


from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
# Config (set these as ENV VARS in production)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# Optional: Fail-fast if SECRET_KEY is not set
if not app.config['SECRET_KEY']:
    raise ValueError("No SECRET_KEY set for Flask application. Set it as an environment variable.")


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/signup')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.config['SESSION_COOKIE_SECURE'] = True  # Ensures cookies are only sent over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevents JavaScript from accessing cookies
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # Limits cookie sharing between sites

# Initialize extensions
db = SQLAlchemy(app)
csrf = CSRFProtect(app)

# Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Routes
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Basic validation
        if not username or not password:
            flash('Username and password are required')
            return render_template('signup.html')
            
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return render_template('signup.html')
        
        # Create new user with hashed password
        new_user = User(username=username)
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            print(f"User created with ID: {new_user.id}")
            flash('Account created successfully! Please log in.')
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}')
            return render_template('signup.html')
            
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash(f'Welcome {username}!')
            return redirect(url_for('dashboard'))
        
        flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in first')
        return redirect(url_for('home'))
        
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', username=user.username)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out')
    return redirect(url_for('home'))


# # Set up logging
# if not app.debug:
#     handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
#     handler.setLevel(logging.INFO)
#     app.logger.addHandler(handler)

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Server Error: {error}")
    return "Internal Server Error", 500

@app.errorhandler(404)
def not_found_error(error):
    app.logger.warning(f"404 Error: {error}")
    return "Page Not Found", 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
    
    