from app.db import db
from app.db.models import User


def find(user_id):
    return User.query.get(user_id)


def find_by(**kwargs):
    return User.query.filter_by(**kwargs).first()


def create(username, password, bio=None, photo=None):
    user = User(username=username, password=password, bio=bio, photo=photo)
    db.session.add(user)
    db.session.commit()
    return user


def update(user, username, password=None, bio=None, photo=None):
    user.username = username

    if password:
        user.password = password

    if bio:
        user.bio = bio

    if photo:
        user.photo = photo

    db.session.add(user)
    db.session.commit()
