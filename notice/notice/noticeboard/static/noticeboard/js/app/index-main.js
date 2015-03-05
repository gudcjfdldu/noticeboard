require(['util/search', 'jquery'], function(search, $){
   $(function(){
       $("#nb-search").keyup(function(){
           $.ajax({
               type: "GET",
               url: "/post/search/",
               data: {
                   title: $("#nb-search").val()
               },
               success: searchSuccess,
               dataType: 'html',
           });
       });
   });
});

function searchSuccess(data, textStatus, jqXHR){
    $("#plist-mini-list").html(data);
}
