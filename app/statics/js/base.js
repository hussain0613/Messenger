var msgs = []
var c = 0;

function check_logged_in(){
    cookies = document.cookie.split(';')
    for(cookie of cookies){
        key_value = cookie.split('=')
        if(key_value[0] == 'name'){
            name = key_value[1]
        }
    }
    if (name != "NaN" && name != NaN){
        document.getElementById('div-login').style.visibility='hidden';
        document.getElementById('messenger').style.visibility='visible';
        document.getElementById('div-logout').style.visibility='visible';
    }else{
        document.getElementById('div-login').style.visibility='visible';
        document.getElementById('messenger').style.visibility='hidden';
        document.getElementById('div-logout').style.visibility='hidden';
    }
    get(send_url)
}

function display(msg_dict){
    var str_c = c.toString();
    var sender_id = 'sender_' + str_c;
    var msg_id = 'msg_' + str_c;
    
    document.getElementById('display').innerHTML += `<div id = 'msg_div_${str_c}' style='visibility: hidden' class='clearfix container-fluid'>
        <strong class = 'clearfix'><header id = 'sender_${str_c}'></header></strong><p id='msg_${str_c}'></p>
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
    /*document.getElementById('display').innerHTML += `<div id = 'msg_div_${str_c}' style='visibility: hidden' class='clearfix container-fluid'>
        <strong class = 'clearfix'><header id = 'sender_${str_c}'></header></strong><p id='msg_${str_c}'></p>
        <hr>
    </div>
    `;*/
    
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
        if(msgs.length != 0){
            var last_msg_timestamp = msgs[msgs.length - 1]['timestamp'];
        }else{
            last_msg_timestamp = 0.0;
        }
        if (this.readyState == 4 && this.status == 200){
            new_msgs = JSON.parse(this.responseText)
            for (msg of new_msgs){
                if(last_msg_timestamp != msg['timestamp'])
                    display(msg)
            }
            msgs.push(...new_msgs)
            get_json(url)
        }
    }
    xhttp.open("GET", url, true)
    xhttp.send()
}




function logout(url){
    
    //gotta send data to the server
    document.getElementById('display').innerHTML = ""
    c = 0;
    name = NaN
    msgs = []
    var xhttp = new XMLHttpRequest();
    xhttp.open('GET', url, true);
    xhttp.send()
    
    document.getElementById('div-login').style.visibility='visible';
    document.getElementById('messenger').style.visibility='hidden';
    document.getElementById('div-logout').style.visibility='hidden';
    return false;
}

