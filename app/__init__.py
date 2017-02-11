# -*- coding: utf-8 -*-

from flask import Flask
# <<<<<<< HEAD
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from config import config
from flask_moment import Moment 



"""
config
 -- 'default': DevelopmentConfig
 -- 'develop': DevelopmentConfig
 -- 'testing': TestingConfig
 -- 'production': ProductionConfig
    you can edit this in config.py
"""
    


db = SQLAlchemy()
moment = Moment()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'



# admin site
# from admin import views


"""
blueprint
you can register a <blueprint> by run:
 -- mana blueprint <blueprint>
under app folder
""""""
from main import main
app.register_blueprint(main, url_prefix='/main')

from auth import auth
app.register_blueprint(auth, url_prefix="/auth")
"""
def create_app(config_name=None,main=True) : 
    if config_name is None :
        config_name = 'default'
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)
    db.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)


    from .api_1_0 import api  
    app.register_blueprint(api ,url_prefix='/api/v1.0')
    return app


app = create_app(config_name = 'default')


from . import views, forms
# >>>>>>> ec2645b42e8d0b874bf3ca3e57dd7dd3e98d9fb0
