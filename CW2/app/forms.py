from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


# Form for user registration
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
            DataRequired(), Length(min=3, max=20)]
    )
    email = StringField('Email', validators=[
            DataRequired(), Email()]
    )
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=6)]
    )
    confirm_password = PasswordField('Confirm Password', validators=[
            DataRequired(),
            EqualTo('password', message="Passwords must match.")]
    )
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class SolveMathForm(FlaskForm):
    answer = StringField('Your Answer', validators=[DataRequired()])
    submit = SubmitField('Submit Answer')
