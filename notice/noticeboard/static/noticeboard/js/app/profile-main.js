require(['util/profile', 'jquery'], function(profile, $){
   $(function(){
       $(".profile-file").change(function(){
            profile.changeImage(this);
       });
   });
});

function uploadImage(selector){
    var targets = $(selector).next();
    targets.trigger('click')
}

