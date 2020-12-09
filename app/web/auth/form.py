from flask_wtf import FlaskForm 
from wtforms import TextField, SubmitField, PasswordField
from wtforms.validators import Required

class LoginForm(FlaskForm):
    username = TextField('username', [Required()])
    password = PasswordField('password', [Required()])
