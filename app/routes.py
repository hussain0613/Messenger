from flask import Blueprint
from .views import (index, room_view, create_room, delete_room, invite_members, invitations, accept_invitation, get_msg_json, send_msgs_json,
                check_room)

main = Blueprint('main', __name__)

main.route("/")(index)
main.route("/index/")(index)

main.route('/room/<int:room_id>/')(room_view)
main.route('/create_room/', methods = ['POST', 'GET'])(create_room)

main.route("/invite/<int:room_id>", methods = ['POST'])(invite_members)
main.route('/invitaions/')(invitations)
main.route('/accept_invitation/<int:invitation_id>/<decision>')(accept_invitation)

main.route('/get_msg/json/<int:room_id>', methods = ['POST'])(get_msg_json)
main.route('/send_msgs/json/<int:room_id>', methods = ['POST'])(send_msgs_json)
main.route('/check_room/json/<int:room_id>', methods = ['POST'])(check_room)

