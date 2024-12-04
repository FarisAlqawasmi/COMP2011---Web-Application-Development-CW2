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

# Enforce strong session protection
login_manager.session_protection = "strong"  # Use "strong" session protection


# Define the user loader callback
@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))


# Initialize migrations
migrate = Migrate(app, db)

from app import views, models # noqa


# Define a global flag to track if seeding is done
database_seeded = False


# Seed achievements after `flask db upgrade` automatically
@app.before_request
def seed_database():
    """Seed the achievements table if not already populated."""
    global database_seeded  # Access the global flag
    if not database_seeded:
        from app.models import seed_achievements
        seed_achievements()
        database_seeded = True  # Mark the seeding as done
