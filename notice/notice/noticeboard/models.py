# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    writer = models.ForeignKey(User)
    title = models.CharField(max_length=20)
    text = models.TextField(max_length=200)
    pub_date = models.DateTimeField('post time',
                                    auto_now=True,
                                    auto_now_add=True)
    hits = models.IntegerField(default=0)
    ip_address = models.CharField(max_length=20)

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


class Comment(models.Model):
    writer = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    text = models.CharField(max_length=30)
    pub_date = models.DateTimeField('post time',
                                    auto_now=True,
                                    auto_now_add=True,
                                    default=timezone.now(),
                                    )

    def __unicode__(self):
        return self.text

    def update(self, text):
        self.text = text
        self.save()
