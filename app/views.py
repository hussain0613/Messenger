import json
import time

from flask import render_template, redirect, flash, request, Response, url_for, jsonify
from flask_login import current_user, login_required
from sqlalchemy import text, and_, update

from . import db
from .auth.models import User
from .models import Message, Room, Invitation, P2RConnection, Receivers

from .forms import CreateRoomForm
from .utils import room_membership_required


def index():
    return render_template('index.html')


@room_membership_required()
@login_required
def room_view(room_id):
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
        return redirect(url_for('main.room_view', room_id = room.id))

    return render_template('create_room.html', form = form)




@login_required
def delete_room():
    pass


@room_membership_required()
@login_required
def invite_members(room_id):
    guest_username = request.data.decode()
    user = User.query.filter_by(username = guest_username).first()
    if not user:
        return jsonify({'status': 'invalid user'})
    if(Invitation.query.filter(and_(Invitation.guest_id == user.id, Invitation.room_id == room_id))).all():
        return jsonify({'status': 'already sent'})
    
    inv = Invitation()
    inv.host_id = current_user.id
    inv.guest_id = user.id
    inv.room_id = room_id

    db.session.add(inv)
    db.session.commit()
    return jsonify({'status': '200'})


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


@room_membership_required()
@login_required
def delete_members():
    pass


@room_membership_required()
@login_required
def leave_room():
    pass

@login_required
def invitations():
    return render_template('invitations.html')


@room_membership_required()
@login_required
def get_msg_json(room_id):
    msg_dict = json.loads(request.data.decode())
    msg = Message()
    msg.message = msg_dict['msg']
    ## sender_id and current_user.id crosscheck
    msg.sender_id = msg_dict['sender_id']
    msg.room_id = room_id
    ## ts = time.time()
    msg.timestamp = msg_dict['timestamp']## ts
    room = Room.query.get(room_id)

    msg.receivers.extend([member for member in room.members if member.id != current_user.id])
    
    db.session.query(P2RConnection).filter(and_(P2RConnection.room_id == room_id, P2RConnection.user_id != current_user.id)).update({P2RConnection.status: "none"})

    db.session.add(msg)
    db.session.commit()

    resp = Response()
    resp.content_type = 'application/json'
    resp.set_data(json.dumps({'id': msg.id})) ## , 'timestamp': ts}))
    return resp


@room_membership_required()
@login_required
def send_msgs_json(room_id):
    #last_msg_ts = float(request.data.decode())
    last_msg_ts = int(request.data.decode())
    msgs = list(map(Message.as_dict, 
                Message.query.filter( and_( text(f'message.room_id = {room_id}'), text(f'message.id > {last_msg_ts}') ) ) 
                ))
    p2rconn = P2RConnection.query.filter(and_(P2RConnection.room_id == room_id, P2RConnection.user_id== current_user.id)).first()
    p2rconn.status = "seen" ## pore client theke feedback er bhittite korar bebostha korte hbe..
    db.session.commit()
    return jsonify(msgs)




@room_membership_required()
@login_required
def check_room(room_id):
    t = time.time()
    #last_msg_ts = float(request.data.decode())
    last_msg_id = int(request.data.decode())
    
    msgs = Message.query.filter( and_( text(f'message.room_id = {room_id}'), text(f'message.id > {last_msg_id}') ) ).all()
    while time.time()-t < 15 and not msgs:
        msgs = Message.query.filter( and_( text(f'message.room_id = {room_id}'), text(f'message.id > {last_msg_id}') ) ).all()
    if msgs:
        code = '200'
    else:
        code = '304'
    return jsonify(code)


@login_required
def check():
    t = time.time()
    #last_msg_ts = float(request.data.decode())
    #last_msg_id = int(request.data.decode())
    last_update_ts = float(request.data.decode())
    
    msgs = db.session.query(Message, Receivers, P2RConnection).filter(and_(
        Message.id == Receivers.message_id, Receivers.receiver_id == current_user.id, Message.timestamp > last_update_ts,
        P2RConnection.room_id == Message.room_id, P2RConnection.user_id == current_user.id, P2RConnection.status != 'seen'
        )).all()
    while time.time()-t < 15 and not msgs:
        msgs = db.session.query(Message, Receivers, P2RConnection).filter(and_(
        Message.id == Receivers.message_id, Receivers.receiver_id == current_user.id, Message.timestamp > last_update_ts,
        P2RConnection.room_id == Message.room_id, P2RConnection.user_id == current_user.id, P2RConnection.status != 'seen'
        )).all()
    resp = {}
    if msgs:
        resp['status'] = 200
        #update(P2RConnection).where(and_(P2RConnection.user_id == current_user.id, P2RConnection.status != "seen")).values(status = "notified")
        db.session.query(P2RConnection).filter(and_(P2RConnection.user_id == current_user.id, P2RConnection.status != 'seen')).update({P2RConnection.status: "notified"})
        rooms_with_new_msgs = set()
        for msg in msgs:
            #print("***************************************************************************msg: ",msg)
            rooms_with_new_msgs.add(msg[0].room.id)
        resp['rooms_with_new_msgs'] = list(rooms_with_new_msgs)
        resp['timestamp'] = msgs[-1][0].timestamp
        db.session.commit()
    else:
        resp['status'] = 304
    return jsonify(resp)
    
