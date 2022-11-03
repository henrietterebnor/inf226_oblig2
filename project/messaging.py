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
from project.models import Messages
from . import db

messaging = Blueprint('messaging', __name__)
tls = local()
inject = "'; insert into messages (sender,message) values ('foo', 'bar');select '"
conn = apsw.Connection('instance/db.sqlite')

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
def search(stmt):
    result = f"Query: {pygmentize(stmt)}\n"
    try:
        c = conn.execute(stmt)
        rows = c.fetchall()
        result = result + 'Result:\n'
        for row in rows:
            result = f'{result}    {dumps(row)}\n'
        c.close()
        return result
    except Error as e:
        return (f'{result}ERROR: {e}', 500)

def send(username, message, recipient, time):
    try:
        if not username or not message or not recipient or not time:
            return f'ERROR: missing sender or message'
        newMessage = Messages(sender=username, recipient = recipient, message=message);
        #stmt = ('INSERT INTO messages (sender, message) VALUES (?,?)',(sender, message))
       # ('INSERT INTO messages (sender, message, recipient, time) VALUES (?,?,?,?)',
        # (username, message, person, date_now))
        stmt = f"INSERT INTO messages (sender, recipient, message, time) values ('{username}', '{message}')";
        result = f"Query: {pygmentize(stmt)}\n"
        db.session.add(newMessage)
        db.session.commit()
        return f'{result} ok'
    except Error as e:
        return f'ERROR: {e}'

