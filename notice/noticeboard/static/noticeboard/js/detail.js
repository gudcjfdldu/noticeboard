require.config({
    paths: {
        'jquery': '//code.jquery.com/jquery-1.11.2.min',
        'app': './app',
        'util': './util'
    },
});

require(['app/detail-main'], function(){
});
