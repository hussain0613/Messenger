from flask import request, request, Response
from flask_login import current_user, login_user, logout_user, login_required
from .models import db, User
import json

def login_api():
    resp = Response()
    resp.content_type = "text/json"
    resp_data = {}
    if current_user.is_authenticated:
        resp_data = {"Status":"Success", "Message":f"Alredy logged in as {current_user.username}", "uname": current_user.username, "name": current_user.name}
        resp.set_data(json.dumps(resp_data))
        return resp

    if request.method == "POST":
        data = json.loads(request.data.decode())
        un = data['username']
        psd = data['password']
        rm = data['rememberme']

        user = User.query.filter_by(username = un).first()

        if user and (user.checkPassword(psd)):
            login_user(user, remember= rm)
            resp_data = {"Status":"Success", "Message":f"Succesfully logged in as {un}", "uname": un, "name": user.name}
            resp.set_data(json.dumps(resp_data))
            ##if(body):
            ##    resp.set_cookie("user", body.split(':')[1]) 
            return resp
        else:
            resp_data = {"Status": "Failed", "Message":"invalid username and/or password!"}
    else:
        resp_data = {"Status": "Failed", "Message":"Method must be POST"}

    resp.set_data(json.dumps(resp_data))
    return resp


def logout_api():
    logout_user()
    resp = Response()
    resp.content_type = "text/json"
    resp_data = {"Status": "Success", "Message":"Successfully Logged Out"}
    resp.set_data(json.dumps(resp_data))
    #resop.set_cookie("user", "", )
    return resp