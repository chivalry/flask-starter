from app.db import user_repository


def test_should_show_usage_help(app):
    runner = app.test_cli_runner()
    result = runner.invoke(args=['create-user'])
    assert 'Usage' in result.output


def test_should_create_user(app, client):
    username = 'foo'
    runner = app.test_cli_runner()
    result = runner.invoke(args=['create-user', '-u', username, '-p', 'bar'])
    assert 'Created' in result.output
    with app.app_context():
        user = user_repository.find_by(username=username)
    assert user.username == username
