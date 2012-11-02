function hideAll(){//hide all divs in profile
    $("div#home").hide();
    $("div#userprofile").hide();
    $("div#setting").hide();
    $("div#consign").hide();
    $("div#request").hide();
    $("li#li_home").attr("class","");
    $("li#li_setting").attr("class","");
    $("li#li_userprofile").attr("class","");
    $("li#li_consign").attr("class","");
    $("li#li_request").attr("class","");
    $("li#li_help-consign").attr("class","");
    $("li#li_help-buying").attr("class","");
}
function showUserHome(){
    hideAll();
    show("home");
}
function showProfile(){
    hideAll();
    show("userprofile");
}
function showSettings(){
    hideAll();
    show("setting");
}
function showConsigned(){
    hideAll();
    show("consign");
    loadConsigned();
}
function showRequested(){
    hideAll();
    show("request");
    loadRequested();
}
function show(targ){
    $("div#"+targ).show();
    $("#li_"+targ).attr("class","active");
}
/* functions to request from server data about consignment*/
function loadConsigned(){
    var xmlhttp = ajaxRequest();
    xmlhttp.onreadystatechange=function(){
        if (xmlhttp.readyState===2){
            $("#consign-loading").show();
        }else if(xmlhttp.readyState===4){
            if (xmlhttp.status===200){
                //populate data
            }else if (xmlhttp.status === 400){//no data

            }else{
                $("#consign-loading").hide();
                $("#consign-response").text("Failed to fetch data. Please try again in a while.");
                $("#consign-response").show();
            }
        }
    }
    var params="";
    xmlhttp.open("POST","/",true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xmlhttp.send(params);
}
function loadRequested(){
    var xmlhttp = ajaxRequest();
    xmlhttp.onreadystatechange=function(){
        if (xmlhttp.readyState===2){
            $("#request-loading").show();
        }else if(xmlhttp.readyState===4){
            if (xmlhttp.status===200){
                //populate data
            }else if (xmlhttp.status === 400){//no data

            }else{
                $("#request-loading").hide();
                $("#request-response").text("Failed to fetch data. Please try again in a while.");
                $("#request-response").show();
            }
        }
    }
    var params="";
    xmlhttp.open("POST","/",true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xmlhttp.send(params);
}
/*functions to change user information*/
function changeName(){
    changeGeneral("name");
}
function changeEmail(){
    changeGeneral("email");
}
function changeNum(){
    changeGeneral("num");
}
function changeCollege(){
    changeGeneral("college");
}
function changeDegree(){
    changeGeneral("degree");
}
function changeDormitory(){
    changeGeneral("dormitory");
}
function changeGeneral(n){
    document.getElementById("form-"+n).className="";
    document.getElementById("edit-"+n).innerText=" ok";
    document.getElementById("href-"+n).setAttribute("onclick","hideProfile('"+n+"')");
    document.getElementById("user-"+n).className="hidden";    
    document.getElementById("update-profile-submit").className="btn btn-success pull-right";
}
function hideProfile(n){//function to hide the "edit" of profile
    document.getElementById("edit-"+n).innerText=" edit";
    if (n === 'name'){
        document.getElementById("user-name").innerText = document.getElementById("name-last").value + ", " +document.getElementById("name-first").value;
    }else{
        document.getElementById("user-"+n).innerText = document.getElementById("input-"+n).value;
    }
    document.getElementById("user-"+n).className="";
    document.getElementById("form-"+n).className="hidden";
    document.getElementById("href-"+n).setAttribute("onclick","change"+n.toProperCase()+"()");
}
//marker when a value in profile changes, used by the ajax request to determine if value would be sent to server
function change(n){
    document.getElementById("change-"+n).value = "True";
}
function updateProfile(){
    var xmlhttp = ajaxRequest();
    xmlhttp.onreadystatechange=function(){
        if (xmlhttp.readyState==2){
            //sending request
        }if (xmlhttp.readyState==4){
            if (xmlhttp.status === 200){
                $("#settings-updated").attr("class","alert alert-success");//show ok updated
                $("#req-ok").text("Profile successfully updated!");
                hideProfile('name');hideProfile('num');hideProfile('email');hideProfile('college');hideProfile('degree');hideProfile('dormitory');
                $("#update-profile-submit").attr("class","hidden");
            }else if (xmlhttp.status === 400){
                $("#settings-not-updated").attr("class","alert alert-error");
                $("#req-error").text(xmlhttp.responseText);
            }
        }
    }
    var first="first="+encodeURIComponent(document.getElementById("name-first").value);
    var last="last="+encodeURIComponent(document.getElementById("name-last").value);
    var num="num="+encodeURIComponent(document.getElementById("input-num").value);
    var email="email="+encodeURIComponent(document.getElementById("input-email").value);
    var college="college="+encodeURIComponent(document.getElementById("input-college").value);
    var degree="degree="+encodeURIComponent(document.getElementById("input-degree").value);
    var dormitory="dormitory="+encodeURIComponent($("#form-dormitory option:selected").val())
    var params="";
    if (document.getElementById("change-name").value === "True")
        params+=first+"&"+last+"&";
    if (document.getElementById("change-num").value === "True")
        params+=num+"&";
    if (document.getElementById("change-email").value === "True")
        params+=email+"&";
    if (document.getElementById("change-college").value === "True")
        params+=college+"&";
    if (document.getElementById("change-degree").value === "True")
        params+=degree+"&";
    if (document.getElementById("change-dormitory").value === "True")
        params+=dormitory+"&";
    params+="submit=profile";//tells the server that this is an update to profile info
    xmlhttp.open("POST","/user/update",true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xmlhttp.send(params);
}
/* checks the url to determine defauls div to show*/
function checkUrl(){
    var index = location.href.indexOf("#");
    if (index === -1) return;   //default to profile
    var targ = location.href.substr(index,15);
    if (targ==="#")
        showUserHome();
    else if (targ==="#profile")
        showProfile();
    else if(targ==="#settings")
        showSettings();
    else if(targ==="#myconsign")
        showConsigned();
    else if(targ==="#myrequest")
        showRequested();
    else if(targ==="#help_consign")
        showHelp('selling');
    else if(targ==="#help_buying")
        showHelp('buying');   
}/* settings functions*/
function changePassword(){
    document.getElementById("form-change-password").className="";
    document.getElementById("edit-password").className="hidden";
    document.getElementById("privacy-form-submit").className="btn btn-success pull-right";
}
function updatePrivacy(){
    var xmlhttp = ajaxRequest();
    xmlhttp.onreadystatechange=function(){
        if (xmlhttp.readyState==2){
            //show saving
        }if (xmlhttp.readyState==4){ 
            if (xmlhttp.status==200){   //show success
                document.getElementById("settings-updated").className = "alert alert-success";
                document.getElementById("req-ok").innerText = "Settings successfully updated!";
                document.getElementById("privacy-form-submit").className = "hidden";
                hidePassword();
            }else if (xmlhttp.status=401){
                document.getElementById("settings-not-updated").className = "alert alert-error";
                document.getElementById("req-error").innerText = "Invalid Password";
            }else{  //show fail
                document.getElementById("settings-not-updated").className = "alert alert-error";
                document.getElementById("req-error").innerText = "An Error occurred while updating. Failed to update!";
            }           
        }
    }
    var old = "&old="+ encodeURIComponent(document.getElementById("old").value);
    var new1 = "&new="+ encodeURIComponent(document.getElementById("new").value);
    var new2 = "&new2="+ encodeURIComponent(document.getElementById("new2").value);
    var params = "submit=settings";
    
    if (old != "&old=") params += old+new1+new2;
    xmlhttp.open("POST","/user/update",true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xmlhttp.send(params);
}
function hidePassword(){
    document.getElementById("old").value = "";
    document.getElementById("new").value = "";
    document.getElementById("new2").value = "";
    document.getElementById("form-change-password").className = "hidden";
    document.getElementById("edit-password").className= " ";
}