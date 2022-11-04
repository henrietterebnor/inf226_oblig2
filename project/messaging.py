from flask_login import current_user

from flask import Blueprint
from threading import local
from apsw import Error
from project.models import Messages, User
from . import db
from sqlalchemy import create_engine

engine = create_engine("sqlite:///instance/db.sqlite", echo=True, connect_args={'check_same_thread':False})

messaging = Blueprint('messaging', __name__)
tls = local()
conn = engine.connect()


@messaging.get('/search')
def receive_all_messages():
    try:
        messages = Messages.query.filter_by(recipient=current_user.username)
        result = '---------- DISPLAYING INBOX ---------- \n'
        for message in messages:
            result += f'Message from : {message.sender} \n Content : {message.message} \n Sent at : {message.time} \n ---------------------------------------\n'
        if len(result)==0:
            result = 'No messages received'
        return result
    except Error as e:
        return 'ERROR : ' + e


@messaging.get('/search')
def receive_message(user_name):
    try:
        messages = Messages.query.filter_by(sender=user_name, recipient=current_user.username)
        result = '---- DISPLAYING MESSAGES FROM SINGLE USER ---- \n'
        for message in messages:
            result += f'Message from : {message.sender} \n Content : {message.message} \n Sent at : {message.time} \n ---------------------------------------\n'
        if len(result) == 0:
            result = 'No messages received from this user'
        return result
    except Error as e:
        return 'ERROR : ' + e

#
def send(username, message, recipient,time):
    try:
        if not username or not message:
            return f'ERROR: missing sender or message'
        exists = db.session.query(User.username).filter_by(username=recipient).scalar() is not None
        if not exists:
            return f'ERROR: {recipient} user does not exist!'
        newMessage = Messages(sender=username, recipient = recipient, message=message);
        db.session.add(newMessage)
        db.session.commit()
        result = '------- DISPLAYING MESSAGE SENT ------- \n'
        result += f'You sent a message to : {recipient} \n Content : {message} \n ---------------------------------------'
        return f'{result}'
    except Error as e:
        return f'ERROR: {e}'

