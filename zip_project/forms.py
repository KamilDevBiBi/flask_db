from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = EmailField("Login / Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    repeat_pw = PasswordField("Repeat password", validators=[DataRequired()])
    surname = StringField("Surname")
    name = StringField("Name")
    age = IntegerField("Age")
    position = StringField("Position")
    speciality = StringField("Speciality")
    address = StringField("Address")
    submit = SubmitField("Submit")