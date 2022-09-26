
from wtforms import StringField, SelectField, EmailField
from flask_wtf import FlaskForm
from wtforms.fields import EmailField
from wtforms.validators import Email


class UserForm(FlaskForm):
    telegram_id = StringField('Telegram id')
    username = StringField('Username')
    first_name = StringField('First name')
    phone_number = StringField('Phone number')
    email = EmailField('Email', validators=[Email('Incorrect email ')])
    user_city = StringField('City')
    is_blocked = SelectField('Is blocked', choices=[('True', 'Blocked'), ('False', 'Not blocked')], default=False)

