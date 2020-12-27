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


function send_msg_json(url){
    var inp = document.getElementById('msg')
    if(userid == null){
        msg_dict = {
            'sender_id': userid,
            'sender': 'System!',
            'msg': '[!] You are not logged in!' 
        }
        display(msg_dict)
        return false
    }
    last_msg_id = 0;
    if (msgs.length>0){
        last_msg_id = msgs[msgs.length-1]['id']
    }
    msg_dict = {
        'id': last_msg_id+1,
        'sender_id': userid,
        'sender': username,
        'msg': inp.value,
        'timestamp': Date.now() 
    }
    display(msg_dict)
    msgs.push(msg_dict)
    inp.value = ''

    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200){
            var resp = JSON.parse(this.responseText);
            //msg_dict['id'] = resp['id']
            //msg_dict['timestamp'] = resp['timestamp']
            //msgs.push(msg_dict)
            if (msgs.length>0){
                msgs[msgs.length-1]['id'] = resp['id'];
            }
            return false;
        }
    }
    xhttp.open('POST', url, true);
    xhttp.send(JSON.stringify(msg_dict))
    return false;
}


function get_msgs_json(url){
    if(msgs.length>0){
        var last_msg = msgs[msgs.length-1]
        var last_ts = last_msg['timestamp']
        var last_msg_id = last_msg['id']
    }else{
        var last_msg = null;
        var last_ts = 0.0;
        var last_msg_id = null
    }
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200){
            var resp = JSON.parse(this.responseText);
            
            for (msg of resp){
                if(msg['id'] != last_msg_id){
                    display(msg);
                    msgs.push(msg)
                }
            }
            
            return check_room(check_room_url);
        }
    }
    xhttp.open('POST', url, true);
    if(last_msg_id){
        xhttp.send(JSON.stringify(last_msg_id))
    }else{
        xhttp.send(JSON.stringify(-1))
    }
}



function check_room(url){
    if(msgs.length>0){
        var last_msg = msgs[msgs.length-1]
        var last_ts = last_msg['timestamp']
        var last_msg_id = last_msg['id']
    }else{
        var last_msg = null;
        var last_ts = 0.0;
        var last_msg_id = null
    }

    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200){
            var resp = JSON.parse(this.responseText);
            
            if (resp == '200'){
                return get_msgs_json(send_msg_json_url);
            }
            else{
                return check_room(url);
            }
        }
    }
    xhttp.open('POST', url, true);
    if(last_msg_id){
        xhttp.send(JSON.stringify(last_msg_id))
    }else{
        xhttp.send(JSON.stringify(-1))
    }
}


