/*  js used in sell steps*/
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