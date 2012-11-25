window.onload = function(){
    var path = window.location.pathname;
    $("#admin-nav").click(function(){
        showAdmin();
    });
    $("a.span").each(function(index){
        $(this).click(function(){
            toggle(index);
        })
    });
    if (path.indexOf("users")!==-1){
        var targ = $("select.input-medium");
        targ.change(function(){
            window.location.replace("/admin/view/users?sort="+targ.val());
        });
    }
    if (path.indexOf("/admin/")!==-1)
        showAdmin();
}
function showAdmin(){
    hideAll();
    var admn = $("#uladmin");
    if (admn.attr("class")==="hidden") 
        admn.attr("class","nav nav-list");
    else 
        admn.attr("class","hidden");
}
function toggle(id){
    var targ = $("tbody#bdy-"+id);
    if (targ.css('display')==="none"){
        targ.show(555);  
        $("i#ex-"+id).attr('class','icon-minus');
    }else targ.hide(555,function(){$("i#ex-"+id).attr('class','icon-plus')});
}