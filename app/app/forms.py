from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class NameForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField("Submit")
