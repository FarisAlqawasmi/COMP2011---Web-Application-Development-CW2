from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    # Relationship to Leaderboard
    leaderboard = db.relationship('Leaderboard', backref='user', uselist=False, cascade="all, delete")

    # Many-to-Many relationship with achievements
    achievements = db.relationship(
        'UserAchievement', back_populates='user', cascade="all, delete"
    )

class Leaderboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, default=0)

class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    points_required = db.Column(db.Integer, nullable=False)

    # Many-to-Many relationship with users
    users = db.relationship(
        'UserAchievement', back_populates='achievement', cascade="all, delete"
    )

class UserAchievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievement.id'), nullable=False)
    progress = db.Column(db.Integer, default=0)  # Track progress towards the achievement
    completed = db.Column(db.Boolean, default=False)

    # Relationships
    user = db.relationship('User', back_populates='achievements')
    achievement = db.relationship('Achievement', back_populates='users')

# Add a helper method to track achievement unlocking
    @staticmethod
    def update_or_create(user_id, achievement_id, increment=1):
        """
        Update progress for an achievement or create it if it doesn't exist.
        """
        user_achievement = UserAchievement.query.filter_by(
            user_id=user_id, achievement_id=achievement_id
        ).first()

        if not user_achievement:
            user_achievement = UserAchievement(
                user_id=user_id,
                achievement_id=achievement_id,
                progress=increment
            )
            db.session.add(user_achievement)
        else:
            if not user_achievement.completed:
                user_achievement.progress += increment
                achievement = Achievement.query.get(achievement_id)
                if user_achievement.progress >= achievement.points_required:
                    user_achievement.completed = True
                    return f"Achievement Unlocked: {achievement.name}"

        db.session.commit()
        return None