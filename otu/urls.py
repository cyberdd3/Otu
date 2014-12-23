from django.conf.urls import url, patterns
from otuproject import settings
from otu import views
import otu

urlpatterns = patterns('',
                url(r'^$', views.feed, name='index'),
                url(r'^register/$', views.register, name='register'),
                url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
                url(r'^login/$', views.login, name='login'),
                url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/login'}),
                url(r'^profile/$', views.profile, name='home'),
                url(r'^profile/(?P<pk>[\-0-9 ]+)/$', views.profile, name='profile'),
                url(r'^friends/$', views.friends, name='my_friends'),
                url(r'^friends/(?P<pk>[\-0-9 ]+)/$', views.friends, name='friends'),
                url(r'^settings/$', views.settings, name='settings'),
                url(r'^feed/$', views.feed, name='feed'),

                url(r'^send_message/$', views.send_message, name='send_message'),

                url(r'^manage_comment/$', views.manage_comment, name='manage_comment'),

                url(r'^manage_dream/$', views.manage_dream, name='manage_dream'),

                url(r'^follow/$', views.follow, name='follow'),
                url(r'^unfollow/$', views.unfollow, name='unfollow'),

                url(r'^add_dream/$', views.add_dream, name='add_dream'),
                url(r'^followers/$', views.followers, name='followers'),
                url(r'^following/$', views.following, name='following'),
                url(r'^dream/(?P<pk>[\-0-9 ]+)/$', views.dream, name='dream'),
                url(r'^api/check_email/$', views.check_email, name='check_email'),
                )

if settings.DEBUG:
    urlpatterns += patterns('', url(r'media/(?P<path>.*)$', 'django.views.static.serve', {
           'document_root':settings.MEDIA_ROOT,
    }))