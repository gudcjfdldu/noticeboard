# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from noticeboard.models import Post
from noticeboard.views import auth


@auth.login_required()
def index(request):
    current_user = request.user

    query = Post.objects.order_by('-pub_date')
    if 'title' in request.GET:
        title = request.GET.get('title')
        query = query.filter(title__contains=title)

    post_list = query.all()
    paginator = Paginator(post_list, 9)
    
    if 'page' in request.GET:
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
    else:
        contacts = paginator.page(1)

    context = {
        'current_user': current_user,
        'contacts': contacts
    }
    return render(request, 'noticeboard/index.html', context)


@auth.login_required()
def search(request):
    query = Post.objects.order_by('-pub_date')

    if 'title' in request.GET:
        title = request.GET.get('title')
        query = query.filter(title__contains=title)

    post_list = query.all()
    paginator = Paginator(post_list, 9)

    if 'page' in request.GET:
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
    else:
        contacts = paginator.page(1)

    context = {
        'contacts': contacts
    }
    return render(request, 'noticeboard/ajax_search.html', context)


@auth.login_required()
def create(request):
    writer = request.user
    title = request.POST.get('title', '')
    text = request.POST.get('content', '')
    post = Post.objects.create(title=title, text=text, writer=writer)
    return HttpResponseRedirect(reverse('post.read',
                                args=(post.id,)))


@auth.login_required()
def detail(request, post_id):
    current_user = request.user.username
    owner = False
    post = get_object_or_404(Post, pk=post_id)
    post.update_hits()
    comment = post.comment_set.order_by('-pub_date')
    if current_user == post.writer:
        owner = True
    context = {
        'post': post,
        'comment': comment,
        'current_user': current_user,
        'owner': owner
    }
    return render(request, 'noticeboard/detail.html', context)


def detail_or_delete(request, post_id):
    if request.method == 'GET':
        return detail(request, post_id)
    elif request.method == 'POST':
        return delete(request, post_id)


def index_or_create(request):
    if request.method == 'GET':
        return index(request)
    elif request.method == 'POST':
        return create(request)


@auth.login_required()
def delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return HttpResponseRedirect(reverse('post.index_or_create'))


@auth.login_required('register-required')
def write(request):
    current_user = request.user
    context = {'current_user': current_user}
    return render(request, 'noticeboard/write.html', context)


@auth.login_required()
def edit(request, post_id):
    if request.method == 'GET':
        current_user = request.user
        post = get_object_or_404(Post, pk=post_id)
        context = {'post': post, 'current_user': current_user}
        return render(request, 'noticeboard/write.html', context)

    elif request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)

        title = request.POST.get('title', '')
        text = request.POST.get('content', '')

        post.update(title=title, text=text)
        return HttpResponseRedirect(reverse('post.read',
                                    args=(post.id,)))
