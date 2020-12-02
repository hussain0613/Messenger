from flask import request, flash, render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from flask_mail import Message
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_

import os

#from ..database.models import Actions

from . import mail, login

from .forms import (LogInForm, SignUpForm, EditRoleForm, RequestPasswordResetForm, PasswordResetForm, UpdateUserInfoForm,
                    DeleteUserForm)
from .models import db, User#, Actions
from .utils import role_required, signup_mail_body, reset_password_mail_body, update_user_info_mail_body, get_admin_emails, change_role_request_mail_body

@login_required
def profile(username = None):
    if username == current_user.username or username == None:
        user = current_user
    else:
        user = User.query.filter_by(username = username).first()
    return render_template("profile.html", user = user)

@login_required
def users():
    return render_template("users.html", users = User.query.all())



def sign_up():
    
    if current_user.is_authenticated:
        flash("Please logout first to create new account")
        return redirect(url_for('auth.profile'))
    
    form = SignUpForm()

    if request.method == "POST" and form.validate_on_submit():
        try:
            user = User()
            form.populate_obj(user)
            user.setPassword(form.password.data)
            
            db.session.add(user) 
            db.session.commit()
            #login_user(user)
            #db.session.add(Actions('create', 'user', current_user.id))
            #logout_user()

            msg = Message('Dictionary: Welcome to Dictionary', sender = os.environ.get('MAIL_USERNAME')+"@gmail.com", recipients = [user.email])
            msg.body = signup_mail_body.format(name = user.name, username = user.username)
            #mail.send(msg)
            flash(f"An email has been sent to your email :v", category="alert alert-info")

            flash("successfully created your id, u should get an email", category="alert alert-success")
            return redirect(url_for('auth.profile', username = user.username))
        
        except IntegrityError:
            db.session.rollback()
            flash("username/email already exists", category="alert alert-danger")

    
    return render_template('signup.html', form = form)



def login():
    if current_user.is_authenticated:
        flash("You are already logged in")
        return redirect(url_for('main.index'))

    
    if request.method == "POST":
        form = LogInForm(request.form, obj = User)

        if form.validate_on_submit():
            un = form.username.data
            psd = form.password.data

            user = User.query.filter_by(username = un).first()

            if user and (user.checkPassword(psd)):
                login_user(user, remember= form.rememberme.data)
                flash(f"logged in successfully as {un}", category="alert alert-success")
                return redirect(url_for('main.index'))
            else:
                flash("invalid username and/or password!", category="alert alert-warning")
        else:
            flash("something went wrong with submission. not sure what though :/ ", category="alert alert-danger")


    form = LogInForm(request.form)

    return render_template("login.html", form = form)


def logout():
    logout_user()
    return redirect(url_for('main.index'))

@role_required('admin')
@login_required
def edit_role(pk):
    ## user handling er shob kichu alada korte hbe..
    user = User.query.get(pk)

    if not user:
        flash(f"user with id = {pk} does not exist")
        return redirect(url_for('main.index'))

    if request.method == "POST":
        form = EditRoleForm(request.form)

        if form.validate_on_submit():
            psd = form.password.data
            if current_user.checkPassword(psd):
                user.role = form.role.data
                #db.session.add(Actions('promote', 'users', current_user.id))
                db.session.commit()
                
                msg = Message('Dictionary: Role Update', sender = os.environ.get('MAIL_USERNAME')+"@gmail.com", recipients = [user.email])
                msg.body = f"your role has been updated to {user.role}.\n For furthur query contact one of the admins."
                mail.send(msg)
                
                flash(f"Successfully updated user {user.username}'s role to {user.role}")
                return redirect(url_for('auth.users'))
            else:
                flash("Wrong password")
        else:
            flash("something went wrong with submission. not sure what though :/ ")


    form = EditRoleForm(request.form)
    form.role.data = user.role

    return render_template("edit_role.html", form = form, user = user)
    


def request_password_reset():
    if current_user.is_authenticated:
        flash("you are already logged in")
        return redirect(url_for('database.tables'))
    
    if request.method == "POST":
        form = RequestPasswordResetForm(request.form)

        if form.validate_on_submit():
            email = form.email.data

            user = User.query.filter_by(email = email).first()

            if user:
                token = user.get_reset_token()
                
                msg = Message('Dictionary: Password Reset Request', sender = os.environ.get('MAIL_USERNAME')+"@gmail.com", recipients = [user.email])
                msg.body = reset_password_mail_body.format(reset_pass_url_with_token = url_for('auth.reset_password', token = token, _external=True))
                mail.send(msg)
                
                flash(f"An email has been sent to your email with instruction for reseting your password")
                return redirect(url_for('auth.login'))
            else:
                flash("invalid email!")
        else:
            flash("something went wrong with submission. invalid email most probably ")


    form = RequestPasswordResetForm(request.form)

    return render_template("request_password_reset.html", form = form)


def reset_password(token):
    if current_user.is_authenticated:
        flash("you are already logged in")
        return redirect(url_for('database.tables'))
    
    user = User.verify_reset_token(token)

    if not user:
        flash("Token invalid or expired! Plese try again!")
        return redirect(url_for('auth.request_password_reset'))
    
    form = PasswordResetForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            pswd = form.password.data
            user.setPassword(pswd)
            db.session.commit()
            flash("Password reset successful")
            return redirect(url_for('auth.login'))
    
    return render_template('reset_password.html', form = form, token = token)


@login_required
def update_user_info():
    user = current_user
    mails = [user.email]

    form = UpdateUserInfoForm(request.form, obj = user)
    if request.method == 'POST':
        if form.validate_on_submit():
            if current_user.checkPassword(form.old_password.data):
                form.populate_obj(user)
                
                if(form.password.data):
                    user.setPassword(form.password.data)
                else:
                    user.setPassword(form.old_password.data)

                #db.session.add(Actions("edit", "user", current_user.id))
                try:
                    db.session.commit()
                    flash("Successfully updated!")
                    if(user.email not in mails): 
                        mails.append(user.email)
                    msg = Message('Dictionary: Information Update', sender = os.environ.get('MAIL_USERNAME')+"@gmail.com", recipients = mails)
                    msg.body = update_user_info_mail_body.format(
                        name = user.name, username = user.username, email = user.email,
                        admin_emails = get_admin_emails()
                    )
                    mail.send(msg)

                    return redirect(url_for('auth.profile', username = user.username))
                except IntegrityError:
                    db.session.rollback()
                    flash("username or email already exists")

            else:
                flash("Wrong old password!")
        else:
            flash("Something wrong with form validation")
    
    return render_template("update_user_info.html", form = form)

@role_required('admin', 'self')
@login_required
def delete_user(username):
    user = User.query.filter_by(username = username).first()
    form = DeleteUserForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():
            psd = form.password.data
            if current_user.checkPassword(psd):
                #db.session.add(Actions("delete", 'user', current_user.id))
                db.session.delete(user)
                db.session.commit()

                msg = Message('Dictionary: Account Deleted!', sender = os.environ.get('MAIL_USERNAME')+"@gmail.com", recipients = [user.email])
                msg.body = f"Your account has been deleted.\n If do not know why this has happend, contact the admins immedietly."
                mail.send(msg)

                flash(f"User-{username}'s acount been deleted!")
                return redirect(url_for('auth.users'))
            else:
                flash("wrong password")
        else:
            flash("something went wong with form submission")
    return render_template('delete_user.html', form = form, username = username)


@login_required
def change_role_request():

    msg = Message('Dictionary: Change Role Request', sender = os.environ.get('MAIL_USERNAME')+"@gmail.com", recipients = get_admin_emails())
    msg.body = change_role_request_mail_body.format(username = current_user.username, role = current_user.role)
    mail.send(msg)

    flash('the admins have been notified, please wait')
    return redirect(url_for('auth.profile'))

