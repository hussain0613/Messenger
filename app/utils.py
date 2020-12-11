naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

from functools import wraps
from flask_login import current_user
from flask import flash, url_for, redirect
#from .models import Room
def room_membership_required():
    from functools import wraps
    from .models import Room
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            room = Room.query.get(kwargs['room_id'])
            if current_user.is_authenticated:
                if current_user in room.members:
                    ## may be somethin like current_user.role >= role
                    return view_func(*args, **kwargs)
                else:
                    flash(f"Access Denied! Not a member", category="alert alert-warning")    
            else:
                flash("You need to be logged in", category="alert alert-warning")
            return redirect(url_for('main.index'))
        return wrapper
    return decorator


