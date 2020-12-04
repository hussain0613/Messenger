var msgs = []
var c = 0;

function display(msg_dict){
    var str_c = c.toString();
    var sender_id = 'sender_' + str_c;
    var msg_id = 'msg_' + str_c;
    
    document.getElementById('display').innerHTML += `<div id = 'msg_div_${str_c}' style='visibility: hidden' class='clearfix container-fluid'>
        <strong class = 'clearfix'><header id = 'sender_${str_c}'></header></strong><p id='msg_${str_c}' class = 'text-display'></p>
        <hr>
    </div>
    `;

    if(msg_dict['sender_id'] == userid){
        document.getElementById('msg_'+str_c).classList.add('float-right')
        document.getElementById('sender_'+str_c).classList.add('float-right')
    }
    document.getElementById('msg_div_'+str_c).style.visibility = 'visible';
    document.getElementById(sender_id).innerHTML = msg_dict['sender'];
    document.getElementById(msg_id).innerHTML = msg_dict['msg'];
    ++c;
    str_c = c.toString();
    return false;
}

function login(url){
    name = document.forms['login-form']['name'].value
    
    //gotta send data to the server
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200){
            get(send_url)
        }
    }
    xhttp.open('POST', url, true);
    xhttp.send(name)
    
    document.getElementById('div-login').style.visibility='hidden';
    document.getElementById('messenger').style.visibility='visible';
    document.getElementById('div-logout').style.visibility='visible';

    return false;
}

function send_json(url){
    input = document.forms['msngr-form']['msg']
    msg = input.value;
    input.value = ''
    var ts = Date.now();
    msg_dict = {
        'sender_id': userid,
        'sender': username,
        'msg': msg,
        'timestamp': ts
    }
    msgs.push(msg_dict)
    display(msg_dict);

    //gotta send msg to the server
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200){
            ts = JSON.parse(this.responseText)
            msgs[msgs.length - 1]['timestamp'] = ts
        }
    }
    xhttp.open('POST', url, true);
    xhttp.send(JSON.stringify(msg_dict))

    return false;
}

function get_json(url){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200){
            new_msgs = JSON.parse(this.responseText)
            if(new_msgs == '304'){
                return check(check_url)
            }
            if(msgs.length != 0){
                var last_msg_timestamp = msgs[msgs.length - 1]['timestamp'];
            }else{
                last_msg_timestamp = 0.0;
            }
            for (msg of new_msgs){
                if(last_msg_timestamp != msg['timestamp'])
                    display(msg)
            }
            msgs.push(...new_msgs)
            //console.log("200:- " + this.status)
            return check(check_url)
        }
        else if(this.readyState == 4 && this.status == 304){
            //console.log("304:-" + this.status)
            return check(check_url)
        }
        else if(this.readyState == 4 && this.status == 500){
            var msg = "[!] Whoa! Calm down mate, please be a bit gentle with the server! And also please refresh the page! And also could you\
            plese ask your friend to do the same too?!"
            display({'sender': '[!]SERVER', 'msg': msg})
            return check(check_url)
        }
    }
    xhttp.open("GET", url, true)
    xhttp.send()
}



function check(url){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200){
            resp = JSON.parse(this.responseText)
            if(resp == '304'){
                //console.log('checkf: 304:-', resp)
                return check(url)
            }else{
                //console.log('checkf: non 304:-', resp)
                return get_json(send_json_url)
            }
        }
        else if(this.readyState == 4 && this.status == 500){
            var msg = "[!] Whoa! Calm down mate, please be a bit gentle with the server! And also please refresh the page! And also could you\
            plese ask your friend to do the same too?!"
            display({'sender': '[!]SERVER', 'msg': msg})
            //console.log('checkf: 500:-', resp)
            return check(url)
        }
    }
    xhttp.open("GET", url, true)
    xhttp.send()
}
