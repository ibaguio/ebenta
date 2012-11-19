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

function toggleSearch(){
    if ($("a#toggle-search").text()[0]==="A"){
        $("div#search-basic").hide();
        //$("div#search-advanced").css("display","inline-block")
        $("div#search-advanced").slideDown("slow");
        $("a#toggle-search").text("Basic Search");
    }else{
        $("div#search-advanced").hide();
        $("div#search-basic").slideDown("slow");
        $("a#toggle-search").text("Advanced Search");
    }
}
/* updates the subcategory for advanced search */
function updateSub(){
    var cat_index = $("select#category option:selected").text();
    var newOptions;
    if (cat_index === "Textbook"){
        $("div#sub-category-div").slideDown(500);
        $("#sub-category option").remove();
         newOptions = {
            '':'',
            'math' : 'Mathematics',
            'engg' : 'Engineering',
            'science' : 'Science',
            'history' : 'History',
            'english' : 'English',
            'filipino': 'Filipino',
            //'law' : 'Law',
        };
    }else if (cat_index === "Readings"){
        $("div#sub-category-div").slideUp(500);
        $("#sub-category option").remove();
    }else{
        $("div#sub-category-div").slideUp(500);
        $("#sub-category option").remove();
    }
    populateOptions(newOptions);
}

function populateOptions(newOptions){
    var select = $('#sub-category');
        if(select.prop) 
            var options = select.prop('options');
        else 
            var options = select.attr('options');
        
        $.each(newOptions, function(val, text) {
            options[options.length] = new Option(text, val);
        });
        select.val('');
}

$(window).ready(function(){
    //var subcat = DICT OF SUBCAT
    //window.subCategory = JSON.parse()
    //getSearchData();
});