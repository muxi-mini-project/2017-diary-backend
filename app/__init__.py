# coding: utf-8

from flask import Flask
<<<<<<< HEAD
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from config import config


app = Flask(__name__)
"""
config
 -- 'default': DevelopmentConfig
 -- 'develop': DevelopmentConfig
 -- 'testing': TestingConfig
 -- 'production': ProductionConfig
    you can edit this in config.py
"""
config_name = 'default'
app.config.from_object(config[config_name])
config[config_name].init_app(app)
toolbar = DebugToolbarExtension(app)


db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


# admin site
from admin import views


"""
blueprint
you can register a <blueprint> by run:
 -- mana blueprint <blueprint>
under app folder
"""
from main import main
app.register_blueprint(main, url_prefix='/main')

from auth import auth
app.register_blueprint(auth, url_prefix="/auth")

=======


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key is here'


from . import views, forms
>>>>>>> ec2645b42e8d0b874bf3ca3e57dd7dd3e98d9fb0
