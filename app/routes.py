from flask import Blueprint
from .views import index, send_json, get_json, check, room_view, create_room, delete_room, invite_members, invitations, accept_invitation, inroom_check

main = Blueprint('main', __name__)

main.route("/")(index)
main.route("/index/")(index)
main.route("/send_json/", methods = ["GET"])(send_json)
main.route("/get_json/", methods = ["POST"])(get_json)
main.route('/check/')(check)

main.route('/room/<int:room_id>/')(room_view)
main.route('/create_room/', methods = ['POST', 'GET'])(create_room)

main.route("/invite/", methods = ['POST'])(invite_members)
main.route('/invitaions/')(invitations)
main.route('/accept_invitation/<int:invitation_id>/<decision>')(accept_invitation)

main.route('/inroom_check/')(inroom_check)

