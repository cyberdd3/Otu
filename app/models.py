from django.contrib.auth.models import User
from django.db import models


def content_file_name(instance, filename):
    return 'avatars/' + str(instance.user.pk)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    username = models.TextField(max_length=256)
    fullname = models.TextField(max_length=256, blank=True)
    about = models.TextField(max_length=1024, blank=True)
    avatar = models.ImageField("Avatar", upload_to=content_file_name, blank=True, null=True)

    following = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='followers')

    friends = models.ManyToManyField('self', blank=True)
    outgoing_requests = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='incoming')

    def __unicode__(self):
        return self.user.username


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


class Post(models.Model):
    user = models.ForeignKey(User)
    title = models.TextField()
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post)
