from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length


class RegistrationForm(FlaskForm):
    """Form requested when registering new users."""

    name = StringField("Name", validators=[DataRequired(), Length(
        min=2, max=40, message="Name is too short! And cannot be over 40 characters long")])
    surname = StringField("Surname", validators=[DataRequired(), Length(
        min=2, max=40, message="Surname is too short! And cannot be over 40 characters long")])
    email = StringField("Email", validators=[DataRequired(), Length(
        min=10, max=50, message="Email is too short! And cannot be over 50 characters long")])
    password1 = PasswordField("Password", validators=[DataRequired(), EqualTo(
        "password2", message="Passwords Must Match"), Length(min=8, max=30)])
    password2 = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    """Form requested when users have to log in."""

    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

