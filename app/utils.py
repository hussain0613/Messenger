naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


from functools import wraps
from flask_login import current_user
from flask import session, flash, redirect, url_for


def room_membership_required():
    from .models import Room
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if current_user.is_authenticated:
                if 'room_id' in session or 'room_id' in kwargs:
                    if('room_id' in session):
                        room = Room.query.get(session['room_id'])
                    elif 'room_id' in kwargs:
                        room = Room.query.get(kwargs['room_id'])
                    #if 'room_id' in session: ## eikhane aro nice kahini korte hbe..
                        ## may be somethin like current_user.role >= role
                    if current_user in room.members:
                        return view_func(*args, **kwargs)
                    else:
                        flash('You need to be a member of the room!', category="alert alert-warning")
                else:
                    flash('No room selected!', category="alert alert-warning")
            else:
                flash("You need to be logged in", category="alert alert-warning")
            return redirect(url_for('main.index'))
        return wrapper
    return decorator


def timestamps_cmp(ts1, ts2, curr_room_id = None):
    """
    ans will be with respect to ts1 
    """
    flag = 0
    ans = {}
    for room_id in ts2:
        if(room_id == curr_room_id): continue
        if room_id in ts1:
            if ts1[room_id] < ts2[room_id]:
                ans[room_id] = 1
                flag = 1
            else:
                ans[room_id] = 0
        else:
            ans[room_id] = 1
            flag = 1
            ## this one should raise exception may be..

        ## also if some room_id is in ts2 but not in ts1 that should raise an exception too.. but not now.. later
    
    return flag, ans
        



