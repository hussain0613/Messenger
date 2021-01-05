from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class CreateRoomForm(FlaskForm):
    name = StringField(label = 'Name', validators=[DataRequired()])
    submit = SubmitField(label='Create Room')


class InvitationForm(FlaskForm):
    name = StringField(label='Name:', validators=[DataRequired()])
    submit = SubmitField(label='Invite')

class DeleteRoomForm(FlaskForm):
    roomname = StringField(label='Room name: ', validators=[DataRequired()])
    password = PasswordField(label="Confirm: ", validators=[DataRequired()])
    delete = SubmitField(label="Delete!")

