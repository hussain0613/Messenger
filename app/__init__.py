from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData

import os
from dotenv import load_dotenv

from .utils import naming_convention

BASEDIR = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(BASEDIR, '.env'))

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))

migrate = Migrate(render_as_batch = True) ## render_as_batch dorkar karon sqlite does not support alter table

login = LoginManager()
login.login_view = 'auth.login'
login.login_message_category = 'alert alert-warning'
mail = Mail()

def create_app(config_class= None):
    app = Flask(__name__, template_folder='templates', static_folder="statics")
    
    ## Configurations 
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT') or 587)
    app.config['MAIL_USE_TLS'] = int(os.getenv('MAIL_USE_TLS') or 1)
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

    
    db.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    
    from .auth import auth
    #from .database import database
    from .routes import main

    app.register_blueprint(main)
    app.register_blueprint(auth)#, url_prefix="/auth")
    #app.register_blueprint(database)

    return app
