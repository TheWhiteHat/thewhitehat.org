jQuery.fn.vote = function(dir,objtype,objid){
    if (!$(this).hasClass("btn-info")){
    (function(obj,dir){
        $.ajax({
          type: "POST",
          url: vote_handler,
          data: {
            csrfmiddlewaretoken: csrf_token,
            objid: objid,
            objtype: objtype,
            dir:dir,
          }
        }).done(function( msg ) {
            var response = $.parseJSON(msg);
            if (!response.success){
                console.log("vote-error");
                switch(response.reason){
                    case 'user_cannot_vote':
                        show_error("You may not vote on this. You may be under a ban.");
                        break;
                    case 'user_already_voted':
                        show_error("You have already voted on this.");
                        break;
                    case 'object_does_not_exist':
                        show_error("Invalid object.");
                        break;
                    case 'user_not_logged_in':
                        show_error("Please login to vote.");
                }
            }else{
                $(obj).addClass("btn-info");
                if(dir=="up"){
                    console.log("traversing next");
                    $(obj).next().next(".vote").removeClass("btn-info");
                    var num = parseInt($(obj).nextAll("span").first().text());
                    console.log("num is "+num);
                    $(obj).nextAll("span").first().text(num+1);
                    var num2 = parseInt($(obj).nextAll(".vote").nextAll("span").first().text());
                    $(obj).nextAll(".vote").nextAll("span").first().html(num2-1);
                }else{
                    console.log("traversing prev");
                    $(obj).prevAll(".vote").removeClass("btn-info")
                    var num = parseInt($(obj).nextAll("span").first().text());
                    $(obj).nextAll("span").first().text(num+1);
                    var num2 = parseInt($(obj).prevAll(".vote").nextAll("span").first().text());
                    $(obj).prevAll(".vote").nextAll("span").first().html(num2-1);
                }
            }
        }
        );
    })(this,dir);
    };
}
