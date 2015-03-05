define(['jquery'], function($){
    
    var ns = {};
    
    ns.changeImage = function(input){
        if(input.files && input.files[0]){
            var reader = new FileReader();
            var imagePreview = $(".profile-img-wrapper");
            var filename = $(input).val().split('\\').pop();
            reader.onloadend = function(e){
                var input_tag = $("<input type='hidden' name='img'/>");
                var input_name = $("<input type='hidden' name='filename'/>");
                input_name.attr("value", filename);
                input_tag.attr("value", e.target.result);
                var img = $(".profile-image");
                img.attr("src", e.target.result);
                img.attr("style", "max-width: 100%; max-height: 100%");
            }
            reader.readAsDataURL(input.files[0])
        }
    }
    return ns;
});
