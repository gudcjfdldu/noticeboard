# -*- coding: utf-8 -*-

import urllib

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from noticeboard.models import UserProfile


error_dict = {
    'register-required': 'you have to register account',
    'match-password': 'please match both password',
    'same-username': 'already have been same username',
    'account-disabled': 'The password is valid, but the account the has been disabled!',
    'input-mustbeset': 'The given username and password must be set',
    'input-incorrect': 'The username and password incorrect',
}


def login_required(error_code=None):
    def decorator(func):
        def inner(request, *args, **kwargs):
            if request.user.is_authenticated():
                return func(request, *args, **kwargs)
            else:
                url = reverse('auth.login')
                if error_code is not None:
                    parameters = {
                        'error_code': error_code
                    }

                    url += '?' + urllib.urlencode(parameters)
                return HttpResponseRedirect(url)
        return inner
    return decorator


def login_handler(request, error_code=None):
    if request.method == 'POST':
        username = request.POST.get('user-name', '')
        password = request.POST.get('user-password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('post.index_or_create'))
            error_code = 'account-disabled'
        else:
            error_code = 'input-incorrect'
        context = {'error_message': error_dict[error_code]}
        return render(request, 'noticeboard/login.html', context)
    if request.GET.get('error_code', ''):
        error_code = request.GET.get('error_code')
    else:
        return render(request, 'noticeboard/login.html')
    context = {'error_message': error_dict[error_code]}
    return render(request, 'noticeboard/login.html', context)


def logout_handler(request):
    if request.method == 'GET':
        logout(request)
        return HttpResponseRedirect(reverse('post.index_or_create'))


def register(request):
    if request.method == 'GET':
        return render(request, 'noticeboard/register.html')
    elif request.method == 'POST':
        user_object_list = User.objects.all()
        username = request.POST.get('user-name', '')
        if username == '':
            context = {'error_message': error_dict['input-mustbeset']}
            return render(request, 'noticeboard/register.html', context)
        for user in user_object_list:
            if user.username == username:
                context = {'error_message': error_dict['same-username']}
                return render(request, 'noticeboard/register.html', context)
        email = request.POST.get('user-email', '')
        password = request.POST.get('user-password', '')
        confirm_password = request.POST.get('confirm-password', '')
        if password != confirm_password:
            context = {'error_message': error_dict['match-password']}
            return render(request, 'noticeboard/register.html', context)
        else:
            user = User.objects.create_user(username, email, password)
            UserProfile.objects.create(user=user, email=user.email)
            return HttpResponseRedirect(reverse('post.index_or_create'))
