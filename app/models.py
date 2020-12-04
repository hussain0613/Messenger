import time

from .auth.models import User
from . import db

class Message(db.Model):
    __tablename__ = "message"
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    message = db.Column(db.Text)

    sender_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable = False, default = "unknown")
    sender = db.relationship("User", backref = db.backref("messages"))

    room_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable = False, default = 'unknown')
    room = db.relationship("room", backref = db.backref("messages"))

    timestamp = db.Column(db.Float, nullable = False, default = time.time())

    @staticmethod
    def as_dict(self):
        return {
            'sender_id': self.sender_id,
            'sender': self.sender.username,
            'msg': self.message,
            'timestamp': self.timestamp
        }


class Room(db.Model):

    __tablename__ = 'room'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    roomname = db.Column(db.String(50), unique = True)

    creator_id = db.Column(db.Integer, db.ForeignKey("User.id"), default = "unknown")
    creator = db.relationship("User", backref = db.backref("rooms_created"))


class P2PConnection(db.Model):

    __tablename__ = 'p2pconn'
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    user1_id = db.Column(db.Integer, db.ForeignKey("User.id"))
    user1 = db.relationship("User", backref = db.backref("friends", foreign_keys = ['p2pconn.user1_id', 'p2pconn.user2_id']), foreign_keys = ['user1_id'])

    user2_id = db.Column(db.Integer, db.ForeignKey("User.id"))
    user2 = db.relationship("User", backref = db.backref("friends", foreign_keys = ['p2pconn.user1_id', 'p2pconn.user2_id']), foreign_keys = ['user2_id'])

    __table_args__ = (db.UniqueConstraint('user1_id', 'user2_id', name = 'p2p_connection'),)



class P2RConnection(db.Model):

    __tablename__ = 'p2rconn'
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    user_id = db.Column(db.Integer, db.ForeignKey("room.id"))
    user = db.relationship("User", backref = db.backref("rooms"))

    room_id = db.Column(db.Integer, db.ForeignKey("User.id"))
    room = db.relationship("room", backref = db.backref("members"))

    __table_args__ = (db.UniqueConstraint('user_id', 'room_id', name = 'p2r_connection'),)


