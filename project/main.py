from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db

# Run this in terminal
# python3 -m venv auth
# source auth/bin/activate
# export FLASK_APP=project

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)