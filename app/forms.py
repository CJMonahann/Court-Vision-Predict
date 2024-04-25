from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class signUpForm(FlaskForm):
    user_name = StringField('Username', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired()])
    password = StringField('Password', validators = [DataRequired()])