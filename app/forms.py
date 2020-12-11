from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CreateRoomForm(FlaskForm):
    name = StringField(label = 'Name', validators=[DataRequired()])
    submit = SubmitField(label='Create Room')


class InvitationForm(FlaskForm):
    name = StringField(label='Name:', validators=[DataRequired()])
    submit = SubmitField(label='Invite')

