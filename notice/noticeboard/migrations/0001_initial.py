# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=30)),
                ('pub_date', models.DateTimeField(default=datetime.datetime(2015, 3, 3, 4, 52, 34, 100890, tzinfo=utc), auto_now=True, auto_now_add=True, verbose_name=b'post time')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=255)),
                ('docfile', models.FileField(upload_to=b'post-documents')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=255)),
                ('imgfile', models.ImageField(upload_to=b'post-images')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=20)),
                ('text', models.TextField(max_length=200)),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name=b'post time', auto_now_add=True)),
                ('hits', models.IntegerField(default=0)),
                ('ip_address', models.GenericIPAddressField(default=None, null=True)),
                ('writer', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('age', models.IntegerField(default=0, null=True, blank=True)),
                ('email', models.EmailField(default=b'', max_length=75, null=True, blank=True)),
                ('website', models.URLField(default=b'', null=True, blank=True)),
                ('location', models.CharField(default=b'', max_length=140, blank=True)),
                ('profile_image', models.ImageField(default=None, upload_to=b'profile-images', blank=True)),
                ('about_me', models.TextField(default=b'', max_length=300, blank=True)),
                ('real_name', models.CharField(default=b'', max_length=100, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='image',
            name='post',
            field=models.ForeignKey(to='noticeboard.Post'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='post',
            field=models.ForeignKey(to='noticeboard.Post'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(to='noticeboard.Post'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='writer',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
