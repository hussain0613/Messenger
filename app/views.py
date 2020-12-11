import json
import time

from flask import render_template, redirect, flash, request, session, Response, url_for
from flask_login import current_user, login_required
from sqlalchemy import text, and_

from . import db
from .auth.models import User
from .models import Message, Room, Invitation

from .utils import room_membership_required, timestamps_cmp

from .forms import CreateRoomForm


#global_timestamps_json = None

def index():
    if(current_user.is_authenticated):
        
        if 'timestamps' not in session:
            d = dict([(str(room.id), 0.0) for room in current_user.rooms])
            session['timestamps'] = d

        if 'room_id' in session:
            session.pop('room_id')
        #print("***************************** session: ", session, 'ts: ', session['timestamps'])

    return render_template('index.html')


#@room_membership_required()
@login_required
def get_json():
    t = time.time()
    msg_dict = json.loads(request.data.decode())
    t2 = time.time()

    msg = Message()
    msg.sender_id = current_user.id #msg_dict['sender_id']
    msg.message = msg_dict['msg']
    msg.timestamp = time.time()
    if 'room_id' in session:
        msg.room_id = session['room_id']
    else:
        return 'no room'
    t3 = time.time()
    

    session['timestamps'][f"{session['room_id']}"] = msg.timestamp
    t4 = time.time()
    
    db.session.add(msg)
    db.session.commit()

    t5 = time.time()

    #global global_last_msg_timestamp
    #global_last_msg_timestamp = msg.timestamp
    print("******************** times in get:", t, t2, t3, t4, t5)
    
    return json.dumps(msg.timestamp)


#@room_membership_required()
@login_required
def send_json():
    t = time.time()
    #print("************************************", session['timestamp'])
    if 'room_id' in session:
        room_id = session['room_id']
    else:
        return 'no room'
    #timestamps = json.loads(session['timestamps_json'])

    t2 = time.time()
    curr_timestamps = session['timestamps']

    t3 = time.time()
    timestamps = current_user.get_last_messages_timestamps()
    t4 = time.time()
    session['timestamps'] = timestamps
    
    t5 = time.time()
    msgs = list(map( Message.as_dict, Message.query.filter(and_(text(f'room_id == {room_id}') , text(f"message.timestamp > {curr_timestamps[str(room_id)]}"))).all() ))
    #print("************************msgs: ", msgs)
    t6 = time.time()

    resp = Response()
    resp.content_type = 'application/json'
    #resp.headers['Cache-Control'] = 'no-cache'

    if(msgs):
        
        resp.set_data(json.dumps(msgs))
        
    else:
        #print("********************************* returning 304")
        #resp.status_code = 304
        resp.set_data(json.dumps('304'))
    t8 = time.time()

    print("*********************** timings:", t, t2, t3, t4, t5, t6, t8)
    return resp



@login_required
def check():
    t = time.time()

    if('room_id' in session):
        curr_room_id = str(session['room_id'])
        curr_room_ts = session['timestamps'][curr_room_id]
    else:
        curr_room_id = None


    cmp_res = timestamps_cmp(session['timestamps'], current_user.get_last_messages_timestamps(curr_room_id), curr_room_id = curr_room_id)
    while (time.time()-t <10 ) and not cmp_res[0]:
        cmp_res = timestamps_cmp(session['timestamps'], current_user.get_last_messages_timestamps(curr_room_id), curr_room_id)
    
    resp = Response()
    resp.content_type = 'application/json'
    if (time.time()-t >= 10 ):# or not cmp_res[0]:
        resp.set_data(json.dumps('304'))
    else:

        session['timestamps'] = current_user.get_last_messages_timestamps(curr_room_id = curr_room_id)
        if curr_room_id: session['timestamps'][curr_room_id] = curr_room_ts
        resp.set_data(json.dumps(cmp_res[1]))
    
    #print("****************************************** check", session['timestamps'], current_user.get_last_messages_timestamps(), cmp_res)
    return resp


#@room_membership_required()
@login_required
def inroom_check():
    t = time.time()
    ## print("************************************", session['timestamp'])
    if 'room_id' in session:
        room_id = str(session['room_id'])
        room = Room.query.get(room_id)
    else:
        return 'no room'
    
    #if not room.messages:
    #    return json.dumps('304')

    curr_timestamps = session['timestamps']

    while time.time() - t <10 and (not room.get_last_msg() or room.get_last_msg().timestamp <= curr_timestamps[room_id]):
        pass

    resp = Response()
    resp.content_type = 'application/json'
    
    if time.time() - t >= 10:# or (not room.get_last_msg() or room.get_last_msg().timestamp <= curr_timestamps[room_id]):
        
        resp.set_data(json.dumps('304'))
        
    else:
        #print("********************************* returning 304")
        #resp.status_code = 304
        resp.set_data(json.dumps('200'))
    
    return resp


@room_membership_required()
@login_required
def room_view(room_id):
    if 'timestamps' not in session:
            session['timestamps'] = dict([(room.id, 0.0) for room in current_user.rooms])
    
    session['room_id'] = room_id
    session['timestamps'][str(room_id)] = 0.0
    room = Room.query.get(room_id)
    #print("*********************** room_view: ", session['timestamps'])
    return render_template('room_view.html', room = room)


@login_required
def create_room():
    
    form = CreateRoomForm(request.form)

    if request.method == 'POST' and form.validate_on_submit():
        room = Room()
        room.roomname = form.name.data
        room.creator_id = current_user.id
        room.members.append(current_user)
        db.session.add(room)
        db.session.commit()

        flash('Room created successfully!', category='alert alert-success')
        session['room_id'] = room.id
        return redirect(url_for('main.room_view', room_id = room.id))

    return render_template('create_room.html', form = form)




@room_membership_required() ## also adminship of the room
@login_required
def delete_room():
    pass


@room_membership_required() ## also adminship of the room
@login_required
def invite_members():
    guest_username = request.data.decode()
    user = User.query.filter_by(username = guest_username).first()
    if not user:
        return '404'
    inv = Invitation()
    inv.host_id = current_user.id
    inv.guest_id = user.id
    inv.room_id = session['room_id']

    db.session.add(inv)
    db.session.commit()
    return '200'

@login_required
def accept_invitation(invitation_id, decision):
    inv = Invitation.query.get(invitation_id)

    if current_user.id == inv.guest_id and inv.status in ['pending', 'rejected']:
        if decision == 'yes':
            inv.status = 'accepted'
            #print("********************************* rooms: ", current_user.rooms, inv.room)
            current_user.rooms.append(inv.room)
        else:
            inv.status = 'rejected'
        db.session.commit()
        return redirect(url_for('main.room_view', room_id = inv.room_id))
    else:
        flash('You are not yet invited to this room or you have already accepted this invitaion', category='alert alert-warning')
        return redirect(url_for('main.index'))


@room_membership_required() ## also adminship of the room
@login_required
def delete_members():
    pass


@login_required
def invitations():
    return render_template('invitations.html')


    
    
