from flask import flash, redirect, url_for
from flask_login import current_user
from sqlalchemy import or_
from .models import User


def role_required(*roles):
    from functools import wraps
    if not roles:
        roles = ['admin']
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if current_user.is_authenticated:
                if current_user.role.lower() in roles or ('self' in roles and current_user.username == kwargs.get('username', None)): ## eikhane aro nice kahini korte hbe..
                    ## may be somethin like current_user.role >= role
                    return view_func(*args, **kwargs)
                else:
                    flash(f"You need to have either one of these roles {roles}", category="alert alert-warning")    
            else:
                flash("You need to be logged in", category="alert alert-warning")
            return redirect(url_for('database.tables'))
        return wrapper
    return decorator


signup_mail_body = """Welcome to Dictionary. It is in test version still now. So please have dhoirjo.
details:
name: {name}
username: {username}

for any query contact any of the admins.
"""

reset_password_mail_body = """To reset your passowrd please visit the following link: 
{reset_pass_url_with_token}

if you did not request for a password reset, please ignore.
"""

update_user_info_mail_body = """your user info's have been updated.
details after updating:
name: {name}
username: {username}
emial: {email}

if you have not changed these, please immedietly contatct one of the admins.
admins' emails:
{admin_emails}
"""

admin_emails = []
def get_admin_emails():
    global admin_emails
    if not admin_emails:
        admin_emails = [admin.email for admin in User.query.filter(or_(User.role == 'Admin', User.role =='admin', User.role == 'ADMIN') )]
    return admin_emails


change_role_request_mail_body = """username: {username}
current role: {role} 
"""
