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

function toggleSearch(num){
    if ($("a#toggle-search").text()[0]==="A"){
        $("div#search-basic").hide();
        $("div#search-advanced").show(500);
        $("a#toggle-search").text("Basic Search");
    }else{
        $("div#search-advanced").hide();
        $("div#search-basic").show(500);
        $("a#toggle-search").text("Advanced Search");
    }
}
/* updates the subcategory for advanced search */
function updateSub(){
    var cat_index = $("select#category option:selected").text();
    if (cat_index !== "") $("div#sub-category-div").show(500);
}

$(window).ready(function(){
    //var subcat = DICT OF SUBCAT
    //window.subCategory = JSON.parse()   
    getSearchData();
});