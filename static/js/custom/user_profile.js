/*  user profile page scripts */

/*functions to navigate user profile */
function showProfile(){
    hideAll();
    document.getElementById("profile-info").className = "row";
    document.getElementById("li_profile").className = "active";
}
function showSettings(){
    hideAll();
    document.getElementById("privacy-settings").className = "";
    document.getElementById("li_settings").className = "active";   
}
function showUserHelp(){
    var h = document.getElementById("help-options");
    if (h.className === "nav nav-list"){
        hideUserHelp();
    }else{
        h.className = "nav nav-list";
        document.getElementById("user-help").className="";
    }
}
function hideUserHelp(){
    document.getElementById("help-options").className="hidden";
    document.getElementById("user-help").className="hidden";
    document.getElementById("li_help-buy").className="";
    document.getElementById("li_help-sell").className="";
    document.getElementById("buying-help").className="hidden";
    document.getElementById("selling-help").className="hidden";
}
function showHelp(help){
    hideAll();
    showUserHelp();
    var li_help_buy = document.getElementById("li_help-buy");
    var li_help_sell = document.getElementById("li_help-sell");
    var buy_help = document.getElementById("buying-help");
    var sell_help = document.getElementById("selling-help");
    buy_help.className = "hidden";
    sell_help.className = "hidden";
    li_help_sell.className = "";
    li_help_buy.className = "";
    if (help === "selling"){
        li_help_sell.className = "active";
        sell_help.className = "";
    }else if (help === "buying"){
        li_help_buy.className = "active";
        buy_help.className = "";
    }
}
function showSellOrder(){
    hideAll();
    document.getElementById("user-sell-orders").className = "";
    document.getElementById("li_sell_order").className = "active";
    var loaded = document.getElementById("sell-loaded").value;
    //prevent loading of orders repeatedly
    if (!eval(loaded)){
        loadOrder("sell");
        document.getElementById("sell-loaded").value = "true";
    }
}
function showBuyOrder(){
    hideAll();
    document.getElementById("user-buy-orders").className = "";
    document.getElementById("li_buy_order").className = "active";
    var loaded = document.getElementById("buy-loaded").value;
    //prevent loading of orders repeatedly
    if (!eval(loaded)){
        loadOrder("buy");
        document.getElementById("buy-loaded").value = "true";
    }
}
function showSendMessage(){
    hideAll();
    document.getElementById("send-message").className = "";
    document.getElementById("li_send_message").className="active";
}
function showInbox(){
    hideAll();
    document.getElementById("user-inbox").className = "";
    document.getElementById("li_inbox").className="active";
}
function hideAll(){//hide all divs in profile
    document.getElementById("profile-info").className = "hidden";
    document.getElementById("privacy-settings").className = "hidden";
    document.getElementById("user-help").className = "hidden";
    document.getElementById("user-sell-orders").className = "hidden";
    document.getElementById("user-buy-orders").className = "hidden";
    document.getElementById("user-inbox").className = "hidden";
    document.getElementById("send-message").className = "hidden";
    document.getElementById("send-message-complete").className = "hidden";
    document.getElementById("li_profile").className = "";
    document.getElementById("li_settings").className = "";
    document.getElementById("li_sell_order").className = "";
    document.getElementById("li_buy_order").className = "";
    document.getElementById("li_send_message").className="";
    document.getElementById("li_inbox").className="";
    document.getElementById("settings-updated").className="hidden";
    document.getElementById("settings-not-updated").className="hidden";
    hideUserHelp();
}
/* functions for nav in browse page */
function showNav(){//show nav for browsing
    document.getElementById("imgHide").className="hidden";
    document.getElementById("browsed-div").className="span8 well";
    document.getElementById("browsed-title").className="span9";
    document.getElementById("browseNav").className="";
    $("#results-nav").removeClass();
    $("#results-nav").addClass("span9 offset3");
}
function hideNav(){//hide nav for browsing
    document.getElementById("imgHide").className="";
    document.getElementById("browsed-div").className="span11-5 well";
    document.getElementById("browsed-title").className="span12";
    document.getElementById("browseNav").className="hidden";
    $("#results-nav").removeClass();
}
/*functions to change user information*/
function changeName(){
    var n = "name";
    changeGeneral(n);
}
function changeEmail(){
    var n = "email";
    changeGeneral(n);
}
function changeNum(){
    var n = "num";
    changeGeneral(n);
}
function changeCollege(){
    var n = "college";
    changeGeneral(n);
}
function changeDegree(){
    var n = "degree";
    changeGeneral(n);
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

function title(string){
    return string.charAt(0).toUpperCase() + string.slice(1);
}
function changePassword(){
    document.getElementById("form-change-password").className="";
    document.getElementById("edit-password").className="hidden";
    document.getElementById("privacy-form-submit").className="btn btn-success pull-right";
}
function changePrivacyContact(){
    var n = "contact";
    changeGeneralPrivacy(n)
}
function changePrivacyCollege(){
    var n = "college";
    changeGeneralPrivacy(n)
}
function changeGeneralPrivacy(n){
    document.getElementById("href-"+n+"2").setAttribute("onclick","hideSetting('"+n+"')");
    document.getElementById("form-privacy-"+n).className="";
    document.getElementById("user-privacy-"+n).className="hidden";
    document.getElementById("edit-privacy-"+n).innerText=" ok";
    document.getElementById("privacy-form-submit").className="btn btn-success pull-right";
}//compliment of change general privacy
function hideSetting(n){
    var p = document.getElementsByName("privacy-"+n)[0];
    document.getElementById("edit-privacy-"+n).innerText=" edit";
    document.getElementById("form-privacy-"+n).className = "hidden";
    document.getElementById("user-privacy-"+n).className = "";
    document.getElementById("user-privacy-"+n).innerText = p.options[p.selectedIndex].innerText;
    document.getElementById("href-"+n+"2").setAttribute("onclick","changePrivacy"+title(n)+"()");
}
/*  ajax to update user privacy*/
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
                hideSetting("college");
                hideSetting("contact");
            }else if (xmlhttp.status=401){
                document.getElementById("settings-not-updated").className = "alert alert-error";
                document.getElementById("req-error").innerText = "Invalid Password";
            }
            else{  //show fail
                document.getElementById("settings-not-updated").className = "alert alert-error";
                document.getElementById("req-error").innerText = "An Error occurred while updating. Settings failed to update!";
            }           
        }
    }
    var pcon = document.getElementsByName("privacy-contact")[0];
    var pcol = document.getElementsByName("privacy-college")[0];
    var priv_contact = "privacy-contact="+encodeURIComponent(pcon.options[pcon.selectedIndex].value);
    var priv_college = "&privacy-college="+encodeURIComponent(pcol.options[pcol.selectedIndex].value);
    var old = "&old="+ encodeURIComponent(document.getElementById("old").value);
    var new1 = "&new="+ encodeURIComponent(document.getElementById("new").value);
    var new2 = "&new2="+ encodeURIComponent(document.getElementById("new2").value);
    var params = priv_contact + priv_college +"&submit=settings";
    
    if (old != "&old=") params += old+new1+new2;
    xmlhttp.open("POST","/user/update",true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xmlhttp.send(params);
}
/*  verifies if the input of the user is valid (update password)*/
function checkValid(){
    var new1 = document.getElementById("new").value;
    var new2 = document.getElementById("new2").value;
    if (new1 != new2){
        document.getElementById("unmatch-pass").className = "label label-warning";
        document.getElementById("privacy-form-submit").className = "btn btn-success pull-right disabled"
    }else{
        document.getElementById("unmatch-pass").className = "hidden";
        document.getElementById("privacy-form-submit").className = "btn btn-success pull-right"
    }
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
                document.getElementById("settings-updated").className = "alert alert-success";//show ok updated
                document.getElementById("req-ok").innerText = "Profile successfully updated!";
                hideProfile('name');hideProfile('num');hideProfile('email');hideProfile('college');hideProfile('degree');
                document.getElementById("update-profile-submit").className = "hidden";
            }else if (xmlhttp.status === 400){
                document.getElementById("settings-not-updated").className = "alert alert-error";
                document.getElementById("req-error").innerText = xmlhttp.responseText;
            }
        }
    }
    var first="first="+encodeURIComponent(document.getElementById("name-first").value);
    var last="last="+encodeURIComponent(document.getElementById("name-last").value);
    var num="num="+encodeURIComponent(document.getElementById("input-num").value);
    var email="email="+encodeURIComponent(document.getElementById("input-email").value);
    var college="college="+encodeURIComponent(document.getElementById("input-college").value);
    var degree="degree="+encodeURIComponent(document.getElementById("input-degree").value);
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
    params+="submit=profile";//tells the server that this is an update to profile info
    xmlhttp.open("POST","/user/update",true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xmlhttp.send(params);
}
//more info click in book info
function moreInfo(){
    var inf = document.getElementsByName("info");
    for (var i=0;i< inf.length;i++){
        inf[i].className = "";
    }
    document.getElementById("more-info").onclick="";
    document.getElementById("icon-more-info").className = "icon-ok";
}
function loadOrder(order){
    var xmlhttp = ajaxRequest();
    xmlhttp.onreadystatechange=function(){
        if (xmlhttp.readyState==2){
            document.getElementById(order+"-loading").className = "";
        }if (xmlhttp.readyState==4 && xmlhttp.status === 200){
            document.getElementById(order+"-loading").className = "hidden";
            var jdata = JSON.parse(xmlhttp.responseText);
                var html="";
            for (var i=0;i<jdata.length;i++){
                var output = '<div class="browsed"><div><table>';
                var data = JSON.parse(jdata[i]);
                output+= "<tr><td class='tdmarg'>Title</td><td><a href='/info?book=" + 
                data.bid.toString() + "'>" + data.title.substr(0,33)+"</a></td></tr>" +
                "<tr><td>Author</td><td>" + data.author +"</td></tr>" +
                "<tfoot class='hidden' id='"+order+"-info-item"+i.toString()+"'>";
                if (data.isbn != "")
                    output+="<tr><td>ISBN</td><td> " + data.isbn + "</td></tr>";
                output+="<tr><td>Price</td><td> Php " + data.price + "</td></tr>" +
                "<tr><td>Rating</td><td> " + data.rating + "/5</td></tr>" +
                "<tr><td>Posted</td><td> " + data.posted + "</td></tr>";
                if (data.comments!=null)
                    output+= "<tr><td>Comments</td><td> " + data.comments + "</td></tr>";
                output+= "</tfoot></table><a href='#' onclick=\"showItemInfo('"+order+"',"+i.toString()+")\" id='"+order+"-link"+i.toString()+"'>show more</a>"+
                "</div></div>";
                html+=output;
            }
            document.getElementById(order+"-result").innerHTML = html;
        }       
    }
    var username = "user="+encodeURIComponent(document.getElementById("user_username").value);
    var order2 = "&type="+order;
    var params = username+order2;
    xmlhttp.open("POST","/user/orders",true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xmlhttp.send(params);
}
//type is either sell or buy
function showItemInfo(type,id){
    document.getElementById(type+"-info-item"+id).className='';
    document.getElementById(type+"-link"+id).className='hidden';
}
//function that send message ajax
function sendMessage(){
    var xmlhttp = ajaxRequest();
    xmlhttp.onreadystatechange=function(){
        if (xmlhttp.readyState==2){
            showLoading();
        }if (xmlhttp.readyState==4 && xmlhttp.status==200){
            showMessageSent();
        }
    }
    var title = encodeURIComponent(document.getElementById("title").value);
    var message = encodeURIComponent(document.getElementById("text-message").value);
    var logged = document.getElementById("logged_in").value;
    var to = encodeURIComponent(document.getElementById("to").value);
    //the request to be sent
    var params = "title="+title+"&message="+message+"&to="+to;
    
    if (logged === "True"){
        params += "&from="+encodeURIComponent(document.getElementById("from").value);
    }else{
        params = params+ "&guest-name="+ encodeURIComponent(document.getElementById("guest-name").value);
        params = params+ "&guest-email="+ encodeURIComponent(document.getElementById("guest-email").value);
        params = params+ "&guest-contact="+ encodeURIComponent(document.getElementById("guest-contact").value);//
    }
    xmlhttp.open("POST","/user/sendmessage",true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xmlhttp.send(params);
}
function showLoading(){
    document.getElementById("send-message").className = "hidden";
    document.getElementById("send-message-loading").className = "";
}
function showMessageSent(){
    document.getElementById("send-message-complete").className = "";
    document.getElementById("send-message").className="hidden";
    document.getElementById("send-message-loading").className = "hidden";
}
function hidePassword(){
    document.getElementById("old").value = "";
    document.getElementById("new").value = "";
    document.getElementById("new2").value = "";
    document.getElementById("form-change-password").className = "hidden";
    document.getElementById("edit-password").className= " ";
}
