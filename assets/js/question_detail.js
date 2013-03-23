jQuery.fn.vote = function(dir,objtype,objid){
    // if the user clicked the button that wasn't hightlighted
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
                    var thisSpn = $(obj).nextAll("span").first();
                    var otherBtn = $(obj).next().next(".vote");
                    var otherSpn = $(obj).nextAll(".vote").nextAll("span").first();
                }
                else if(dir=="down"){
                    var thisSpn = $(obj).nextAll("span").first();
                    var otherBtn = $(obj).prevAll(".vote").first();
                    var otherSpn = $(obj).prevAll(".vote").nextAll("span").first();
                }

                var otherBtnActive = otherBtn.hasClass("btn-info");

                // remove the highlighting from the other button
                // and decrement votes if it had any
                if(otherBtnActive){
                    otherBtn.removeClass("btn-info");
                    var otherVotes = parseInt(otherSpn.text());
                    otherVotes != 0 && otherSpn.html(otherVotes-1);
                }

                // get the current votes from the current button
                // and increment
                var thisVotes = parseInt(thisSpn.text());
                thisSpn.text(thisVotes+1);

            }
        }
        );
    })(this,dir);
    };
}
