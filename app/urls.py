from django.conf.urls import url, patterns, include

from project import settings
from app import views

urlpatterns = patterns('',
                       url(r'^$', views.feed, name='index'),
                       url(r'^register/$', views.register, name='register'),
                       url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
                       url(r'^login/$', views.login, name='login'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/login'}),
                       url(r'^profile/',
                           include(patterns('',
                                            url(r'^(?P<pk>[0-9]+)/$', views.profile, name='profile'),
                                            url(r'^$', views.profile, name='my_profile'),
                                            ))),

                       url(r'^followers/',
                           include(patterns('',
                                            url(r'^(?P<pk>[0-9]+)/$', views.followers, name='followers'),
                                            url(r'^$', views.followers, name='my_followers'),
                                            ))),
                       url(r'^following/',
                           include(patterns('',
                                            url(r'^(?P<pk>[0-9]+)/$', views.following, name='following'),
                                            url(r'^$', views.following, name='following_me'),
                                            ))),

                       url(r'^post/(?P<pk>[0-9]+)/$', views.post, name='post'),

                       url(r'^settings/$', views.settings, name='settings'),
                       url(r'^feed/$', views.feed, name='feed'),

                       url(r'^manage_comment/$', views.manage_comment, name='manage_comment'),

                       url(r'^manage_post/$', views.manage_post, name='manage_post'),

                       url(r'^follow/$', views.follow, name='follow'),
                       url(r'^unfollow/$', views.unfollow, name='unfollow'),

                       url(r'^api/check_email/$', views.check_email, name='check_email'),
                       )

if settings.DEBUG:
    urlpatterns += patterns('', url(r'media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }))
