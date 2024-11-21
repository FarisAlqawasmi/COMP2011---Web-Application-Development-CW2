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
from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Retrieve the user by ID from the database

# Initialize migrations
migrate = Migrate(app, db)

# Import views and models to register routes and initialize models
from app import views, models