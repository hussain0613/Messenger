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

