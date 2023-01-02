from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired, Length, Email, EqualTo
import peewee as pw


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class AddSongForm(FlaskForm):
    author = StringField('Author', validators=[DataRequired(), Length(min=2, max=20)])
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    song = FileField(validators=[FileRequired()])
    submit = SubmitField('Add')


class ShazamageForm(FlaskForm):
    song = FileField(validators=[FileRequired()])
    submit = SubmitField('Match')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


