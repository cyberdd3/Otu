from django.contrib import admin
from django.contrib.auth.models import User
from otu.models import UserProfile, Post, Thread, Dream


class PostAdmin(admin.ModelAdmin):
    list_display = ['content', 'user']

admin.site.register(Post, PostAdmin)
admin.site.register(UserProfile)
admin.site.register(Thread)
admin.site.register(Dream)