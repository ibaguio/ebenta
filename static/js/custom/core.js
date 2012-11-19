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
/**/
function validateImage(input_img,success_callback,fail_callback,cancel_callback){
    var fname = input_img.value;
    if (!fname)
      fname = input_img.val();
    if (fname===""){
      cancel_callback();
      return;
    }else if (!/(\.(gif|jpe?g|jpeg|bmp|png))$/i.test(fname)){
       fail_callback();
       return;
    }
    success_callback();
}
/* identical to pythons string.title() built-in function */
String.prototype.toProperCase = function () {
    return this.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
};
// Source: http://stackoverflow.com/questions/497790
function getDateToday(){
    var today = new Date();
    today.setMinutes(0);
    today.setHours(0);
    today.setSeconds(0);
    today.setMilliseconds(0);
    return today;
}
function qsFocus(){
  $("#quick-search").animate({width:'270px'},400);
  $("#quick-search-button").show();
}
function qsBlur(){
  $("#quick-search").animate({width:'130px'},400);
  $("#quick-search-button").hide();
}