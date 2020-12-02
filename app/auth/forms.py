from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo


class SignUpForm(FlaskForm):
    name = StringField(label = 'Name', validators = [DataRequired()])
    username = StringField(label = 'Username', validators = [DataRequired()])
    email = StringField(label = 'Email', validators = [DataRequired(), Email()])
    email2 = StringField(label = 'Confirm Email', validators = [DataRequired(), Email(message="invalid email"), EqualTo('email', message='e-mails do not match')])
    password = PasswordField("Password", validators = [DataRequired()])
    password2 = PasswordField("Confirm Password", validators = [DataRequired(), EqualTo('password', message='passwords do not match')])
    submit = SubmitField(label="Sign Up")

class EditRoleForm(FlaskForm):
    role = SelectField('Role', choices=[('admin', 'Admin'), ('editor', 'Editor'), ('guest', 'Guest')], validators=[DataRequired()])
    confirm = SubmitField(label = "Confirm!")
    password = PasswordField(validators=[DataRequired()])


class LogInForm(FlaskForm):
    username = StringField(label = "Username", validators = [DataRequired()])
    password = PasswordField(label = "Password", validators = [DataRequired()])
    login = SubmitField(label = "Login")
    rememberme = BooleanField(label = "Remember me")
    submit = SubmitField(label = 'Login')

class RequestPasswordResetForm(FlaskForm):
    email = StringField(label = 'Email', validators=[Email()])
    submit = SubmitField(label = 'Submit')


class PasswordResetForm(FlaskForm):
    password = PasswordField("Password", validators = [DataRequired()])
    password2 = PasswordField("Confirm Password", validators = [DataRequired(), EqualTo('password', message='passwords do not match')])
    submit = SubmitField(label = 'Submit')


class UpdateUserInfoForm(SignUpForm):
    password = PasswordField("New Password")
    password2 = PasswordField("Confirm New Password", validators = [EqualTo('password', message='passwords do not match')])

    old_password = PasswordField("Old Password", validators = [DataRequired()])

    submit = SubmitField()


class DeleteUserForm(FlaskForm):
    password = PasswordField(validators=[DataRequired()])
    confirm = SubmitField()
