

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
    submit = SubmitField('Update Account')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Guide.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = Guide.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        'Password',
        validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password',
         validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
