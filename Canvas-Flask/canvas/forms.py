from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, MacAddress, Optional

from canvas.models import User


class SearchForm(FlaskForm):
    search_filter = SelectField('Filter', choices=[("internal_user_id", "User"), ("offender_ip", "IP address"),
                                                   ("offender_mac", "MAC address"),
                                                   ("action", "Action"), ("date_posted", "Date"),
                                                   ("classification", "Classification"), ("case_id", "Case ID"),
                                                   ("offender_userid", "Offender Username")])
    search_input = StringField('Search for: ', validators=[DataRequired()])
    submit = SubmitField('Search')