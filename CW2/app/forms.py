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
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class EditForm(FlaskForm):
    username = StringField("Username", validators=[
            DataRequired(), Length(min=3, max=20)]
    )
    email = StringField("Email", validators=[
            DataRequired(), Email()]
    )
    new_password = PasswordField("New Password", validators=[
            DataRequired()]
    )
    confirm_new_password = PasswordField(
        "Confirm New Password", validators=[
            DataRequired(),
            EqualTo("new_password", message="Passwords must match.")]
    )
    submit = SubmitField("Save Changes")


class SolveMathForm(FlaskForm):
    answer = StringField('Your Answer', validators=[DataRequired()])
    submit = SubmitField('Submit Answer')
