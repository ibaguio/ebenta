/*  book info scripts
    script used to update and modify info on the 
    book info pages */

//ajax request
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

    if (sort_by !== window.sortBy)
        window.offset = 0;

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
            document.getElementById("loading").className = "hidden";
            document.getElementById("load-error").className="hidden";
            if (xmlhttp.status === 200){
                populateUsers(JSON.parse(xmlhttp.responseText));
                displayTab(sort_by);
                $("#sorting-nav").show();
                $("#results-nav").show();
            }else if (xmlhttp.status === 401){//no listings for this item11
                $("#sorting-nav").hide();
                $("#results-nav").hide();
                $("#no-results").removeClass();
            }else{
                $("#sorting-nav").show();
                document.getElementById("load-error").className="";
                $("#results-nav").hide();
            }
        }
    }
    var params= "bid="+encodeURIComponent(bid);
    params+= "&sort="+encodeURIComponent(sort_by);
    params+= "&order="+order;
    if (window.offset)
        params+="&offset="+encodeURIComponent(window.offset);
    xmlhttp.open("POST","/book/info",true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.send(params);
}

//fills the list of sellers for a book
function populateUsers(jdata){
    window.jdata = jdata;
    $("#sellers-list").hide();
    html = "";
    for (var num in window.jdata.books){
        var book = JSON.parse(window.jdata.books[num]);
        var user = JSON.parse(book.user);
        var markup = '<div id="item-info" class="row span5" style="position:relative;padding:14px 0px">\n' +
            '<span class="thumbnail" style="margin:0 15px;width:105px;">\n' +
            '<a class="thumbnail" href="/user?usr=' + user.username + '"><img src="' +user.image + '" class="img100"></a></span>\n'+
            '<table class="table table-condensed" style="position:absolute;top:15px;left:140px;">\n' +
            '<tr><td>Seller</td><td><a href="/user?usr=' + user.username + '">' + user.username + '</a></td></tr>\n' +
            '<tr><td>Book Rating</td><td><a class=\"stars\" rel=\"popover\" data-content=\"' + getDesc(book.rating).toString();
            if (book.comment !== null)
                 markup+= "<br/><br/><b>Seller's Comment:</b><p>" + book.comment + "</p>";
            markup += "\" data-original-title=\""+ getDescTitle(book.rating)+ "\">" + generateStars(book.rating)+ '</a></td></tr>\n' +
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
    $("#sellers-list").show(700);
}

/*  sends ajax request to get stats for the book */
function getStats(bid){
    var xmlhttp = ajaxRequest();
    xmlhttp.onreadystatechange=function(){
        if (xmlhttp.readyState===2){
            $("#stats-loading").show();
        }if (xmlhttp.readyState===4 ){
            $("#stats-loading").hide();
            if (xmlhttp.status === 200){
                $("#book-stats").removeClass();
                showStats(xmlhttp.responseText);
            }else
                $("#stats-error-show").show();
        }
    }
    var params = "book="+bid;
    xmlhttp.open("POST","/item/book/stats",true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xmlhttp.send(params);
}
/*  generates markup to display book stats*/
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

//asc desc setting of active
function activate(order){
    if (window.order === order)
        return;
    window.order = order;
    document.getElementById("li-sort-asc").className = "";
    document.getElementById("li-sort-desc").className = "";
    document.getElementById("li-sort-"+order).className = "active";
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
/*  generate pagination for listings */
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
/* highlights the selected sort order */
function setSortOrderVal(value){
    window.order = value;
    document.getElementById("li-sort-asc").className="";
    document.getElementById("li-sort-desc").className="";
    document.getElementById("li-sort-"+value).className="active";
}
/* returns the description for a rating */
function getDesc(rating){
    if (rating===1) return 'We advice that you find other alternatives';
    else if (rating===2) return 'Some pages torn<br/>not well maintained';
    else if (rating===3) return 'More than 1 year used<br/>Some edges torn';
    else if (rating===4) return 'Taken good care<br/>No torn pages/edges<br/>Has never been wet<br/>Well maintained';
    else if (rating===5) return 'Brand new quality<br/>Less than 2 months used';
}
/* returns the title of the description for a rating */
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
/* activates the current tab in the sort tabs
    update this and use bootstrap-tabs instead */
function displayTab(sort_by){
    window.sortBy = sort_by;
    document.getElementById("li-sort-posted").className = "";
    document.getElementById("li-sort-rating").className = "";
    document.getElementById("li-sort-price").className = "";
    document.getElementById("li-sort-"+sort_by).className = "active";
}
/*  onclick handler for changing sort order*/
function reorder(order){
    if (window.order === order)
        return;
    activate(order)
    requestSellers(window.sortBy,false);
}