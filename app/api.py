from flask import request, request, Response, url_for
from flask_login import current_user, login_required

from . import db
from .auth.models import User
from .models import Message, Room, Invitation, P2RConnection, Receivers
from .utils import room_membership_required

import json

@login_required
def index_api():
    json_data = {}
    json_data["Status"] = "Success"
    json_data["Message"] = "Index page"
    json_data["name"] = current_user.name
    json_data["uname"] = current_user.username

    json_data["rooms"] = {}
    for room in current_user.rooms:
        json_data["rooms"][room.roomname] = url_for("main.room_view", room_id = room.id)
    resp = Response(json.dumps(json_data))
    resp.content_type = "application/json"
    
    
    return resp

@room_membership_required()
@login_required
def room_api(room_id):

    room = Room.query.get(room_id)
    p2rconn = P2RConnection.query.filter(and_(P2RConnection.user_id == current_user.id, P2RConnection.room_id == room_id)).first() ## to check if the user is admin in this room

    json_data = {}
    json_data["Status"] = "Success"
    json_data["Message"] = "Index page"
    json_data["name"] = current_user.name
    json_data["uname"] = current_user.username

    json_data["members"] = {}
    for member in room.members:
        json_data["members"][member.username] = url_for("auth.profile",  username= member.username)
    resp = Response(json.dumps(json_data))
    resp.content_type = "application/json"
    return resp

@login_required
def create_room_api():
    data = json.loads(request.data.decode())
    resp_data = {}
    try:
        room = Room()
        room.roomname = data["roomname"]
        room.creator_id = current_user.id
        room.members.append(current_user)
        db.session.add(room)
        db.session.commit()
        resp_data["Status"] = "Success"
        resp_data["Message"] = f"Successfully created room named {data['roomname']}"
    except Exception as e:
        resp_data["Status"] = "Failed"
        resp_data["Message"] = "Something went wrong!"
    resp = Response(json.dumps(resp_data))
    resp.content_type = "application/json"
    return resp




@login_required
def invitations_api():
    pass



