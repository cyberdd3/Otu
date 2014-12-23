# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import otu.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options=None,
            bases=None,
            managers=None,
        ),
        migrations.CreateModel(
            name='Dream',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('content', models.TextField()),
                ('dream_date', models.TextField()),
                ('post_date', models.DateTimeField(auto_now_add=True)),
                ('lucid', models.BooleanField(default=False)),
                ('lucidStrength', models.IntegerField(default=0)),
                ('privacy', models.TextField(default='me')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options=None,
            bases=None,
            managers=None,
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('datetime', models.DateTimeField(db_index=True, auto_now_add=True)),
                ('sender', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options=None,
            bases=None,
            managers=None,
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options=None,
            bases=None,
            managers=None,
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
            options=None,
            bases=None,
            managers=None,
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('username', models.TextField(max_length=256)),
                ('fullname', models.TextField(blank=True, max_length=256)),
                ('about', models.TextField(blank=True, max_length=1024)),
                ('avatar', models.ImageField(null=True, blank=True, upload_to=otu.models.content_file_name, verbose_name='Avatar')),
                ('following', models.ManyToManyField(blank=True, related_name='followers', to='otu.UserProfile')),
                ('friends', models.ManyToManyField(blank=True, related_name='friends_rel_+', to='otu.UserProfile')),
                ('outgoing_requests', models.ManyToManyField(blank=True, related_name='incoming', to='otu.UserProfile')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options=None,
            bases=None,
            managers=None,
        ),
        migrations.AddField(
            model_name='message',
            name='thread',
            field=models.ForeignKey(to='otu.Thread'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(to='otu.Post'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
