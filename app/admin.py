from django.contrib import admin

from app.models import UserProfile, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['content', 'user']

admin.site.register(UserProfile)
admin.site.register(Post, PostAdmin)
