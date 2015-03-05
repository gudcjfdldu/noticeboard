define(['jquery', 'jquery_cookie'], function($){

    var ns = {};

    ns.chooseFile = function(selector){
        var targets = $(selector);
        var base = targets.parent();
        var targets = base.next();
        targets.css("display", "block");
    }

    ns.uploadFile = function(selector){
        var targets = $(selector);
        targets.nextAll(".upload-file-inner").trigger('click');
    }

    ns.chooseImage = function(selector){
        var targets = $(selector).parent().next().children('#inner-img-form');
        targets.trigger('click');
    }

    ns.changeFile = function(selector){
        var targets = $(selector).prev();
        var filename = $(selector).val().split('\\').pop();
        targets.text(filename)
    }
    
    ns.changeImage = function(selector){
        var targets = $(selector);
        var csrftoken = $.cookie('csrftoken');
        var fd = new FormData();
        var post_id = targets.next().text();
        var filename = targets.val().split('\\').pop();
        fd.append('file', targets[0].files[0]);
        
        $.ajaxSetup({
            beforeSend: function(xhr){
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        });

        $.ajax({
            type: "POST",
            url: "/post/" + post_id + "/image/",
            processData: false,
            contentType: false,
            data: fd,
            success: uploadSuccess,
            dataType: 'html'
        });
        function uploadSuccess(data, textStatus, jqXHR){
            $(".post-image-area").html(data);
        }
    }

    ns.choosePreviewImage = function(selector){
        var targets = $(selector).parent().next().children('#preview-img-form');
        targets.trigger('click')
    }

    ns.previewImage = function(input){
       if(input.files && input.files[0]){
            var reader = new FileReader();
            var dvPreview = $("#dvPreview");
            var delbutton_src = $(".del-button-src").text();
            var filename = $(input).val().split('\\').pop();
            reader.onloadend = function(e){
                var delete_div = $("<div class='del-button'></div>");
                var delete_button = $("<a href='javascript:void(0);' onclick='deleteImage(this);' class='inner-del-button'></a>");
                var img_summary = $("<div class='img-summary'></div>");
                delete_div = delete_div.append(delete_button)

                var input_tag = $("<input type='hidden' name='img'/>");
                var input_name = $("<input type='hidden' name='filename'/>");
                input_name.attr("value", filename);
                input_tag.attr("value", e.target.result);
                var wrapper = $("<div class='img-wrapper'></div>");
                var img = $("<img />");
                img.attr("src", e.target.result);
                img.attr("style", "max-width: 100%; max-height: 100%");
                img_summary = img_summary.append(img);

                dvPreview.append(wrapper.append(img_summary).append(delete_div))
                dvPreview.append(input_tag)
                dvPreview.append(input_name)

            }

            reader.readAsDataURL(input.files[0])
       }
    }

    ns.deleteImage = function(selector){
        var targets = $(selector).parents('.img-summary');
        targets.empty();
    }
    return ns;
});


