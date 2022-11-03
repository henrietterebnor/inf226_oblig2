from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .messaging import send, search
from . import db

# Run this in terminal
# python3 -m venv auth
# source auth/bin/activate
# export FLASK_APP=project

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('login.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)


@main.route('/searchAndSend')
@login_required
def messaging():
    return render_template('sending.html')


@main.route('/messages', methods=['GET'])
@login_required
def search_message():
    query = request.args.get('q') or request.form.get('q') or '*'
    stmt = f"SELECT * FROM Messages WHERE message GLOB '{query}'"
    result = search(stmt)
    return result


@main.route('/messages/id', methods=['GET'])
@login_required
def search_single_message():
    query = request.args.get('q') or request.form.get('q') or '*'
    stmt = f"SELECT message FROM Messages WHERE id ='{query}'"
    result = search(stmt)
    return result


@main.route('/new', methods=['POST', 'GET'])
@login_required
def send_message():
    sender = request.args.get('sender') or request.form.get('sender')
    message = request.args.get('message') or request.args.get('message')
    query = send(sender, message)
    return query

