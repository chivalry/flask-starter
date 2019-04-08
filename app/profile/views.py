from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.profile.forms import EditProfileForm
from app.auth.forms import LogoutForm
from app.db import user_repository

profile = Blueprint('profile', __name__)


@profile.route('/')
@login_required
def index():
    logout_form = LogoutForm()
    return render_template('profile/show.html', logout_form=logout_form,
                           page='profile')


@profile.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditProfileForm()
    logout_form = LogoutForm()
    if form.validate_on_submit():
        user_repository.update(current_user, form.username.data,
                               form.new_password.data, form.bio.data,
                               form.photo.data)
        return redirect(url_for('profile.index'))

    if not form.username.data:
        form.username.data = current_user.username
    form.photo.data = current_user.photo
    form.bio.data = current_user.bio
    return render_template('profile/edit.html', form=form,
                           logout_form=logout_form, page='profile')
