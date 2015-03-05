require.config({
    paths: {
        'jquery': '//code.jquery.com/jquery-1.11.2.min',
        'app': './app',
        'util': './util',
        'jquery_cookie': '//cdnjs.cloudflare.com/ajax/libs/jquery-cookie/1.4.1/jquery.cookie'
    },
});

require(['app/write-main'], function(){
});
