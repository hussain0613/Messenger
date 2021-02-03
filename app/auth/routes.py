from . import auth
from .views import (sign_up, login, logout, edit_role, request_password_reset, reset_password, profile, users,
                     update_user_info, delete_user, change_role_request)

from .api import login_api, logout_api

auth.route("/users/")(users)
auth.route("/profile/")(profile)
auth.route("/profile/<username>")(profile)
auth.route("/sign_up/", methods = ["GET", "POST"])(sign_up)
auth.route("/login/", methods = ["GET", "POST"])(login)
auth.route("/logout/")(logout)
auth.route("/edit_user_role/<int:pk>/", methods = ["GET", "POST"])(edit_role)

auth.route("/request_password_reset", methods = ["GET", "POST"])(request_password_reset)
auth.route("/reset_password/<token>/", methods = ["GET", "POST"])(reset_password)

auth.route("/update_info/", methods = ["GET", "POST"])(update_user_info)
auth.route("/delete_user/<username>", methods = ["GET", "POST"])(delete_user)
auth.route("/change_role_request/")(change_role_request)

auth.route("/api/login/", methods = ["GET", "POST"])(login_api)
auth.route("/api/logout/")(logout_api)
