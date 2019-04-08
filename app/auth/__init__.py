from flask_login import LoginManager
from app.db import user_repository

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return user_repository.find(user_id)
