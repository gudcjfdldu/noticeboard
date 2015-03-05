define(['jquery'], function($){

    var ns = {};

    ns.commentModify = function(selector){
        var targets = $(selector);
        var base = targets.parents(".nb-comment-info");
        var child = base.find(".comment-text-inner");
        var form = base.find(".comment-form");
        child.hide();
        form.show();
    }
    return ns;
});


