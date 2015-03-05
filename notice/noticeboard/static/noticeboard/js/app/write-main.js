require(['util/write', 'jquery'], function(write, $){
   $(function(){
       $("#inner-file-box1").change(function(){
           write.chooseFile(this);
       });
       $("#inner-file-box2").change(function(){
           write.chooseFile(this);
       });
       $("#inner-file-box3").change(function(){
            write.chooseFile(this);
       });
       $("#inner-file-box4").change(function(){
            write.chooseFile(this);
       });
       $(".upload-button").click(function(){
            write.uploadFile(this);     
       });
       $(".upload-file-inner").change(function(){
            write.changeFile(this);
       });
       $(".img-upload-button").click(function(){
            write.chooseImage(this); 
       });
       $("#inner-img-form").change(function(){
            write.changeImage(this);
       });
       $(".img-preview-button").click(function(){
            write.choosePreviewImage(this);
       });
       $("#preview-img-form").change(function(){
            write.previewImage(this);
       });
   });
});

function deleteImage(selector){
    var targets = $(selector).parents('.img-wrapper');
    targets.remove();
}

