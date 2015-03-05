# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from noticeboard.views import auth, post, comment

urlpatterns = patterns(
    '',

    # Post views
    url(r'^post/$', post.index_or_create, name='post.index_or_create'),
    url(r'^post/(?P<post_id>\d+)$', post.detail_or_delete, name='post.read'),
    url(r'^post/search', post.search, name='post.search'),
    url(r'^post/(?P<post_id>\d+)/edit$', post.edit, name='post.edit'),
    url(r'^post/(?P<post_id>\d+)/delete$', post.delete, name='post.delete'),
    url(r'^post/write$', post.write, name='post.write'),

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
)
