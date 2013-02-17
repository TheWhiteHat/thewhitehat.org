function show_error(msg){
    $(".container").append("<div class='alert alert-error'>"+msg+"<a href='#' class='close' data-dismiss='alert'>&times;</a></div>");
    console.log("errored");
};
function show_success(msg){
    $(".container").append("<div class='alert alert-success'>"+msg+"<a href='#' class='close' data-dismiss='alert'>&times;</a></div>");
};
function vote(dir,objtype,objid){
    console.log("voting...");
    intRegex = /^\d+$/;
    if (typeof objtype === 'undefined' || !(objtype == 'question' || objtype == 'answer') || !(dir == 'up' || dir == 'down') || !intRegex.test(objid)){
        console.log("invalid args");
        return;
    }
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
        var response = jQuery.parseJSON(msg);
        if (response.success == false){
            console.log("there was an error");
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
            console.log("there was success");
            switch(response.message){
                case 'vote_handled':
                    show_success("Voted!");
                    break;
            }
        }
    });

}
