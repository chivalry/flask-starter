from app.db import user_repository


def test_get_login_should_return_200(client):
    rv = client.get('/login')
    assert rv.status_code == 200


def test_post_login_without_data(client):
    rv = client.post('/login', data={})
    assert rv.status_code == 200


def test_post_login_should_return_200(client):
    rv = client.post('/login', data={'username': 'dude', 'password': 'edud'})
    assert rv.status_code == 200


def test_post_login_should_return_302(app, client):
    with app.app_context():
        user_repository.create('test', '1234')
    rv = client.post('/login', data={'username': 'test', 'password': '1234'})
    assert rv.status_code == 302
    assert rv.headers['Location'] == 'http://localhost/profile/'


def test_get_login_should_return_302(app, client):
    with app.app_context():
        user_repository.create('test', '1234')
    client.post('/login', data={'username': 'test', 'password': '1234'})
    rv = client.get('/login')
    assert rv.status_code == 302
    assert rv.headers['Location'] == 'http://localhost/profile/'


def test_get_logout_should_return_405(client):
    rv = client.get('/logout')
    assert rv.status_code == 405


def test_post_logout_should_return_302_login(app, client):
    with app.app_context():
        user_repository.create('test', '1234')
    client.post('/login', data={'username': 'test', 'password': '1234'})
    rv = client.post('/logout')
    assert rv.status_code == 302
    assert rv.headers['Location'] == 'http://localhost/login'
