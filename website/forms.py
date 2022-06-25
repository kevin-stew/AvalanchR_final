from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, InputRequired, EqualTo

class UserLoginForm(FlaskForm):
    # email, password, submit_button
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators= [InputRequired()])
    submit_button = SubmitField()

class UserSignupForm(FlaskForm):
    # email, password, submit_button
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators= [InputRequired(),EqualTo("confirm", message = 'Make sure...')])
    confirm = PasswordField('Repeat Password')
    submit_button = SubmitField()

class ObjectUploadForm(FlaskForm):
    title = StringField('Title', validators = [DataRequired()])
    description = StringField('Description', validators = [DataRequired()])
    price = StringField('Price', validators = [DataRequired()])
    dimensions = StringField('Dimensions', validators = [DataRequired()])
    weight = StringField('Weight', validators = [DataRequired()])
    img_url = StringField('Preview image', validators = [DataRequired()])  #reseach what this line needs to be to accept files
    model_url = StringField('3D model file', validators = [DataRequired()])
    submit_button = SubmitField()