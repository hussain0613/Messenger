from flask import Blueprint
from .. import db, mail, login

auth = Blueprint('auth', __name__, template_folder= 'templates', static_folder="app/statics")

from .routes import *
