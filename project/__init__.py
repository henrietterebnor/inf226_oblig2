from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)

    #made with import os, os.urandom(24)
    app.config['SECRET_KEY'] = b'\x8d\x07Q\x06\x8a8\x9f\x0c"\xc4\xca`\xc9\xe0\xec\xe3\x92v"4c\xa0,/'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SESSION_COOKIE_SECURE'] = True

    db.init_app(app)
    csrf.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.session_protection = "strong"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    from . import models  # don't know if we need this import :))

    with app.app_context():
        db.create_all()

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
