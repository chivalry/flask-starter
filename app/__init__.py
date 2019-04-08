import click
from markdown import markdown
from flask import Flask
from flask_assets import Environment, Bundle
from app.db import db, alembic, user_repository
from app.auth import login_manager
from app.auth.views import auth
from app.homepage.views import homepage
from app.profile.views import profile


def create_app():
    #
    # Create app instance and load config
    app = Flask(__name__)
    app.config.from_json('../config.json')

    #
    # Initializse flask extensions
    db.init_app(app)
    alembic.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    assets = Environment(app)

    #
    # Register asset bundles
    css = Bundle('css/bootstrap.min.css', 'css/simplemde.min.css',
                 filters='cssmin', output='bundle.css')
    assets.register('css_all', css)
    js = Bundle('js/simplemde.min.js', filters='jsmin', output='bundle.js')
    assets.register('js_all', js)

    #
    # Custom jinja filters
    app.add_template_filter(lambda s: markdown(s), name='markdown')

    #
    # Register routes from blueprints
    app.register_blueprint(auth)
    app.register_blueprint(homepage)
    app.register_blueprint(profile, url_prefix='/profile')

    @app.cli.command('create-user')
    @click.option('-u', '--username', required=True)
    @click.option('-p', '--password', required=True)
    def create_user(username, password):
        user_repository.create(username, password)
        print('Created user {}'.format(username))

    #
    # GO!
    return app
