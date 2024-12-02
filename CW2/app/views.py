from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user, login_user, logout_user
from app import app, db
from app.models import Leaderboard, User, Achievement, UserAchievement
from app.forms import RegisterForm, LoginForm
from mathgenerator import genById
from sympy import sympify
from werkzeug.security import generate_password_hash, check_password_hash
import re
import random


# Your desired generator IDs
selected_generator_ids = [
    0, 1, 2, 3, 6, 8, 11, 12, 13, 28, 31
]


# Function to update achievements
def update_achievements(type, value):
    # Update user achievements based on the given type (score or mistakes).
    achievements = Achievement.query.all()
    unlocked_achievements = []
    for achievement in achievements:
        user_achievement = UserAchievement.query.filter_by(
            user_id=current_user.id, achievement_id=achievement.id
        ).first()

        if not user_achievement:
            user_achievement = UserAchievement(
                user_id=current_user.id,
                achievement_id=achievement.id,
                progress=0,
                completed=False
            )
            db.session.add(user_achievement)

        # Update progress and mark as completed if requirements are met
        if not user_achievement.completed:
            if type == "score" and "Points in a Row" in achievement.name:
                if value > 0:
                    user_achievement.progress += value
                else:
                    user_achievement.progress = 0
            elif type == "score" and "Points" in achievement.name:
                user_achievement.progress += value
                user_achievement.progress = max(0, user_achievement.progress)
            elif type == "mistakes" and "Mistakes" in achievement.name:
                user_achievement.progress += value
                user_achievement.progress = max(0, user_achievement.progress)

            # Mark the achievement as completed if the requirement is met
            if user_achievement.progress >= achievement.points_required:
                user_achievement.completed = True
                # Add the achievement to the list
                unlocked_achievements.append(achievement.name)

    db.session.commit()

    # Add notifications for unlocked achievements
    if "notifications" not in session:
        session["notifications"] = []
    session["notifications"].extend(unlocked_achievements)
    session.modified = True


@app.route("/")
def landing():
    # Landing page for unauthenticated users;
    # redirects logged-in users to the main index.
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    return render_template("landing.html")


@app.route("/index")
@login_required
def index():
    """
    Main route for generating and solving math problems.
    Displays the current problem and feedback from previous answers.
    """
    feedback = session.get('feedback')

    # Generate a new question only if feedback is absent
    if not feedback:
        problem_index = random.choice(selected_generator_ids)
        problem, solution = genById(problem_index)

        # Strip LaTeX markers ($) from the problem
        problem = problem.replace("$", "")

        # Store the problem and solution in the session for validation
        session['problem'] = problem
        session['solution'] = str(solution)

    return render_template(
        "index.html",
        username=current_user.username,
        problem=session['problem'],
        feedback=feedback,
        show_variable_note=(
            'x' in session['problem']
        ),
        show_fraction_note=(
            '/' in session['problem'] or '\\frac' in session['problem']
        ),
        current_score=(
            current_user.leaderboard.score
            if current_user.leaderboard else 0
        )
    )


@app.route("/check_answer", methods=["POST"])
@login_required
def check_answer():
    print("check_answer route was called")  # Debug
    user_answer = request.form.get("answer")
    correct_answer = session.get('solution')

    # Debug prints
    print(
        f"Raw User Answer: {user_answer}, "
        f"Raw Correct Answer: {correct_answer}"
    )

    if user_answer and correct_answer:
        try:
            # Preprocess the correct answer:
            # Use regex to convert \frac{a}{b} to a/b
            correct_answer = correct_answer.replace("$", "")
            correct_answer = re.sub(
                r"\\frac\{(.*?)\}\{(.*?)\}",
                r"(\1)/(\2)",
                correct_answer
            )
            print(f"Preprocessed Correct Answer: {correct_answer}")

            # Normalize answers
            user_answer_sympy = sympify(user_answer.strip())
            correct_answer_sympy = sympify(correct_answer.strip())

            # Compare as floats
            user_answer_float = float(user_answer_sympy)
            correct_answer_float = float(correct_answer_sympy)

            # Format for display
            user_answer_clean = f"{user_answer_float:.15g}"
            correct_answer_clean = f"{correct_answer_float:.15g}"

        except Exception as e:
            print(f"Error in parsing answer: {e}")
            session['feedback'] = {
                'status': 'error',
                'message': "Please enter a valid number as your answer."
            }
            # Ensure we stay in "Submit Answer" mode
            session['show_next'] = False

            # Deduct score and reset "Points in a Row" progress
            if current_user.leaderboard:
                current_user.leaderboard.score = max(
                    0, current_user.leaderboard.score - 1
                )
            update_achievements("score", 0)  # Reset "Points in a Row"
            update_achievements("mistakes", 1)  # Increment "mistakes" progress

            db.session.commit()  # Commit changes to the database
            return redirect(url_for("index"))

        # Check correctness
        # Ensure we stay in "Submit Answer" mode
        if abs(user_answer_float - correct_answer_float) < 1e-9:
            session['feedback'] = {
                'status': 'success',
                'message': "Correct! Well done.",
                'user_answer': user_answer_clean,
                'correct_answer': correct_answer_clean
            }
            # Enable "Next Question" button
            session['show_next'] = True

            # Update score for correct answer
            if current_user.leaderboard:
                current_user.leaderboard.score += 1
                update_achievements("score", 1)
            else:
                leaderboard_entry = Leaderboard(
                    user_id=current_user.id, score=1
                )
                db.session.add(leaderboard_entry)
                update_achievements("score", 1)

        else:
            session['feedback'] = {
                'status': 'error',
                'message': "Incorrect!",
                'user_answer': user_answer_clean,
                'correct_answer': correct_answer_clean
            }
            # Enable "Next Question" button even for incorrect answers
            session['show_next'] = True

            # Deduct score for incorrect answer
            if current_user.leaderboard:
                current_user.leaderboard.score = max(
                    0, current_user.leaderboard.score - 1
                )
                update_achievements("score", 0)  # Reset "Points in a Row"
            update_achievements("mistakes", 1)  # Increment "mistakes" progress

        # Commit changes to the database
        db.session.commit()
    else:
        session['feedback'] = {
            'status': 'error',
            'message': "Please submit an answer."
        }
        session['show_next'] = False  # Ensure we stay in "Submit Answer" mode

        # Deduct score for an invalid (empty) answer
        if current_user.leaderboard:
            current_user.leaderboard.score = max(
                0, current_user.leaderboard.score - 1
            )
        update_achievements("score", 0)  # Reset "Points in a Row"
        update_achievements("mistakes", 1)  # Increment "mistakes" progress

        # Commit changes to the database
        db.session.commit()

    return redirect(url_for("index"))


@app.route("/next_question", methods=["POST"])
@login_required
def next_question():
    # Generate a new random math problem
    problem_index = random.choice(selected_generator_ids)
    problem, solution = genById(problem_index)

    # Strip LaTeX markers ($) from the problem
    problem = problem.replace("$", "")

    # Store the new problem and solution in the session
    session['problem'] = problem
    session['solution'] = str(solution)

    # Clear feedback from the session
    session.pop('feedback', None)

    # Redirect to the index page with the new problem
    return redirect(url_for("index"))


@app.route("/leaderboard")
@login_required
def leaderboard():
    users = db.session.query(User.username, Leaderboard.score) \
                      .join(Leaderboard, User.id == Leaderboard.user_id) \
                      .order_by(Leaderboard.score.desc()) \
                      .all()
    return render_template("leaderboard.html", users=users)


@app.route("/achievements")
@login_required
def achievements():
    """
    Displays the user's achievements, their progress
    and the percentage unlocked.
    Links all predefined achievements to the user if not already linked.
    """
    all_achievements = Achievement.query.all()

    # Ensure each achievement is associated with the user
    # in the UserAchievement table
    for achievement in all_achievements:
        user_achievement = UserAchievement.query.filter_by(
            user_id=current_user.id, achievement_id=achievement.id
        ).first()
        if not user_achievement:
            # Add a new association with default progress if it doesn't exist
            user_achievement = UserAchievement(
                user_id=current_user.id,
                achievement_id=achievement.id,
                progress=0,
                completed=False
            )
            db.session.add(user_achievement)
    db.session.commit()

    # Query all user achievements and calculate statistics
    user_achievements = (
        db.session.query(Achievement, UserAchievement)
        .join(
            UserAchievement,
            Achievement.id == UserAchievement.achievement_id
        )
        .filter(
            UserAchievement.user_id == current_user.id
        )
        .all()
    )

    total_count = len(user_achievements)
    unlocked_count = sum(
        1 for _, user_achievement in user_achievements
        if user_achievement.completed
    )
    unlocked_percentage = (
        (unlocked_count / total_count * 100)
        if total_count > 0
        else 0
    )

    return render_template(
        "achievements.html",
        user_achievements=user_achievements,
        unlocked_count=unlocked_count,
        total_count=total_count,
        unlocked_percentage=unlocked_percentage
    )


@app.route("/seed_achievements")
def seed_achievements():
    """
    Seeds predefined achievements into the database
    if they do not already exist.
    Useful for initializing the system with default achievement data.
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

    # Iterate over each achievement and add to the database if missing
    for achievement_data in achievements:
        existing_achievement = Achievement.query.filter_by(
            name=achievement_data["name"]
        ).first()
        if not existing_achievement:
            new_achievement = Achievement(
                name=achievement_data["name"],
                description=achievement_data["description"],
                points_required=achievement_data["points_required"],
            )
            db.session.add(new_achievement)

    db.session.commit()
    return "Achievements seeded successfully!"


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Fetch the user by username
        user = User.query.filter_by(username=username).first()

        if user:
            # Verify the hashed password
            if check_password_hash(user.password, password):
                login_user(user)
                flash("Logged in successfully.", "success")
                return redirect(url_for("index"))
            else:
                flash(
                    "The password you entered is incorrect. "
                    "Please try again.",
                    "error"
                )
                return redirect(url_for("login"))
        else:
            flash(
                "The username entered is not found in our database. "
                "Perhaps you haven't registered?",
                "error"
            )
            return redirect(url_for("register"))

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    # Clear flash messages and notifications from the session
    session.pop('notifications', None)
    session.pop('_flashes', None)

    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("landing"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            confirm_password = form.confirm_password.data

            if password != confirm_password:
                flash("Passwords do not match.", "error")
                return redirect(url_for("register"))

            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash("Email already registered.", "error")
                return redirect(url_for("register"))

            try:
                # Use pbkdf2:sha256 as the hashing method
                hashed_password = generate_password_hash(
                    password, method="pbkdf2:sha256"
                )
                print("Generated hash:", hashed_password)  # Debugging line
                new_user = User(
                    username=username, email=email, password=hashed_password
                )
                db.session.add(new_user)
                db.session.commit()

                leaderboard_entry = Leaderboard(user_id=new_user.id, score=0)
                db.session.add(leaderboard_entry)
                db.session.commit()

                flash("Registration successful. Please log in.", "success")
                return redirect(url_for("login"))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {str(e)}", "error")
                return redirect(url_for("register"))

    return render_template("register.html", form=form)
