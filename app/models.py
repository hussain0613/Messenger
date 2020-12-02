import time

from .auth.models import User
from . import db

class Message(db.Model):
    __tablename__ = "message"
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    message = db.Column(db.Text)

    sender_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable = False, default = "unknown")
    sender = db.relationship("User", backref = db.backref("messages"))

    timestamp = db.Column(db.Float, nullable = False, default = time.time())

    @staticmethod
    def as_dict(self):
        return {
            'sender_id': self.sender_id,
            'sender': self.sender.username,
            'msg': self.message,
            'timestamp': self.timestamp
        }



