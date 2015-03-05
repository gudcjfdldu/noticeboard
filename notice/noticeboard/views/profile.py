from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from noticeboard.models import UserProfile
from noticeboard.views import auth


def profile_validate(func):
    def inner(request, *args, **kwargs):
        profile = get_object_or_404(UserProfile, pk=kwargs['profile_id'])
        if request.user.username == profile.user.username:
            return func(request, *args, **kwargs)
        else:
            url = reverse('post.index_or_create')
            return HttpResponseRedirect(url)
    return inner


@auth.login_required()
@profile_validate
def detail(request, profile_id):
    profile = get_object_or_404(UserProfile, pk=profile_id)
    current_user = request.user.username
    context = {'profile': profile,
               'current_user': current_user}
    return render(request, 'noticeboard/profile.html', context)


@auth.login_required()
@profile_validate
def delete(request, profile_id):
    profile = get_object_or_404(UserProfile, pk=profile_id)
    if request.user.username == profile.user.username:
        profile.user.delete()
        auth.logout(request)
    return HttpResponseRedirect(reverse('auth.login'))


@auth.login_required()
@profile_validate
def edit(request, profile_id):
    if request.method == 'GET':
        profile = get_object_or_404(UserProfile, pk=profile_id)
        current_user = request.user.username
        context = {'profile': profile,
                   'current_user': current_user}
        return render(request, 'noticeboard/profile_edit.html', context)

    else:
        profile = get_object_or_404(UserProfile, pk=profile_id)
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        realname = request.POST.get('realname', '')
        website = request.POST.get('website', '')
        location = request.POST.get('location', '')
        age = request.POST.get('age', 0)
        if age == '':
            age = 0
        aboutme = request.POST.get('aboutme', '')

        if 'file' in request.FILES:
            profile_image = request.FILES.get('file')
            profile.image_update(profile_image=profile_image)

        profile.update(username=username, email=email, website=website,
                       location=location, realname=realname, age=age,
                       aboutme=aboutme)

        return HttpResponseRedirect(reverse('profile.detail',
                                    args=(profile.id,)))
