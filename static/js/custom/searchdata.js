/* get the typeahead data for the book */

function getSearchData(){
    var xmlhttp;
    if (window.XMLHttpRequest)// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
    else// code for IE6, IE5
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");

    xmlhttp.onreadystatechange=function(){
        if (xmlhttp.readyState === 4){
            src = eval(xmlhttp.responseText);
            window.test = src;
            $('input#q').typeahead({source:src,minLength:"4",items:"10"});
        }
    }
    xmlhttp.open("GET","/book/list.txt",true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.send();
}

$(window).ready(getSearchData());