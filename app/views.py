import json
import time

from flask import render_template, redirect, flash, request, session, Response
from flask_login import current_user, login_required
from sqlalchemy import text

from . import db
from .auth.models import User
from .models import Message

global_last_msg_timestamp = 0.0 #Message.query.order_by(Message.timestamp.desc()).first().timestamp

def index():
    session['timestamp'] = 0.0
    msg = Message.query.order_by(Message.timestamp.desc()).first()
    global global_last_msg_timestamp
    if(msg):
        global_last_msg_timestamp = msg.timestamp
    else:
        global_last_msg_timestamp = 0.0
    
    return render_template('index.html')

@login_required
def get_json():

    msg_dict = json.loads(request.data.decode())

    msg = Message()
    msg.sender_id = msg_dict['sender_id']
    msg.message = msg_dict['msg']
    msg.timestamp = time.time()
    
    session['timestamp'] = msg.timestamp
    
    db.session.add(msg)
    db.session.commit()


    global global_last_msg_timestamp
    global_last_msg_timestamp = msg.timestamp
    
    return json.dumps(msg.timestamp)


@login_required
def send_json():
    #print("************************************", session['timestamp'])
    msgs = list(map(Message.as_dict, Message.query.filter(text(f"message.timestamp > {session['timestamp']}")).all()))
    #print("************************msgs: ", msgs)


    resp = Response()
    resp.content_type = 'application/json'
    #resp.headers['Cache-Control'] = 'no-cache'

    if(msgs):
        #print("********************** returning msgs:", msgs)
        session['timestamp'] = msgs[-1]['timestamp']
        resp.set_data(json.dumps(msgs))
        
    else:
        #print("********************************* returning 304")
        #resp.status_code = 304
        resp.set_data(json.dumps('304'))
    
    return resp


@login_required
def check():
    t = time.time()
    while (time.time()-t <10 ) and session['timestamp'] >= global_last_msg_timestamp:
        pass
    
    resp = Response()
    resp.content_type = 'application/json'
    if (time.time()-t > 10 ) or session['timestamp'] >= global_last_msg_timestamp:
        resp.set_data(json.dumps('304'))
    else:
        resp.set_data(json.dumps('200'))
    
    return resp
    
    
    
