Flask-Starter
=============

My personal starter app for creating new flask apps.

Requirements
------------

* **pipenv** is used for venv management
* **python 3.7**

What's Included?
----------------

* ORM (Flask-SQLAlchemy)
* Database migrations (Flask-Alembic)
* Authentication (Flask-Login)
* Asset management (Flask-Assets)
* Form validation (Flask-WTF)

Getting Started
---------------

1. 
    Copy the example config to real config and edit as needed

    `cp config.json.example config.json`

2.
    Install dependencies

    `pipenv sync --dev`

    (You can remove `--dev` if you don't want to install dev dependencies)

3.
    Create a database

    `pipenv run flask db upgrade`

4.
    Create a user

    `pipenv run flask create-user -u <username> -p <password>`

5.
    Run the flask development server

    `pipenv run flask run`
