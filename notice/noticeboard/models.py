# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    writer = models.ForeignKey(User)
    title = models.CharField(max_length=20, blank=False)
    text = models.TextField(max_length=200)
    pub_date = models.DateTimeField('post time',
                                    auto_now=True,
                                    auto_now_add=True)
    hits = models.IntegerField(default=0)
    ip_address = models.GenericIPAddressField(default=None, null=True)

    def __unicode__(self):
        return self.title

    def update(self, title, text, ip_address):
        self.title = title
        self.text = text
        self.ip_address = ip_address
        self.save()

    def update_hits(self):
        self.hits = self.hits + 1
        self.save()


class Document(models.Model):
    filename = models.CharField(max_length=255, blank=False)
    docfile = models.FileField(upload_to='post-documents', blank=False)
    post = models.ForeignKey(Post)

    def update(self, filename, docfile):
        self.filename = filename
        self.docfile = docfile
        self.save()


class Image(models.Model):
    filename = models.CharField(max_length=255, blank=False)
    imgfile = models.ImageField(upload_to='post-images', blank=False)
    post = models.ForeignKey(Post)

    def update(self, filename, imgfile):
        self.filename = filename
        self.imgfile = imgfile
        self.save()


class Comment(models.Model):
    writer = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    text = models.CharField(max_length=30)
    pub_date = models.DateTimeField('post time',
                                    auto_now=True,
                                    auto_now_add=True,
                                    default=timezone.now())

    def __unicode__(self):
        return self.text

    def update(self, text):
        self.text = text
        self.save()


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    age = models.IntegerField(blank=True, default=0, null=True)
    email = models.EmailField(blank=True, default='', null=True)
    website = models.URLField(blank=True, default='', null=True)
    location = models.CharField(blank=True, max_length=140, default='')
    profile_image = models.ImageField(upload_to='profile-images', blank=True,
                                      default=None)
    about_me = models.TextField(max_length=300, blank=True, default='')
    real_name = models.CharField(blank=True, default='', max_length=100)

    def __unicode__(self):
        return self.user.username

    def update(self, username, email, website, location, age, realname, aboutme):
        self.user.username = username
        self.email = email
        self.website = website
        self.location = location
        self.real_name = realname
        self.age = age
        self.about_me = aboutme
        self.save()
        self.user.save()

    def image_update(self, profile_image):
        self.profile_image = profile_image
        self.save()
