function ajaxRequest(){
    var xmlhttp;
    if (window.XMLHttpRequest)// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
    else// code for IE6, IE5
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    return xmlhttp;
}
//gets the url params
function parseURLParams(){
    if (location.search != ""){
        var params = {};
        var x = location.search.substr(1).split(";")
        for (var i=0; i<x.length; i++){
            var y = x[i].split("=");
            params[y[0]] = y[1];
        }
        return params;
    }   
}
function toggleHelp() {    
    var pro = document.getElementById("sellProcedure").style.display;
    
    if (pro != "none"){
        document.getElementById("sellProcedure").style.display = "none";
        document.getElementById("conditionHelp").style.display = "block";
    }else{
        document.getElementById("sellProcedure").style.display = "block";
        document.getElementById("conditionHelp").style.display = "none";
    }
}
function setCondition(value){
    if (value >0 && value < 6){
        document.getElementById("condition").value = value;
        clearStars();
        for (var s=1;s<=value;s++){
            document.getElementById("star".concat(s.toString())).src = "/static/images/gold_star.png";
        }
    }
}
function clearStars(){
    for (var s=1;s<=5;s++)
        document.getElementById("star".concat(s.toString())).src = "/static/images/white_star.png";
}
function changePass(){
    document.getElementById("cplink").style.display = "none";
    document.getElementById("change-user-pass").style.display = "block";
}
function changeView(){
    document.getElementById("vslink").style.display = "none";
    document.getElementById("change-view-settings").style.display = "block"
}
function clearViewRadio(){
    document.getElementById("view-admin").checked = false;
    document.getElementById("view-users").checked = false;
    document.getElementById("view-everyone").checked = false;
}
function checkRadio(hello){
    clearViewRadio();
    document.getElementById("view-"+hello).checked = true;
}
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
    document.getElementById("browseNav").className="";
}
function hideNav(){//hide nav for browsing
    document.getElementById("imgHide").className="";
    document.getElementById("browsed-div").className="span11-5 well";
    document.getElementById("browseNav").className="hidden";
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
    document.getElementById("href-"+n).setAttribute("onclick","change"+title(n)+"()");
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
//function to open book page in browse
function openBookPage(book_id){
    location.href="/info?book="+book_id;
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

//manipulate html and populate stats
function showStats(json){
    var jdata = JSON.parse(json)
    document.getElementById("total-listed").innerText = jdata.listings;
    if (jdata.totalSold>0)
        document.getElementById("total-sold").innerText = jdata.totalSold+" books";
    else
        document.getElementById("total-sold").innerText = "None yet";
    document.getElementById("ave-price").innerText = "Php "+jdata.avePrice;
    if (jdata.newPrice > 0)
        document.getElementById("new-price").innerText = "Php "+jdata.newPrice;
    else
        document.getElementById("new-price").innerText = "No Data";
    document.getElementById("icon-show-stats").className = "icon-ok";
}
//get the stats for a book
function getStats(bid){
    var xmlhttp = ajaxRequest();
    xmlhttp.onreadystatechange=function(){
        if (xmlhttp.readyState==2){
            document.getElementById("stats-loading").className = "span4 alert alert-success";
        }if (xmlhttp.readyState==4 ){
            if (xmlhttp.status === 200){
                document.getElementById("stats-loading").className = "hidden";
                document.getElementById("book-stats").className = ""
                showStats(xmlhttp.responseText);
            }else{
                document.getElementById("stats-loading").className = "hidden";
                document.getElementById("show-error-stats").className="span4 alert alert-error";
            }
        }
    }
    var params = "book="+bid;
    xmlhttp.open("POST","/item/book/stats",true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xmlhttp.send(params);
}

function setSortOrderVal(value){
    window.order = value;
    document.getElementById("li-sort-asc").className="";
    document.getElementById("li-sort-desc").className="";
    document.getElementById("li-sort-"+value).className="active";
}

function requestSellers(sort_by,def){
    document.getElementById("loading").className = "";
    def = typeof def !== 'undefined' ? def : true;  //if def(ault) is null, set to true
    if (document.getElementById("li-sort-"+sort_by).className === "active" && def===true)
        return;
    //set default values
    if (def)
        if (sort_by==="price")
            setSortOrderVal("asc");
        else
            setSortOrderVal("desc");
    var order = window.order;
    if (order != "asc" && order != "desc")
        order="desc";
    var xmlhttp = ajaxRequest();
    bid = parseURLParams()["book"];
    xmlhttp.onreadystatechange=function(){
        if (xmlhttp.readyState === 2){
            document.getElementById("loading").className = "";
            document.getElementById("load-error").className="hidden";
        }if (xmlhttp.readyState === 4){
            if (xmlhttp.status === 200){
               document.getElementById("loading").className = "hidden";
               document.getElementById("load-error").className="hidden";
               populateUsers(JSON.parse(xmlhttp.responseText));
               displayTab(sort_by);
            }else{
                document.getElementById("load-error").className="";
                document.getElementById("loading").className = "hidden";
            }
        }
    }
    var params= "bid="+encodeURIComponent(bid);
    params+= "&sort="+encodeURIComponent(sort_by);
    params+= "&order="+order;
    if (window.offset)
        params+="&offset="+encodeURIComponent(window.offset);
    xmlhttp.open("POST","/info",true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.send(params);
}
//fills the list of sellers for a book
function populateUsers(jdata){
    window.jdata = jdata;

    html = "";
    for (var num in window.jdata.books){
        var book = JSON.parse(window.jdata.books[num]);
        var user = JSON.parse(book.user);
        var markup = '<div id="item-info" class="row span5" style="position:relative;padding:14px 0px">\n' +
            '<span class="thumbnail" style="margin:0 15px;width:105px;">\n' +
            '<a class="thumbnail" href="/user?usr=' + user.username + '"><img src="' +user.image + '" class="img100"></a></span>\n'+
            '<table class="table table-condensed" style="position:absolute;top:15px;left:140px;">\n' +
            '<tr><td>Seller</td><td><a href="/user?usr=' + user.username + '">' + user.username + '</a></td></tr>\n' +
            '<tr><td>Book Rating</td><td><a class=\"stars\" rel=\"popover\" data-content=\"' + getDesc(book.rating).toString() +
            "\" data-original-title=\""+ getDescTitle(book.rating)+ "\">" + generateStars(book.rating)+ '</a></td></tr>\n' +
            '<tr><td>Price</td><td>Php '+ book.price +'</td></tr>';
        if (book.comment !=null)
            markup+= '<tr><td>Comments</td><td>'+book.comment+'</td></tr>';
        markup+= '<tr><td>Date Posted</td><td>'+ book.posted +'</table></div>';
        html += markup;
    }
    window.listing_page = jdata.page;
    document.getElementById("sellers-list").innerHTML = html;
    document.getElementById("display-info").innerText = "Showing "+ (jdata.offset+1).toString() + "-"+(jdata.offset+jdata.limit).toString()+" of " + jdata.total.toString();
    document.getElementById("pagination").innerHTML = generatePaginationMarkup();
    $("a.stars").popover();
}
function getDesc(rating){
    if (rating===1)
        return 'We advice that you find other alternatives';
    else if (rating===2)
        return 'Some pages torn<br/>not well maintained';
    else if (rating===3)
        return 'More than 1 year used<br/>Some edges torn';
    else if (rating===4)
        return 'Taken good care<br/>No torn pages/edges<br/>Has never been wet<br/>Well maintained';
    else if (rating===5)
        return 'Brand new quality<br/>Less than 2 months used';
}

function getDescTitle(rating){
    if (rating===1)
        return 'Abused';
    else if (rating===2)
        return 'Poor';
    else if (rating===3)
        return 'Average';
    else if (rating===4)
        return 'Slightly Used';
    else if (rating===5)
        return 'Good as New';
}
function generateStars(rating){
    var markup = "", i=0;
    for (i=0; i<rating; i++)
        markup+= '<img class="rating-star14" src="/static/images/gold_star.png">';
    for (i=0; i<5-rating;i++)
        markup+= '<img class="rating-star14" src="/static/images/white_star.png">';
    return markup;
}
//book info 
function displayTab(sort_by){
    window.sortBy = sort_by;
    document.getElementById("li-sort-posted").className = "";
    document.getElementById("li-sort-rating").className = "";
    document.getElementById("li-sort-price").className = "";
    document.getElementById("li-sort-"+sort_by).className = "active";
}
function reorder(order){
    if (window.order === order)
        return;
    activate(order)
    requestSellers(window.sortBy,false);
}

//asc desc setting of active
function activate(order){
    if (window.order === order)
        return;
    window.order = order;
    document.getElementById("li-sort-asc").className = "";
    document.getElementById("li-sort-desc").className = "";
    document.getElementById("li-sort-"+order).className = "active";
}
//generate pagination for listings
function generatePaginationMarkup(){
    var i=0;
    var limit=5;
    var data = window.jdata

    //calculate the number of pages
    var pages = Math.ceil(data.total / limit);
    window.pages = pages;
    //current page
    var page = window.listing_page;

    var markup = "<ul id=\"pagination\"><li";
    if (page === 1)
        markup+= " class=\"disabled\"";
    markup+= "><a href=\"javascript:void(0)\" onclick=\"gotoPrevPage()\">«</a></li>";
    for (i=1;i<=pages;i++){
        markup+= "<li";
        if (i===page)
            markup+=  " class=\"active\"";
        markup+="><a href=\"javascript:void(0)\" onclick=\"gotoPage("+ i.toString() +")\">"+ i.toString() + "</a></li>";
    }
    markup+="<li";
    if (page===pages)
        markup+= " class=\"disabled\"";
    markup+="><a href=\"javascript:void(0)\" onclick=\"gotoNextPage()\">»</a></li></ul>";
    return markup;
}

function gotoPage(page){
    if (window.listing_page === page)
        return;

    var limit = 5;
    window.offset = (page-1) * limit;
    requestSellers(window.sortBy,false);
}
function gotoNextPage(){
    page = window.listing_page+1;
    if (page > window.pages) return;
    gotoPage(page);
}
function gotoPrevPage(){
    page = window.listing_page-1;
    if (page < 1) return;
    gotoPage(page);   
}

/* browse scripts */
function requestLibrary(page){
    var xmlhttp = ajaxRequest();
    xmlhttp.onreadystatechange=function(){
        if (xmlhttp.readyState === 2){
            document.getElementById("loading").className = "";
            document.getElementById("load-error").className="hidden";
        }if (xmlhttp.readyState === 4){
            if (xmlhttp.status === 200){
                document.getElementById("loading").className = "hidden";
                document.getElementById("load-error").className="hidden";
                var jdata=JSON.parse(xmlhttp.responseText);
                populateResults(jdata);
                window.pages = jdata.pages;
                window.page = jdata.page;
            }else{
                document.getElementById("load-error").className="";
                document.getElementById("loading").className = "hidden";
            }
        }
    }
    var params = "page="+encodeURIComponent(page);
    xmlhttp.open("POST","/browse");
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.send(params);
}

function noImage(){
    return '<div class="result-img" alt="No image available" title="no image available"><div style="height:25px"></div>'+
            '<label class="label label-success" style="text-align:center;">No Image<br/>Available</label></div>';
}

function getDescription(desc){
    if (!desc)
        return "No Description available";
    return desc
}

function modTitle(title){
    if (title.length>=28)
        return title.substr(0,25)+"...";
    return title;
}
function modAuthor(author){
    if (!author)
        return "";
    return author;
}
function populateResults(jdata){
    var i=0;
    var books = JSON.parse(jdata.books);
    var buySell = JSON.parse(jdata.buySell);
    var pages = jdata.pages;
    window.page = jdata.page;

    var html="";
    for (i=0;i<books.length;i++){
        book = JSON.parse(books[i]);
        var markup = '<div class="browsed"><div class="row-fluid">' +
        '<span class="browsed-img"><a href="/info?book='+book.key+'" class="book-image">';
        if (book.image==null)
            markup += noImage();
        markup+= '</a></span><div class="browsed-info"><table>'+
            '<tr><td class="tdmarg"><img src="/static/images/title.png" title="Book Title" class="icon16px"></td>'+
            '<td><a href="javascript:void(0)" class="link" rel="popover" onclick="openBookPage('+book.key+
            ')" data-content=\'<b>Author: </b><font color="#049cdb">'+modAuthor(book.author)+'</font><br/>'+
            '<div style="margin-top:5px;">' +getDescription(book.description)+ '</div>\''+
            ' data-original-title="'+book.title+'">'+modTitle(book.title)+'</a></td></tr>'+
            '<tr><td><img src="/static/images/author.png" title="Author" class="icon16px"></td><td>'+
            modAuthor(book.author) +'</td></tr>'+'</table><span class="browsed-stats">'+
            '<span title="Buying"><i class="icon-shopping-cart"></i>'+buySell[i][0].toString()+'</span>'+
            '<span title="Selling"><i class="icon-book"></i>'+buySell[i][1].toString()+'</span></span></div></div></div>';
        html+=markup;
    }
    $("#browsed-div").html(html);
    $(".link").popover();
}
function generateBrowsePaginationMarkup(){
    var i=0;
    var limit=15;
    var data = window.jdata

    //calculate the number of pages
    var pages = Math.ceil(data.total / limit);
    window.pages = pages;
    //current page
    var page = window.listing_page;

    var markup = "<ul id=\"pagination\"><li";
    if (page === 1)
        markup+= " class=\"disabled\"";
    markup+= "><a href=\"javascript:void(0)\" onclick=\"gotoPrevPage()\">«</a></li>";
    for (i=1;i<=pages;i++){
        markup+= "<li";
        if (i===page)
            markup+=  " class=\"active\"";
        markup+="><a href=\"javascript:void(0)\" onclick=\"gotoPage("+ i.toString() +")\">"+ i.toString() + "</a></li>";
    }
    markup+="<li";
    if (page===pages)
        markup+= " class=\"disabled\"";
    markup+="><a href=\"javascript:void(0)\" onclick=\"gotoNextPage()\">»</a></li></ul>";
    return markup;
}