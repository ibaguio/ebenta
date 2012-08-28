function removeImage(num){
    if (num > 3 || num < 1) return;
    $("input#img"+num).val("");
    if (num == window.max_img && num !=1){
        $("#simg"+num).hide(); 
        window.max_img = num;
    }
    if ($("input#img"+num).attr("class") === "imgerror"){
        $("input#img"+num).removeClass("imgerror");
        window.invalid_img -= 1;
    }
    clearColors(num);
}
function showAddImage(input){
    var num = parseInt($(input).attr("id").charAt(3))+1;
    if (num > 3 || num < 1) return;
    $("#simg"+num).show();
    window.max_img = num-1;
}
function update(input){
    var img_id = $(input).attr("id");
    var num = parseInt(img_id.charAt(3));
    validateImage(input,function(){
        $("div#simg"+num).removeClass("error");
        $("div#simg"+num).addClass("success");
        $(input).removeClass("imgerror");
        if (window.invalid_img>0)
            window.invalid_img -=1;
        showAddImage(input);
    },function(){
        $("div#simg"+num).removeClass("success");
        $("div#simg"+num).addClass("error");
        $(input).addClass("imgerror");
        window.invalid_img += 1;
    },clearColors(num));
    checkDisabled();
}
function clearColors (num) {
    $("div#simg"+num).removeClass("success");
    $("div#simg"+num).removeClass("error");
    $("input#img"+num).removeClass("imgerror");
    checkDisabled();
}
function checkDisabled(){
    if (window.invalid_img !==0)
        $("button#submit-order").addClass("disabled");
    else
        $("button#submit-order").removeClass("disabled");
}
window.invalid_img = 0;