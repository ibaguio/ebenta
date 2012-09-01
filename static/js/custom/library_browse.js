/* library browse scripts 
    script used in browsing ebenta library*/
function requestLibrary(page){
    var xmlhttp = ajaxRequest();
    xmlhttp.onreadystatechange=function(){
        if (xmlhttp.readyState === 2){
            $("i#loading").show();
            $("#load-error").hide();
        }if (xmlhttp.readyState === 4){
            if (xmlhttp.status === 200){
                var jdata=JSON.parse(xmlhttp.responseText);
                populateResults(jdata);
                window.pages = jdata.pages;
                window.page = jdata.page;
                $("#loading").hide();
                $("#load-error").hide();
            }else{
                $("#loading").hide();
                $("#load-error").show();
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
//populate results in browse
function populateResults(jdata){
    var i=0;
    var books = JSON.parse(jdata.books);
    var buySell = JSON.parse(jdata.buySell);
    var pages = jdata.pages;
    window.jdata = jdata;
    window.page = jdata.page;
    var html_code="";
    for (i=0;i<books.length;i++){
        book = JSON.parse(books[i]);
        var markup = '<div class="browsed"><div class="row-fluid">' +
        '<span class="browsed-img"><a href="book/info?book='+book.key+'" class="book-image">';
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
            '<span title="Buying"><i class="icon-shopping-cart"></i> '+buySell[i][0].toString()+' </span>'+
            '<span title="Selling"><i class="icon-book"></i> '+buySell[i][1].toString()+' </span></span></div></div></div>';
        html_code+=markup;
    }
    $("#browsed-div").html(html_code);
    $(".link").popover();
    generateBrowsePaginationMarkup();
    var offset = ((jdata.page-1)*14)+1;
    var disp = "Showing "+offset+"-"+jdata.items+" of "+jdata.total;
    $("#display-info").text(disp);
}
function generateBrowsePaginationMarkup(){
    var i=0;
    var limit=14;
    var data = window.jdata;
    //calculate the number of pages
    var pages = data.pages;
    //current page
    var page = data.page;

    var markup = "<li";
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
    markup+="><a href=\"javascript:void(0)\" onclick=\"gotoNextPage()\">»</a></li>";
    $("#pagination").html(markup);
}
function gotoPage(page){
    if (window.page === page)
        return;
    requestLibrary(page);
}
function gotoNextPage(){
    page = window.page+1;
    if (page > window.pages) return;
    gotoPage(page);
}
function gotoPrevPage(){
    page = window.page-1;
    if (page < 1) return;
    gotoPage(page);   
}
//function to open book page in browse
function openBookPage(book_id){
    location.href="book/info?book="+book_id;
}
/* functions for nav in browse page */
function showNav(){//show nav for browsing
    document.getElementById("imgHide").className="hidden";
    $("div#browsed-div").hide();
    $("#results-nav").hide();
    document.getElementById("browsed-title").className="hidden";
    $("#browseNav").slideDown("fast",function(){
        document.getElementById("browsed-title").className="span9";
        document.getElementById("browsed-div").className="span8 well";
        $("div#browsed-div").slideDown("normal");
        $("#results-nav").show();
    })        
    $("#results-nav").removeClass();
    $("#results-nav").addClass("span9 offset3");

}
function hideNav(){//hide nav for browsing
    $("#browseNav").hide();
    document.getElementById("browsed-div").className="span11-5 well";
    document.getElementById("browsed-title").className="span12";
    document.getElementById("imgHide").className="";
    $("#results-nav").removeClass();
}