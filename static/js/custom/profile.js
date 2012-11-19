function showProfile(){
    hideAll();
    $("#profile-info").show();
    $("#li_profile").attr("class","active");
}
function showConsigned(){
    hideAll();
    $("#li_consigned").attr("class","active");
    $("#user-consigned").show();
    loadConsigned();
}
function showRequest(){
    hideAll();
    $("#user-request").show();
    loadRequest();
}
function hideAll(){
    $("#profile-info").hide();
    $("#user-consigned").hide();
    $("#user-request").hide();
    $("#li_consigned").attr("class","");
    $("#li_profile").attr("class","");
    $("#li_requests").attr("class","");
}
function loadConsigned(){
    var xmlhttp = ajaxRequest();
    if (window.consiged_data != undefined)
        populateConsigned();
     xmlhttp.onreadystatechange=function(){
        if (xmlhttp.readyState==4){ 
            $("#consign-loading").hide();
            if (xmlhttp.status==200){
                var data = JSON.parse(xmlhttp.responseText);
                window.consiged_data = data;
                populateConsigned();
            }else{  
                $("#consign-result").text("Error");
            }
        }
    }
    var params = "u="+encodeURIComponent($("#username").val());
    xmlhttp.open("POST","/user/consiged",true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xmlhttp.send(params);
    $("#consign-loading").show();
}
function populateConsigned(){
    var data = window.consiged_data;
    /*consigned items*/
    var consiged = data.c;
    var markup="<br/>";
    if (consiged.length === 0)
        markup+="<b>NONE</b>";
    for (var i in consiged){
        var c = consiged[i];
        markup+= '<div class="row"><table class="span table-bordered table table-condensed" style="width:370px;margin-left:40px">'+
            '<tr><td style="width:90px">Title</td><td>'+c.title+'</td></tr>'+
            '<tbody id="b-'+i+'" style="display:none">'+
            '<tr><td>Author</td><td>'+c.author+'</td></tr>'+
            '<tr><td>Ask Price</td><td>Php '+c.ask_price+'</td></tr>'+
            '<tr><td>Price Posted</td><td>Php '+c.price+'</td></tr>'+  
            '<tr><td>Status</td><td>'+c.status.toProperCase()+'</td></tr>'+
            '<tr><td>Added by</td><td>'+c.added_by+'</td></tr>'+
            '<tr><td>Rating</td><td>'+c.rating+'</td></tr>'+
            '<tr><td>Posted</td><td>'+c.posted+'</td></tr>'+
            '<tr><td>ID</td><td>'+c.cid+'</td></tr>'+
        '</tbody></table><a href="javascript:void(0)" id="a-'+i+'"onclick="expand('+i+')" class="span"><i class="icon-plus"></i></a></div>';
    }
    $("#consign-result").html(markup);
    /*request to consign*/
    var req_consiged = data.rtc;
    markup="<br/>";
    if (req_consiged.length === 0)
        markup+="<b>NONE</b>";
    for (var i in req_consiged){
        var c = req_consiged[i];
        markup+= '<div class="row"><table class="span table-bordered table table-condensed" style="width:370px;margin-left:40px">'+
            '<tr><td style="width:90px">Title</td><td>'+c.title+'</td></tr>'+
            '<tbody id="bb-'+i+'" style="display:none">'+
            '<tr><td>Author</td><td>'+c.author+'</td></tr>'+
            '<tr><td>Status</td><td>'+c.status.toProperCase()+'</td></tr>'+
            '<tr><td>Posted</td><td>'+c.posted+'</td></tr>'+
            '<tr><td>ID</td><td>'+c.crid+'</td></tr>'+
        '</tbody></table><a href="javascript:void(0)" id="aa-'+i+'"onclick="expand2('+i+')" class="span"><i class="icon-plus"></i></a></div>';
    }
    $("#request-consign-result").html(markup);
}
function expand(num){
    $("#b-"+num).slideDown(200);
    $("a#a-"+num).hide();
}
function expand2(num){
    $("#bb-"+num).slideDown(200);
    $("a#aa-"+num).hide();
}
function loadRequest(){
    var xmlhttp = ajaxRequest();
    if (window.request_data != undefined)
        populateRequests();
     xmlhttp.onreadystatechange=function(){
        if (xmlhttp.readyState===4){
            $("#request-loading").hide();
            if (xmlhttp.status===200){
                var data = JSON.parse(xmlhttp.responseText);
                window.request_data = data;
                populateRequests();
            }else{
                $("#request-result").text("Error");
            }
        }
    }
    var params = "u="+encodeURIComponent($("#username").val());
    xmlhttp.open("POST","/user/requests",true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xmlhttp.send(params);
    $("#request-loading").show();
}
function populateRequests(){
    var data = window.request_data;
    var markup="<br/>";
    for (var i in data){
        var c = data[i];
        markup+= '<div class="row"><table class="span table-bordered table table-condensed" style="width:370px;margin-left:40px">'+
            '<tr><td style="width:90px">Title</td><td>'+c.title+'</td></tr>'+
            '<tbody id="b-'+i+'" style="display:none">'+
            '<tr><td>Author</td><td>'+c.author+'</td></tr>'+
            '<tr><td>Max Price</td><td>Php '+c.max_price+'</td></tr>'+
            '<tr><td>Min Rating</td><td>'+c.min_rating+'</td></tr>'+  
            '<tr><td>Status</td><td>'+c.status.toProperCase()+'</td></tr>'+
            '<tr><td>Posted</td><td>'+c.posted+'</td></tr>'+
            '<tr><td>ID</td><td>'+c.rid+'</td></tr>'+
        '</tbody></table><a href="javascript:void(0)" id="a-'+i+'"onclick="expand('+i+')" class="span"><i class="icon-plus"></i></a></div>';
    }
    $("#request-result").html(markup);
}