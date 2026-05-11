from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SelectField,
    SubmitField,
    HiddenField
)
from wtforms.validators import DataRequired

ROWS = 12
COLUMNS = 4

class LoginForm(FlaskForm):

    username = StringField("Username", [DataRequired()])

    password = PasswordField("Password", [DataRequired()])
    
    submit = SubmitField("Login")

class ReservationForm(FlaskForm):

    first_name = StringField("First Name", [DataRequired()])

    last_name = StringField("Last Name", [DataRequired()])

    row = SelectField(
        "Choose a Row:",
        choices=[("", "Choose a Row")] + [(str(r), str(r + 1)) for r in range(ROWS)],
        validators=[DataRequired()],
    )

    column = SelectField(
        "Choose a Seat:",
        choices=[("", "Choose a Seat")] + [(str(c), str(c + 1)) for c in range(COLUMNS)],
        validators=[DataRequired()],
    )

    submit = SubmitField("Submit")

class DeleteForm(FlaskForm):

    submit = SubmitField("Delete")
