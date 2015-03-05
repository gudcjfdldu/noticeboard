from django.conf import settings
from django.conf.urls import patterns, url
from noticeboard.views import auth, post, comment, files, profile
urlpatterns = patterns(
    '',
    # Post views
    url(r'^post/$', post.index_or_create, name='post.index_or_create'),
    url(r'^post/(?P<post_id>\d+)$', post.detail_or_delete, name='post.read'),
    url(r'^post/search', post.search, name='post.search'),
    url(r'^post/(?P<post_id>\d+)/edit$', post.edit, name='post.edit'),
    url(r'^post/(?P<post_id>\d+)/delete$', post.delete, name='post.delete'),
    url(r'^post/write$', post.write, name='post.write'),
    url(r'^post/(?P<post_id>\d+)/image/$', post.upload_img, name='post.img'),

    # Comment views
    url(r'^post/(?P<post_id>\d+)/comment/$',
        comment.write_comment, name='comment.create'),
    url(r'^comment/(?P<comment_id>\d+)/delete$',
        comment.delete_comment,
        name='comment.delete'),
    url(r'^comment/(?P<comment_id>\d+)/edit$',
        comment.modify_comment,
        name='comment.edit'),

    # Auth views
    url(r'^register$', auth.register, name='auth.register'),
    url(r'^login$', auth.login_handler, name='auth.login'),
    url(r'^logout$', auth.logout_handler, name='auth.logout'),

    # file views
    url(r'^download/(?P<document_id>\d+)$', files.download,
        kwargs=dict(
            document_root=settings.MEDIA_ROOT,
        ),
        name='files.download'),

    # profile views
    url(r'^users/(?P<profile_id>\d+)$', profile.detail, name='profile.detail'),
    url(r'^users/(?P<profile_id>\d+)/edit$', profile.edit, name='profile.edit'),
    url(r'^users/(?P<profile_id>\d+)/delete$', profile.delete, name='profile.delete'),

)
