import flask
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .messaging import send, receive_message, receive_all_messages
from sqlalchemy.sql import func


# Run this in terminal
# python3 -m venv auth
# source auth/bin/activate
# export FLASK_APP=project

main = Blueprint('main', __name__)
resp = flask.Response()
resp.headers['Content-Security-Policy'] = "default-src 'self'"


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
    return render_template('sending.html', name=current_user.username)


@main.route('/messages', methods=['GET'])
@login_required
def receive_message_from_user():
    user_name = request.args.get('q') or request.form.get('q')
    if user_name == '' or user_name == '*':
        result = receive_all_messages()
    else:
        result = receive_message(user_name)
    return result


@main.route('/new', methods=['POST', 'GET'])
@login_required
def send_message():
    sender = current_user.username
    message = request.args.get('message') or request.args.get('message')
    recipient = request.args.get('recipient') or request.form.get('recipient')
    time = func.now()
    query = send(sender, message, recipient, time)
    return query

