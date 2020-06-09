from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, DateField, TextAreaField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from .models import Guide


class RegistrationForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[DataRequired(), Length(min=3, max=20)])
    surname = StringField(
        'Surname',
        validators=[DataRequired(), Length(min=3, max=20)])
    phone = StringField(
        'Phone',
        validators=[DataRequired(), Length(min=9, max=15)])
    email = StringField(
        'Email',
        validators=[DataRequired()])
    password = PasswordField(
        'Password',
        validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = Guide.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password',
        validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class GuideForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[DataRequired(), Length(min=3, max=20)])
    surname = StringField(
        'Surname',
        validators=[DataRequired(), Length(min=3, max=20)])
    phone = StringField(
        'Phone',
        validators=[DataRequired(), Length(min=9, max=15)])
    email = StringField(
        'Email',
        validators=[DataRequired()])
    image_file = StringField(
        'image_file')
    picture = FileField(
        'Update Profile Picture',
        validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Guide.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class TravelForm(FlaskForm):
    guide_id = StringField(
        'Guide ID',
        validators=[DataRequired()])
    title = StringField(
        'Title',
        validators=[DataRequired()])
    content = TextAreaField(
        'Content',
        validators=[DataRequired()])
    submit = SubmitField('Create')
