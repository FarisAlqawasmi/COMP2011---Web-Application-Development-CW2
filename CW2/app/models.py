from app import db
from flask_login import UserMixin


# User model to store user details
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    # One-to-one relationship with the Leaderboard table
    leaderboard = db.relationship(
        'Leaderboard', backref='user', uselist=False, cascade="all, delete"
    )

    # Many-to-many relationship with the Achievement table via
    # the UserAchievement table
    achievements = db.relationship(
        'UserAchievement', back_populates='user', cascade="all, delete"
    )


# Leaderboard model to track user scores
class Leaderboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, default=0)


# Achievement model to store details of each achievement
class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    points_required = db.Column(db.Integer, nullable=False)

    # Many-to-many relationship with users via the UserAchievement table
    users = db.relationship(
        'UserAchievement', back_populates='achievement', cascade="all, delete"
    )


# UserAchievement model to track user progress on achievements
class UserAchievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    achievement_id = db.Column(
        db.Integer, db.ForeignKey('achievement.id'), nullable=False
    )
    progress = db.Column(db.Integer, default=0)
    completed = db.Column(db.Boolean, default=False)

    # Relationships
    user = db.relationship('User', back_populates='achievements')
    achievement = db.relationship('Achievement', back_populates='users')

    # Helper method to update or create progress for an achievement
    @staticmethod
    def update_or_create(user_id, achievement_id, increment=1):
        """
        Update progress for an achievement or create it if it doesn't exist.
        """
        # Check if a UserAchievement entry exists
        # for the given user and achievement
        user_achievement = UserAchievement.query.filter_by(
            user_id=user_id, achievement_id=achievement_id
        ).first()

        if not user_achievement:
            # If no entry exists, create a new one
            user_achievement = UserAchievement(
                user_id=user_id,
                achievement_id=achievement_id,
                progress=increment
            )
            db.session.add(user_achievement)
        else:
            # If an entry exists, update progress and
            # check if the achievement is completed
            if not user_achievement.completed:
                user_achievement.progress += increment
                achievement = Achievement.query.get(achievement_id)
                if user_achievement.progress >= achievement.points_required:
                    user_achievement.completed = True
                    return f"Achievement Unlocked: {achievement.name}"

        db.session.commit()
        return None


# Function to seed the achievements table with predefined achievements
def seed_achievements():
    """
    Populate the achievements table with predefined achievements.
    This function ensures that achievements are created
    only if they don't already exist.
    """
    achievements = [
        {
            "name": "Reach 10 Points",
            "description": "Earn a total of 10 points.",
            "points_required": 10,
        },
        {
            "name": "Reach 100 Points",
            "description": "Earn a total of 100 points.",
            "points_required": 100,
        },
        {
            "name": "Reach 1000 Points",
            "description": "Earn a total of 1000 points.",
            "points_required": 1000,
        },
        {
            "name": "Make 10 Mistakes",
            "description": "Submit 10 incorrect answers.",
            "points_required": 10,
        },
        {
            "name": "Make 100 Mistakes",
            "description": "Submit 100 incorrect answers.",
            "points_required": 100,
        },
        {
            "name": "Make 1000 Mistakes",
            "description": "Submit 1000 incorrect answers.",
            "points_required": 1000,
        },
        {
            "name": "Get 10 Points in a Row",
            "description": (
                "Earn 10 points consecutively without making a mistake."
            ),
            "points_required": 10,
        },
        {
            "name": "Get 100 Points in a Row",
            "description": (
                "Earn 100 points consecutively without making a mistake."
            ),
            "points_required": 100,
        },
        {
            "name": "Get 1000 Points in a Row",
            "description": (
                "Earn 1000 points consecutively without making a mistake."
            ),
            "points_required": 1000,
        },
    ]

    for achievement_data in achievements:
        # Check if the achievement already exists
        existing_achievement = Achievement.query.filter_by(
            name=achievement_data["name"]
        ).first()
        if not existing_achievement:
            # Create a new achievement if it doesn't exist
            new_achievement = Achievement(
                name=achievement_data["name"],
                description=achievement_data["description"],
                points_required=achievement_data["points_required"],
            )
            db.session.add(new_achievement)
    db.session.commit()
