import time

from .auth.models import User
from . import db
from  sqlalchemy import and_, text

class Message(db.Model):
    __tablename__ = "message"
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    message = db.Column(db.Text)

    sender_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable = True, default = 'deleted_user')
    sender = db.relationship("User", backref = db.backref("sent_messages"))

    room_id = db.Column(db.Integer, db.ForeignKey("room.id"), nullable = True, default = 'deleted_room')
    room = db.relationship("Room", backref = db.backref("messages"))

    receivers = db.relationship("User", secondary = "receivers", backref = db.backref("messages_received"))

    timestamp = db.Column(db.Float, nullable = False, default = time.time(), index = True)

    @staticmethod
    def as_dict(self):
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'sender': self.sender.username,
            'msg': self.message,
            'timestamp': self.timestamp
        }


class Room(db.Model):

    __tablename__ = 'room'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    roomname = db.Column(db.String(50))

    creator_id = db.Column(db.Integer, db.ForeignKey("User.id"), default = "unknown")
    creator = db.relationship("User", backref = db.backref("rooms_created"))


    members = db.relationship('User', secondary = 'p2rconn', backref = db.backref('rooms'))

    def get_last_msg(self):
        if self.messages:
            return next(reversed(self.messages))
        else:
            return None
    def get_p2r_obj(self, member_id):
        p2r = db.session.query(P2RConnection).filter(and_(
            text(f"p2rconn.room_id = {self.id}"),
            text(f"p2rconn.user_id = {member_id}")
            )).first()
        return p2r

class P2PConnection(db.Model):

    __tablename__ = 'p2pconn'
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    user1_id = db.Column(db.Integer, db.ForeignKey("User.id"))
    user2_id = db.Column(db.Integer, db.ForeignKey("User.id"))

    ## relationship base thik korte hbe.
    user1 = db.relationship("User", backref = db.backref("shortlist", foreign_keys = [user1_id]), foreign_keys = [user1_id])
    user2 = db.relationship("User", backref = db.backref("shortlisted_by", foreign_keys = [user2_id]), foreign_keys = [user2_id])

    __table_args__ = (db.UniqueConstraint(user1_id, user2_id, name = 'p2p_connection'),)



class P2RConnection(db.Model):

    __tablename__ = 'p2rconn'
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    user_id = db.Column(db.Integer, db.ForeignKey("User.id"))
    user = db.relationship("User", backref = db.backref("p2rconn"))

    room_id = db.Column(db.Integer, db.ForeignKey("room.id"))
    room = db.relationship("Room", backref = db.backref("p2rconn"))

    status = db.Column(db.String(50), default = 'none') ## seen, notified, none eita bhul jaygay disi.. eita receives e hbe.
    role = db.Column(db.String(50), default = 'member')


    __table_args__ = (db.UniqueConstraint('user_id', 'room_id', name = 'p2r_connection'),)



class Receivers(db.Model):

    __tablename__ = 'receivers'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    message_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    message = db.relationship("Message", backref = db.backref("receivers_obj")) ## the backref names are not 'right'

    receiver_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    receiver = db.relationship('User', backref = db.backref('receiver_obj'))


class Invitation(db.Model):
    __tablename__ = 'invitation'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    host_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    host = db.relationship("User", backref = db.backref("invitations_sent"), foreign_keys = [host_id])

    guest_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    guest = db.relationship("User", backref = db.backref("invitations_received"), foreign_keys = [guest_id])

    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    room = db.relationship('Room', backref=db.backref('invitations'))
    
    status = db.Column(db.String(50), default = 'pending') ## pending, accepted, rejected

    



