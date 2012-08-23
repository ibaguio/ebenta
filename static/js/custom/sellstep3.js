function removeImage(num){
    if (num > 3 || num < 1) return;
    $("input[name=img"+num+"]").val("");
    if (num == window.max_img && num !=1){
        $("#simg"+num).hide(); 
        window.max_img = num-1;
    }   
}

function showAddImg(num){
    if (num > 3 || num < 1) return;
    $("#simg"+num).show();
    window.max_img = num;
}