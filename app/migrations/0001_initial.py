# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import app.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('text', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.TextField()),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('username', models.TextField(max_length=256)),
                ('fullname', models.TextField(blank=True, max_length=256)),
                ('about', models.TextField(blank=True, max_length=1024)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=app.models.content_file_name, verbose_name='Avatar')),
                ('following', models.ManyToManyField(to='app.UserProfile', blank=True, related_name='followers')),
                ('friends', models.ManyToManyField(to='app.UserProfile', blank=True, related_name='friends_rel_+')),
                ('outgoing_requests', models.ManyToManyField(to='app.UserProfile', blank=True, related_name='incoming')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(to='app.Post'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
