require(['util/comment', 'jquery'], function(comment, $){
   $(function(){
       $(".comment-modify").click(function(){
            comment.commentModify(this);
       });
   });
});
