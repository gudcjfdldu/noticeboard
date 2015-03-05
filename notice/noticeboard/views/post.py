# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.files.base import ContentFile

from noticeboard.views import auth
from noticeboard.models import Document, Image, Post


@auth.login_required()
def index(request):
    current_user = request.user
    profile = request.user.userprofile
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
        'contacts': contacts,
        'profile': profile
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
def upload_img(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if 'file' in request.FILES:
        imgfile = request.FILES.get('file')
        Image.objects.create(filename=imgfile.name,
                             imgfile=imgfile,
                             post=post)

    images = post.image_set.all()
    context = {'images': images}

    return render(request, 'noticeboard/ajax_image.html', context)


@auth.login_required()
def create(request):
    writer = request.user
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip_address:
        ip = ip_address.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    title = request.POST.get('title', '')
    text = request.POST.get('content', '')
    if 'img' in request.POST:
        filename_list = request.POST.getlist('filename')
        img_list = request.POST.getlist('img')
        img_summary = zip(filename_list, img_list)

    if title == '' or text == '':
        error_message = "you have to write title and content"
        context = {"error_message": error_message}
        return render(request, 'noticeboard/write.html', context)

    post = Post.objects.create(title=title, text=text, writer=writer, ip_address=ip)
    if 'file' in request.FILES:
        for afile in request.FILES.getlist('file'):
            file = afile
            Document.objects.create(docfile=file,
                                    filename=file.name,
                                    post=post)
    if 'img' in request.POST:
        for name, afile in img_summary:
            image_data = afile[afile.find(',') + 1:].decode('base64')
            Image.objects.create(filename=name,
                                 imgfile=ContentFile(image_data, name),
                                 post=post)

    return HttpResponseRedirect(reverse('post.read',
                                args=(post.id,)))


@auth.login_required()
def detail(request, post_id):
    current_user = request.user.username
    owner = False
    post = get_object_or_404(Post, pk=post_id)
    document = post.document_set.all()
    images = post.image_set.all()
    post.update_hits()
    profile = request.user.userprofile
    comments = post.comment_set.order_by('-pub_date')
    if current_user == post.writer.username:
        owner = True
    context = {
        'profile': profile,
        'post': post,
        'comments': comments,
        'current_user': current_user,
        'owner': owner,
        'documents': document,
        'images': images,
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
    if request.user.username == post.writer.username:
        post.delete()
    return HttpResponseRedirect(reverse('post.index_or_create'))


@auth.login_required('register-required')
def write(request):
    current_user = request.user
    profile = request.user.userprofile
    context = {'current_user': current_user,
               'profile': profile}
    return render(request, 'noticeboard/write.html', context)


@auth.login_required()
def edit(request, post_id):
    if request.method == 'GET':
        current_user = request.user
        profile = request.user.userprofile
        post = get_object_or_404(Post, pk=post_id)
        document = post.document_set.all()
        images = post.image_set.all()
        if current_user.username == post.writer.username:
            context = {'post': post,
                       'current_user': current_user,
                       'documents': document,
                       'profile': profile,
                       'images': images}
            return render(request, 'noticeboard/write.html', context)
        else:
            return HttpResponseRedirect(reverse('post.index_or_create'))

    elif request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        title = request.POST.get('title', '')
        text = request.POST.get('content', '')
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip_address:
            ip = ip_address.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        post.update(title=title, text=text, ip_address=ip)
        documents = post.document_set.all()
        ziplist = zip(request.FILES.getlist('file'), documents)
        for afile, document in ziplist:
            file = afile
            document.update(docfile=file,
                            filename=file.name)
        return HttpResponseRedirect(reverse('post.read',
                                    args=(post.id,)))
