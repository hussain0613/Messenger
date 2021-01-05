function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
  }
  
  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
  }

  function openNav_r() {
    document.getElementById("mySidenav2").style.width = "250px";
  }
  
  function closeNav_r() {
    document.getElementById("mySidenav2").style.width = "0";
    elem = document.getElementById('invite_msg');
    if(elem != null){
      elem.innerHTML = '';
      elem.classList.remove('alert');
      elem.classList.remove('alert-info')
    }
  }


  function invite_comm(url){
    try{
        form = document.forms['invite-form']
        uname = form['uname'].value
        form['uname'].value = '';
        xhttp = new XMLHttpRequest();
        
        xhttp.onreadystatechange = function(){
            elem = document.getElementById('invite_msg');
            if(this.readyState == 4 && this.status == 200){
                ans = JSON.parse(this.responseText);
                if(ans['status'] == '200'){
                    elem.innerHTML = 'Successfully sent to '+uname+'.';
                    //elem.classList.toggle('alert-success');
                }else if (ans['status'] == 'already one pending'){
                    elem.innerHTML = 'Already sent to '+ uname + '!';
                    //elem.classList.toggle('alert-info');
                }
                else if (ans['status'] == 'already member'){
                  elem.innerHTML = uname + ' is already a member!';
                }
                else{
                    elem.innerHTML = 'User '+ uname + ' not found!';
                    //elem.classList.toggle('alert-warning');
                }
                elem.classList.add('alert');
                elem.classList.add('alert-info');
            }
        }
        xhttp.open('POST', url, true)
        xhttp.send(uname)
        return false;
    }catch(err){
        console.log(err)
        return false
    }
}



mybutton = document.getElementById("toBottomBtn");
msg_field = document.getElementById("msg")

window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if ((document.body.scrollHeight-document.documentElement.scrollTop) <= screen.height || (document.body.scrollHeight-document.body.scrollTop) <= screen.height) {
    mybutton.style.display = "none";
  } else {
    mybutton.style.display = "block";
  }
}

function bottomFunction() {
  msg_field.scrollIntoView();
}

function showKick(m_id){
  document.getElementById('kick-div-'+m_id).style.display = 'block';
}

function hideKick(m_id){
  document.getElementById('kick-div-'+m_id).style.display = 'none';
}

function showMakeAdmin(m_id){
  document.getElementById('make-admin-div-'+m_id).style.display = 'block';
}

function hideMakeAdmin(m_id){
  document.getElementById('make-admin-div-'+m_id).style.display = 'none';
}

function toggle_admin_control(m_id){
  toggler = document.getElementById('toggler_'+m_id)
  buttons = document.getElementById('admin_control_buttons_'+m_id)
  if(buttons.style.display == 'none'){
    buttons.style.display = 'block'
    toggler.innerHTML = '-'
  }
  else{
    buttons.style.display = 'none'
    toggler.innerHTML = '+'
  }
  return false;
}


  