from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import bcrypt
import os
import datetime

from . import db, login

class User(UserMixin, db.Model):
    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    name = db.Column(db.String(200), nullable = False)
    username = db.Column(db.String(200), unique = True, nullable = False, index =True)
    email = db.Column(db.String(200), unique = True, nullable = False, index = True)
    password = db.Column("password", db.String(300), nullable = False)

    role = db.Column("role", db.String(20), default = "Guest")


    creator_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    creator = db.relationship('User', backref = db.backref('users_created',cascade="save-update"), cascade="save-update", foreign_keys=[creator_id], remote_side = 'User.id', post_update = True)
    creation_date = db.Column(db.DateTime, default = datetime.datetime.utcnow())

    last_modifier_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    last_modifier = db.relationship('User', backref = db.backref('users_modified',cascade="save-update"), cascade="save-update", foreign_keys=[last_modifier_id], remote_side = 'User.id', post_update = True)
    last_modified_date = db.Column(db.DateTime, default = datetime.datetime.utcnow())    

    def setPassword(self, psd):
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(psd.encode('utf-8'), salt).decode('utf-8')
    
    def checkPassword(self, psd):

        return bcrypt.checkpw(psd.encode('utf-8'), self.password.encode('utf-8'))
    
    def get_reset_token(self, exp = 300):
        s = Serializer(os.getenv('SECRET_KEY'), 300)
        return s.dumps({'user_id': self.id}) # .decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(os.getenv('SECRET_KEY'))
        try:
            user_id = s.loads(token)['user_id']
            return User.query.get(user_id)
        except Exception:
            return None
        


@login.user_loader
def load_user(id):
    return User.query.get(int(id))