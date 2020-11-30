from flask import Flask, render_template, request, make_response, session, Response
#from flask.ext.socketio import SocketIO, emit
import json
import time
from collections import OrderedDict
from functools import wraps

messeges = OrderedDict()

sessions = []

app = Flask(__name__, static_folder='statics', template_folder='templates')
app.secret_key = 'secret'

devices = {}
def create_device_name(string):
    name = ''
    if('Windows' in string):
        name += 'pc'
    elif 'Android' in string:
        name += 'android'
    else:
        name += 'un'
    
    if ('Chrome' in string):
        name += '_chrome'
    elif ('Firefox' in string):
        name += '_firefox'
    else:
        name+= '_un'
    return name

def get_device_name(string):
    if string not in devices:
        devices[string] = create_device_name(string)
    return devices[string]


def login_required():
    from functools import wraps
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if 'name' in session:
                return view_func(*args, **kwargs)
            
            resp = Response()
            resp.status_code = 403
            return resp
        return wrapper
    return decorator




@app.route("/")
def index():
    #if 'timestamp' in session and messeges and session['timestamp'] == next(reversed(messeges)):
    #    resp = Response()
    #    resp.status_code = 304
    #    return resp

    print("[***************************************************************************] request.environ[usr_ant]: ", get_device_name(request.environ['HTTP_USER_AGENT']))
    
    session['timestamp'] = 0.0
    
    resp = Response(render_template('index.html'))
    if 'name' in session:
        resp.set_cookie('name', session['name'])
    
    return resp


@app.route('/login/', methods =['POST'])
def login():
    #print("login: env:", request.environ, "data: ", request.data)
    name = request.data.decode()
    session['timestamp'] = 0.0
    session['name'] = name
    resp = make_response(f'from login, name: {name}')
    resp.set_cookie('name', name)
    print(f"[*] name: {get_device_name(request.environ['HTTP_USER_AGENT'])}")
    return resp


@app.route('/get/', methods = ['POST'])
def get():
    #print("process: env:", request.environ, "data: ", request.data)
    msg = request.data.decode()
    msg = json.loads(msg)
    msg['timestamp'] = time.time()
    session['timestamp'] = msg['timestamp']
    messeges[msg['timestamp']] = msg
    print(f"[*] name: {get_device_name(request.environ['HTTP_USER_AGENT'])}")
    return json.dumps(msg['timestamp'])



@app.route('/send/')
@login_required()
def send():
    t = time.time()
    
    print(f"[*] send to client name 1 : {get_device_name(request.environ['HTTP_USER_AGENT'])}, timestamp: {session['timestamp']}")
    
    while time.time()-t < 25 and ((not messeges) or session['timestamp'] == next(reversed(messeges))):
        pass

    if time.time()-t >= 25:
        resp = make_response(json.dumps(304))
        resp.headers['Content-Type'] = 'application/json'
        return resp
    if int(session['timestamp']) > 0:
        new_msgs = [messeges[msg] for msg in messeges if msg > session['timestamp']]
    else:
        new_msgs = list(messeges.values())
    
    print(f"[*] send to client name 2 : {get_device_name(request.environ['HTTP_USER_AGENT'])}, s_ts: {session['timestamp']}, new_msgs: {new_msgs}")

    session['timestamp'] = new_msgs[-1]['timestamp']
    resp = make_response(json.dumps(new_msgs))
    resp.headers['Content-Type'] = 'application/json'
    print(f"[*] send to client name 3 : {get_device_name(request.environ['HTTP_USER_AGENT'])}, s_ts: {session['timestamp']}, new_msgs: {new_msgs}")
    ## bebostha korte hbe jeno logout howar pore logut howar ager rqst er msg o na pay
    return resp


@app.route('/logout/')
def logout():
    if 'name' in session:
        session.pop('name')
    if 'timestamp' in session:
        session.pop('timestamp')
    
    session.clear()
    resp = make_response()
    resp.set_cookie('name','', expires = 0.0)
    #resp.set_cookie('session','', expires = 0.0)
    print(f"[*]logout name: {get_device_name(request.environ['HTTP_USER_AGENT'])}")
    return resp


if __name__ == '__main__':
    app.config["SERVER_NAME"] = "bcc0613.herokuapp.com"
    app.run(debug = True)
    

