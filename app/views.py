import json
import time

from flask import render_template, redirect, flash, request, session
from flask_login import current_user, login_required
from sqlalchemy import text

from . import db
from .auth.models import User
from .models import Message

db_timestamp = None #Message.query.order_by(Message.timestamp.desc()).first().timestamp

def index():
    session['timestamp'] = 0.0
    global db_timestamp
    db_timestamp = Message.query.order_by(Message.timestamp.desc()).first()
    return render_template('index.html')

@login_required
def get_json():

    msg_dict = json.loads(request.data.decode())

    msg = Message()
    msg.sender_id = msg_dict['sender_id']
    msg.message = msg_dict['msg']
    msg.timestamp = time.time()
    
    db.session.add(msg)
    db.session.commit()
    session['timestamp'] = msg.timestamp
    global db_timestamp
    db_timestamp = msg

    return json.dumps(msg.timestamp)


@login_required
def send_json():
    t = time.time()
    #session['timestamp'] = json.loads(request.data.decode())

    last_msg = db_timestamp #Message.query.order_by(Message.timestamp.desc()).first()
    while (time.time()-t <10 ) and ((not last_msg) or (session['timestamp'] >= last_msg.timestamp )):
        last_msg = db_timestamp #Message.query.order_by(Message.timestamp.desc()).first()

    if(time.time()-t <= 10):
        return json.dumps('304')
    
    #print("************************************", session['timestamp'])
    msgs = list(map(Message.as_dict, Message.query.filter(text(f"message.timestamp > {session['timestamp']}")).all()))
    #print("************************msgs: ", msgs)

    session['timestamp'] = msgs[-1]['timestamp']

    return json.dumps(msgs)

