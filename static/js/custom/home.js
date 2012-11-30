function hideAll(callback){
    $("div#home").hide();
    $("div#search").hide();
    $("div#userprofile").hide();
    $("div#setting").hide();
    $("div#consign").hide();
    $("div#request").hide(callback);
    $("li#li_home").attr("class","");
    $("li#li_search").attr("class","");
    $("li#li_aids").attr("class","");
    $("li#li_setting").attr("class","");
    $("li#li_userprofile").attr("class","");
    $("li#li_consign").attr("class","");
    $("li#li_request").attr("class","");
    $("li#li_help-consign").attr("class","");
    $("li#li_help-buying").attr("class","");
}
function showUserHome(){
    if (window.location.pathname.indexOf("/home")===-1)
        window.location.replace("/home")
}
function showSearch(){
    if (window.location.pathname.indexOf("/home")===-1)
        window.location.replace("/home#search")
    hideAll();
    show("search");
}
function showProfile(){
    if (window.location.pathname.indexOf("/home")===-1)
        window.location.replace("/home#profile")
    hideAll();
    show("userprofile");
}
function showSettings(){
    if (window.location.pathname.indexOf("/home")===-1)
        window.location.replace("/home#settings")
    hideAll();
    show("setting");
}
function showConsigned(){
    if (window.location.pathname.indexOf("/home")===-1)
        window.location.replace("/home#myconsign")
    hideAll();
    show("consign");
    loadConsigned();
}
function showRequested(){
    if (window.location.pathname.indexOf("/home")===-1)
        window.location.replace("/home#myrequest")
    hideAll();
    show("request");
    loadRequested();
}
function show(targ){
    $("div#"+targ).slideDown(500);
    $("#li_"+targ).attr("class","active");
}
/* functions to request from server data about consignment*/
function loadConsigned(){
    var xmlhttp = ajaxRequest();
    xmlhttp.onreadystatechange=function(){
        if (xmlhttp.readyState===2){    
            $("#consign-loading").show();
        }else if(xmlhttp.readyState===4){
            $("#consign-loading").hide();
            if (xmlhttp.status===200){
                var data = JSON.parse(xmlhttp.responseText);
                populateConsigned(data);
            }else if (xmlhttp.status === 400){//no data
                $("div#consign-result").html("<span style='font-size:15px'>You have no consigned books</span>")//. Click here to <a href=''>learn more about consigning </a>");
                $("div#consign-request").html("<span style='font-size:15px'>You have not requested to consign any book yet</span>");
            }else{
                $("#consign-result").text("Failed to fetch data. Please try again in a while.");
            }
        }
    }
    var params="req=consign";
    xmlhttp.open("POST","/user/orders",true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xmlhttp.send(params);
}
function populateConsigned(data){
    var markup = "";
    var books = data.books;
    if (books.length===0){
        $("div#consign-result").html("You have no consigned books.");
    }else{
        for (var raw in books){
            var cbook = books[raw];
            markup += '<table class="table table-condensed table-bordered" style="width:350px;margin-left:40px;margin-bottom:0;margin-top:20px">'+
                '<tr><td style="width:80px">Title</td><td>'+cbook.title+'</td></tr>'+
                '<tbody id="cbody-'+raw+'" class="hidden">'+
                '<tr><td>Author</td><td>'+cbook.author+'</td></tr>'+
                '<tr><td>Ask Price</td><td>'+cbook.ask_price+'</td></tr>'+
                '<tr><td>Rating</td><td>'+cbook.rating+'</td></tr>'+
                '<tr><td>Status</td><td>'+cbook.status.toProperCase()+'</td></tr>'+
                '<tr><td>Date Posted</td><td>'+cbook.posted+'</td></tr>'+
                '</tbody></table><a href="#" style="margin-left:350px;" id="cex-'+raw+
                '"onclick="showConDetails('+"'c'"+','+raw+')">expand</a></div>';
        }
        $("div#consign-result").html(markup);
    }
    var req = data.req;
    if (req.length===0){
        $("div#consign-request").html("You have not requested to consign any book.");
    }else{
        markup="";
        for (var raw in req){
            var rbook = req[raw];
            markup += '<table class="table table-condensed table-bordered" style="width:350px;margin-left:40px">'+
                '<tr><td style="width:80px">Title</td><td>'+rbook.title+'</td></tr>'+
                '<tbody id="xbody-'+raw+'" class="hidden">'+
                '<tr><td>Author</td><td>'+rbook.author+'</td></tr>'+
                '<tr><td>Status</td><td>'+rbook.status.toProperCase()+'</td></tr>'+
                '<tr><td>Date Posted</td><td>'+rbook.posted+'</td></tr>'+
                '</tbody></table><a href="#" style="margin-left:350px;" id="tex-'+raw+
                '"onclick="showConDetails('+"'x'"+','+raw+')">expand</a></div>';
        }
        $("div#consign-request").html(markup);   
    }
}
function showConDetails(t,num){
    $("#"+t+"body-"+num).slideDown(300);
    $("#"+t+"ex-"+num).hide();
}
function loadRequested(){
    var xmlhttp = ajaxRequest();
    xmlhttp.onreadystatechange=function(){
        if (xmlhttp.readyState===2){
            $("#request-loading").show();
        }else if(xmlhttp.readyState===4){
            $("#request-loading").hide();
            if (xmlhttp.status===200){
                var data = JSON.parse(xmlhttp.responseText);
                populateRequested(data);
            }else if (xmlhttp.status === 400){
                $("#request-response").html("You have not requested any item. Click here to <a href='/book/request'>request for an item</a>");
                $("#request-response").show();
            }else{
                $("#request-response").text("Failed to fetch data. Please try again in a while.");
                $("#request-response").show();
            }
        }
    }
    var params="req=request";
    xmlhttp.open("POST","/user/orders",true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xmlhttp.send(params);
}
function populateRequested(data){
    var markup = "";
    window.test2 = data;
    for (var raw in data){
        var rbook = data[raw];
        markup += '<div style="margin-top:20px"><table class="table table-condensed table-bordered" style="width:350px;margin-left:40px;margin-bottom:0;margin-top:20px">'+
            '<tr><td style="width:80px">Title</td><td>'+rbook.title+'</td></tr>'+
            '<tr><td>Author</td><td>'+rbook.author+'</td></tr>'+
            '<tbody id="rbody-'+raw+'" class="hidden">';
            if (rbook.ask_price)
                markup+= '<tr><td>Max Price</td><td>'+rbook.ask_price+'</td></tr>'+
                '<tr><td>Min Rating</td><td>'+rbook.rating+'</td></tr>';
            markup+='<tr><td>Status</td><td>'+rbook.status.toProperCase()+'</td></tr>'+
            '<tr><td>Date Posted</td><td>'+rbook.posted+'</td></tr>'+
            '</tbody></table><a href="#" style="margin-left:350px;" id="ex-'+raw+
                '"onclick="showReqDetails('+raw+')">expand</a></div>';
    }
    $("div#request-result").html(markup);
}
function showReqDetails(num){
    $("#rbody-"+num).slideDown(300);
    $("#ex-"+num).hide();
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
window.onload = checkUrl();