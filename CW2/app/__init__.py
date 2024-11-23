from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = None  # Initialize the variable for migrations

# Create the Flask app instance
app = Flask(__name__)
app.config.from_object('config')

# Initialize extensions with the app
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

# Define the user loader callback
from app.models import User, seed_achievements

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Retrieve the user by ID from the database

# Initialize migrations
migrate = Migrate(app, db)

# Import models and views to register routes and models
from app import views, models

# Seed achievements when the app starts
with app.app_context():
    seed_achievements()