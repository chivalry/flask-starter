import pytest
from app import create_app
from app.db import alembic


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    yield app


@pytest.fixture
def client(app):
    with app.app_context():
        alembic.upgrade('head')
    client = app.test_client()
    yield client
