import bcrypt
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import ValidationError
from wtforms.validators import DataRequired
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from app.db import user_repository


class EditProfileForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    current_password = PasswordField('Current Password')
    new_password = PasswordField('New Password')
    photo = StringField('Photo URL')
    bio = TextAreaField('Bio')
    submit = SubmitField()

    def validate_username(self, username):
        if username.data != current_user.username:
            user = user_repository.find_by(username=username.data)
            if user:
                raise ValidationError('This username is already taken')

    def validate_current_password(self, current_password):
        if self.new_password.data and not bcrypt.checkpw(
                current_password.data.encode('utf-8'),
                current_user.password):
            raise ValidationError('Current password was empty or invalid')
