


class TravelForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[DataRequired()])
    content = TextAreaField(
        'Content',
        validators=[DataRequired()])
    submit = SubmitField('Submit')
