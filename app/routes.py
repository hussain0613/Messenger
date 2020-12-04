from flask import Blueprint
from .views import index, send_json, get_json, check

main = Blueprint('main', __name__)

main.route("/")(index)
main.route("/index/")(index)
main.route("/send_json/", methods = ["GET"])(send_json)
main.route("/get_json/", methods = ["POST"])(get_json)
main.route('/check/')(check)
