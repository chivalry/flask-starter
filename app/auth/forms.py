import bcrypt
from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from app.db import user_repository


class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField()

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        user = user_repository.find_by(username=self.username.data)
        if not user or not bcrypt.checkpw(self.password.data.encode('utf-8'),
                                          user.password):
            flash('Invalid username or password', category='error')
            return False

        self.user = user
        return True


class LogoutForm(FlaskForm):
    submit = SubmitField()
