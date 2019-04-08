from app.db import user_repository


def test_get_index_should_return_302(client):
    rv = client.get('/profile/')
    assert rv.status_code == 302
    assert rv.headers['Location'] == \
        'http://localhost/login?next=%2Fprofile%2F'


def test_get_index_should_return_200(app, client):
    with app.app_context():
        user_repository.create('dude', '1234')
    client.post('/login', data={'username': 'dude', 'password': '1234'})

    rv = client.get('/profile/')
    assert rv.status_code == 200


def test_get_edit_should_return_302(client):
    rv = client.get('/profile/edit')
    assert rv.status_code == 302
    assert rv.headers['Location'] == \
        'http://localhost/login?next=%2Fprofile%2Fedit'


def test_get_edit_shoud_return_200(app, client):
    with app.app_context():
        user_repository.create('dude', '1234')
    client.post('/login', data={'username': 'dude', 'password': '1234'})

    rv = client.get('/profile/edit')
    assert rv.status_code == 200


def test_should_not_update_username(app, client):
    with app.app_context():
        id = user_repository.create('dude', '1234').id
        user_repository.create('foo', 'bar')
    client.post('/login', data={'username': 'dude', 'password': '1234'})

    rv = client.post('/profile/edit', data={'username': 'foo'})
    assert rv.status_code == 200
    with app.app_context():
        user = user_repository.find(id)
    assert user.username == 'dude'


def test_should_update_username(app, client):
    with app.app_context():
        id = user_repository.create('dude', '1234').id
    client.post('/login', data={'username': 'dude', 'password': '1234'})

    rv = client.post('/profile/edit', data={'username': 'woa'})
    assert rv.status_code == 302
    assert rv.headers['Location'] == 'http://localhost/profile/'
    with app.app_context():
        user = user_repository.find(id)
    assert user.username == 'woa'


def test_should_not_update_password(app, client):
    with app.app_context():
        u = user_repository.create('dude', '1234')
        old_password_hash = u.password
    client.post('/login', data={'username': 'dude', 'password': '1234'})

    rv = client.post(
        '/profile/edit', data={'username': 'dude', 'new_password': '4321'})
    assert rv.status_code == 200
    with app.app_context():
        user = user_repository.find(u.id)
        assert user.password == old_password_hash


def test_should_update_password(app, client):
    with app.app_context():
        u = user_repository.create('dude', '1234')
        old_password_hash = u.password
    client.post('/login', data={'username': 'dude', 'password': '1234'})

    rv = client.post('/profile/edit', data={
        'username': 'dude', 'current_password': '1234', 'new_password': '4321'
    })
    assert rv.status_code == 302
    with app.app_context():
        user = user_repository.find(u.id)
        assert user.password != old_password_hash


def test_should_update_bio_and_photo(app, client):
    with app.app_context():
        u = user_repository.create('dude', '1234')
        old_bio = u.bio
        old_photo = u.photo
    client.post('/login', data={'username': 'dude', 'password': '1234'})

    rv = client.post('/profile/edit', data={
        'username': 'dude', 'bio': 'LOL', 'photo': 'http://'
    })
    assert rv.status_code == 302
    with app.app_context():
        user = user_repository.find(u.id)
        assert user.bio != old_bio
        assert user.photo != old_photo


def test_should_show_profile_after_update(app, client):
    with app.app_context():
        user_repository.create('dude', '1234')
    client.post('/login', data={'username': 'dude', 'password': '1234'})
    client.post('/profile/edit', data={'username': 'dude', 'bio': '# Welcome'})

    rv = client.get('/profile/')
    assert rv.status_code == 200
