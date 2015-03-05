# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from noticeboard.models import Post, Comment


def write_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        writer = request.user
        text = request.POST.get('comment', '')
        post.comment_set.create(text=text, writer=writer)
        return HttpResponseRedirect(reverse('post.read',
                                    args=(post.id,)))


def delete_comment(request, comment_id):
    if request.method == 'GET':
        comment = get_object_or_404(Comment, pk=comment_id)
        if request.user.username == comment.writer.username:
            comment.delete()
        return HttpResponseRedirect(reverse('post.read',
                                    args=(comment.post.id,)))


def modify_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, pk=comment_id)
        if request.user.username == comment.writer.username:
            text = request.POST.get('comment', '')
            comment.update(text=text)
        return HttpResponseRedirect(reverse('post.read',
                                    args=(comment.post.id,)))
