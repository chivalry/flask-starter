from flask import Blueprint, render_template
from app.auth.forms import LogoutForm

homepage = Blueprint('homepage', __name__)


@homepage.route('/')
def index():
    logout_form = LogoutForm()
    return render_template('homepage/index.html', logout_form=logout_form,
                           page='home')


@homepage.route('/about')
def about():
    logout_form = LogoutForm()
    return render_template('homepage/about.html', logout_form=logout_form,
                           page='about')
