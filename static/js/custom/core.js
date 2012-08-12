/*	general usefull functions*/
/* creates an ajax object */
function ajaxRequest(){
    var xmlhttp;
    if (window.XMLHttpRequest)// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
    else// code for IE6, IE5
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    return xmlhttp;
}
/* returns the get params in the url */
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
/* generates markup for stars given a rating */
function generateStars(rating){
    var markup = "", i=0;
    for (i=0; i<rating; i++)
        markup+= '<img class="rating-star14" src="/static/images/gold_star.png">';
    for (i=0; i<5-rating;i++)
        markup+= '<img class="rating-star14" src="/static/images/white_star.png">';
    return markup;
}
/* identical to pythons string.title() built-in function */
String.prototype.toProperCase = function () {
    return this.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
};