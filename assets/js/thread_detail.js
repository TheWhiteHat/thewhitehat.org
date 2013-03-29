jQuery.fn.show_reply_form = function(replyid){
    // show reply form to a post in a thread.
    $(this).html("Cancel");
    $(this).attr("onclick","$(this).hide_reply_form("+replyid+");");
    $(this).parent().append("<div id='replybox-"+replyid+"'>\
    <textarea name='body_text' id='reply-"+replyid+"'\
    class='span5' rows='6'></textarea><br />\
    <input type='hidden' id='id-"+replyid+"'value='"+replyid+"' />\
    <button onclick=\"$(this).reply('"+replyid+"');\">Submit</button>\
    </div>");
}
jQuery.fn.hide_reply_form = function(replyid){
    // hide reply form to post in a thread.
    $(this).html("Reply");
    $("#replybox-"+replyid).remove();
    $(this).attr("onclick","$(this).show_reply_form("+replyid+");");
}
jQuery.fn.reply = function(replyid){
    // post to reply handler
    if($("#reply-"+replyid).val() != "" && $("#id-"+replyid).val() != ""){
        (function(obj,replyid){
            $.ajax({
                type: "POST",
                url: reply_handler,
                data:{
                    csrfmiddlewaretoken: csrf_token,
                    body_text: $("#reply-"+replyid).val(),
                    reply_to: replyid,
                }
            }).done(function(msg){
                var response = $.parseJSON(msg);
                if (!response.success){
                    console.log("reply-error");
                    switch(response.reason){
                        case 'invalid-request':
                            show_error("Invalid Request");
                            break;
                        default:
                            show_error("Unspecified Error.");
                            break;
                    }
                }
                else
                {
                    console.log("success");
                    $("#replybox-"+replyid).remove();
                    var replies = $("#post-"+replyid).has("ul");
                    console.log(replies);
                    if(replies.length){
                        console.log("does not have replies");
                        $(replies).append("\
                        <span class='forum-thread-user-info'>You Said:</span>\
                        <div class='forum-thread-body'>"+response.message+"</div>\
                        </li>");
                    }else{
                        console.log("does not have replies");
                        $("#post-"+replyid).append("\
                        <ul class='unstyled thread-reply'><li>\
                        <span class='forum-thread-user-info'>You Said:</span>\
                        <div class='forum-thread-body'>"+response.message+"</div>\
                        </li></ul>");
                    }
                }
            });
        })(this,replyid);
    }
}
