from flask_login import login_required

from flask import Flask, abort, request, send_from_directory, make_response, render_template, Blueprint
from pygments import highlight
from pygments.lexers import SqlLexer
from pygments.formatters import HtmlFormatter
from pygments.filters import NameHighlightFilter, KeywordCaseFilter
from pygments import token;
from threading import local
import apsw
from apsw import Error
from json import dumps, loads
from markupsafe import escape
from project.models import Messages, User
from . import db
from sqlalchemy import create_engine, select
engine = create_engine("sqlite:///instance/db.sqlite", echo=True, connect_args={'check_same_thread':False})

messaging = Blueprint('messaging', __name__)
tls = local()
#conn = apsw.Connection('instance/db.sqlite')
conn = engine.connect()

def pygmentize(text):
    if not hasattr(tls, 'formatter'):
        tls.formatter = HtmlFormatter(nowrap=True)
    if not hasattr(tls, 'lexer'):
        tls.lexer = SqlLexer()
        tls.lexer.add_filter(NameHighlightFilter(names=['GLOB'], tokentype=token.Keyword))
        tls.lexer.add_filter(NameHighlightFilter(names=['text'], tokentype=token.Name))
        tls.lexer.add_filter(KeywordCaseFilter(case='upper'))
    return f'<span class="highlight">{highlight(text, tls.lexer, tls.formatter)}</span>'



@messaging.get('/search')
def search(sql):
    result = sql
    try:
        c = conn.execute(sql)
        rows = c.fetchall()
        result = result + 'Result:\n'
        for row in rows:
            result = f'{result}    {dumps(row)}\n'
        c.close()
        return result
    except Error as e:
        return (f'{result}ERROR: {e}', 500)

#B';  DROP TABLE messages; --
def send(username, message, recipient, time):
    try:
        if not username or not message:
            return f'ERROR: missing sender or message'
        exists = db.session.query(User.username).filter_by(username=recipient).scalar() is not None
        if not exists:
            return f'ERROR: {recipient} user does not exist!'
        newMessage = Messages(sender=username, recipient = recipient, message=message);
        #stmt = ('INSERT INTO messages (sender, message) VALUES (?,?)',(sender, message))
        # ('INSERT INTO messages (sender, message, recipient, time) VALUES (?,?,?,?)',
        # (username, message, person, date_now))
        stmt = f"INSERT INTO messages (sender, recipient, message, time) values ('{username}','{recipient}' '{message}', '{time}')";

        result = f"Query: {pygmentize(stmt)}\n"
        db.session.add(newMessage)
        db.session.commit()
        return f'{result} ok'
    except Error as e:
        return f'ERROR: {e}'

