function show_error(msg){
    $("#info").prepend("<div class='alert alert-error'>"+msg+"<a href='#' class='close' data-dismiss='alert'>&times;</a></div>").show();
    console.log("errored");
};
function show_success(msg){
    $("#info").prepend("<div class='alert alert-success'>"+msg+"<a href='#' class='close' data-dismiss='alert'>&times;</a></div>").show();
};
