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
/* returns the visible width of the browser*/
function getWidth(){
  return(window.innerWidth)?
  window.innerWidth:
  document.documentElement.clientWidth||document.body.clientWidth||0;
}/* returns the visible height of the browser*/
function getHeight(){
  return(window.innerHeight)?
  window.innerHeight:
  document.documentElement.clientHeight||document.body.clientHeight||0;
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