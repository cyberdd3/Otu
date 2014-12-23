import json
from shutil import copyfile

from PIL import Image
import datetime
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from otu.models import Post, Comment, Dream, UserProfile
from otuproject import settings as otu_settings
from otu.utils import manage_avatar

def index(request):
    return render_to_response('otu/index.html', {}, RequestContext(request))


def register(request):
    context = RequestContext(request)

    if request.user.is_authenticated():
        logout(request)
    if request.method == 'POST':
        user = User()
        user.username = request.POST.get('email').replace('@', '-').replace('.', '-')
        user.email = request.POST.get('email')
        user.set_password(request.POST.get('password'))
        user.save()

        new_user = authenticate(username=user.email, password=request.POST.get('password'))
        if new_user:
            auth_login(request, new_user)

            media_root = otu_settings.MEDIA_ROOT;
            copyfile(media_root + 'avatars/no_med.jpg', media_root + 'avatars/' + str(new_user.pk) + '_med.jpg')
            copyfile(media_root + 'avatars/no_small.jpg', media_root + 'avatars/' + str(new_user.pk) + '_small.jpg')

            return HttpResponseRedirect('/edit_profile')
    return render_to_response('otu/register.html', {}, context)


def login(request):
    context = RequestContext(request)
    error_msg = None
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            error_msg = "Wrong email/password."

    return render_to_response('otu/login.html', {'error_msg': error_msg}, context)


@login_required
def edit_profile(request):
    context = RequestContext(request)
    user = request.user
    profile = UserProfile.objects.get_or_create(user=user)[0]

    if request.method == 'POST':

        profile.fullname = request.POST['fullname']
        profile.username = request.POST['username']
        profile.about = request.POST['about']

        media_root = otu_settings.MEDIA_ROOT
        if request.FILES.get('avatar', None):
            profile.avatar = request.FILES['avatar']
            profile.save()

            img_path = media_root + 'avatars/' + str(user.pk)
            img = Image.open(img_path)
            manage_avatar(img, img_path)

        profile.save()
        changed = True
    else:
        changed = False

    return render_to_response('otu/edit_profile.html', {'changed': changed, 'user_data': user, 'me': True}, context)


@login_required
def settings(request):
    context = RequestContext(request)
    if request.method == 'POST':
        user = request.user
        user.set_password(request.POST['new_password1'])
        user.save()
        changed = True
    else:
        changed = False

    change_password_form = PasswordChangeForm(request.user)
    return render_to_response('otu/settings.html', {'change_password_form': change_password_form,
                                                       'changed': changed}, context)


@login_required
def feed(request):
    context = RequestContext(request)
    friends = request.user.profile.friends.all()
    posts = []
    for friend in friends:
        posts += list(friend.user.post_set.all())

    posts.sort(key=lambda r: r.timestamp, reverse=True)
    return render_to_response('otu/feed.html', {'posts': posts}, context)


@login_required
def friends(request, pk=None):
    context = RequestContext(request)

    if not pk:
        pk = request.user.pk

    user = User.objects.get(pk=pk)
    context_dict = {'friends': user.profile.friends.all(), 'user_data':user, 'requests':user.profile.incoming.all()}

    return render_to_response('otu/friends.html', context_dict, context)


@login_required
def profile(request, pk=None):
    context = RequestContext(request)

    if not pk:
        pk = request.user.pk

    me = pk == request.user.pk

    user = User.objects.get(pk=pk)
    followers = user.profile.followers

    is_following = False
    if not me:
        for follower in list(followers.all()):
            if request.user == follower.user:
                is_following = True
                break

    my_dreams = Dream.objects.filter(user=user)

    for dream in my_dreams:
        date = datetime.datetime.strptime(dream.dream_date, '%d/%m/%Y')
        date.strftime('%d %b %Y')
        dream.dream_date = date.date()

    context_dict = {'dreams': my_dreams, 'user_data': user, 'is_following': is_following, 'me': me}

    return render_to_response('otu/profile.html', context_dict, context)


def dream(request, pk):
    dream = Dream.objects.get(pk=pk)
    return render_to_response('otu/dream.html', {'dream': dream}, RequestContext(request))

def follow(request):
    pk = request.GET['pk']

    if pk == request.user.pk:
        return HttpResponse()

    try:
        following_user = User.objects.get(pk=pk)
        request.user.profile.following.add(following_user.profile)
    except User.DoesNotExist:
        return HttpResponse()
    return HttpResponse()

def unfollow(request):
    pk = request.GET['pk']


    try:
        following_user = User.objects.get(pk=pk)
        request.user.profile.following.remove(following_user.profile)
    except User.DoesNotExist:
        return HttpResponse()
    return HttpResponse()

def followers(request):
    followers = request.user.profile.followers.all()
    count = followers.count()
    return render_to_response('otu/followers.html', {'count': count, 'followers': followers}, RequestContext(request))

def following(request):
    following = request.user.profile.following.all()
    count = following.count()
    return render_to_response('otu/following.html', {'count': count, 'following': following}, RequestContext(request))


@login_required
def manage_comment(request):
    if request.method == 'GET':
        if request.GET['action'] == 'delete':
            comment = Comment.objects.get(pk=request.GET['comment_id'])
            comment.delete()
        elif request.GET['action'] == 'edit':
            comment = Comment.objects.get(pk=request.GET['comment_id'])
            comment.text = request.GET['edited_text']
            comment.save()
        elif request.GET['action'] == 'add':
            comment = Comment()
            comment.text = request.GET['text']
            comment.user = request.user
            comment.post = Post.objects.get(pk=request.GET['post_id'])
            comment.save()

            resp = serialize('json', [comment,])
            resp_obj = json.loads(resp)
            resp_obj[0]['fields']['first_name'] = request.user.first_name
            resp_obj[0]['fields']['last_name'] = request.user.last_name
            resp_obj[0]['fields']['username'] = request.user.username
            return HttpResponse(json.dumps(resp_obj))


        return HttpResponse()


@login_required
def manage_dream(request):
    if request.method == 'GET':
        action = request.GET['action']
        try:
            dream = None if action == 'add' else Dream.objects.get(pk=request.GET['pk'])
        except Dream.DoesNotExist:
            return render_to_response('otu/manage_dream.html', {}, RequestContext(request))

        if action == 'delete':
            dream.delete()
            return HttpResponse()
        else:
            return render_to_response('otu/manage_dream.html', {'dream': dream}, RequestContext(request))
    else: #Button add dream was clicked
        if request.POST['pk']:
            dream = Dream.objects.get(pk=request.POST['pk'])
        else:
            dream = Dream(user=request.user)
        dream.title = request.POST['title']
        dream.content = request.POST['content']
        dream.dream_date = request.POST['dreamDate']

        dream.save()
        return HttpResponseRedirect('/dream/' + str(dream.pk))



def add_dream(request):
    if request.method == 'POST':
        dream = Dream(user=request.user)
        dream.title = request.POST['title']
        dream.content = request.POST['content']
        dream.dream_date = request.POST['dreamDate']

        dream.save()
        return HttpResponseRedirect('/dream/' + str(dream.pk))
    else:
        return render_to_response('otu/manage_dream.html', {}, RequestContext(request))



def check_email(request):
    if request.GET['email']:
        try:
            User.objects.get(email=request.GET['email'])
        except User.DoesNotExist:
            return HttpResponse(status=200)
        return HttpResponse(status=800)
    return HttpResponse(status=200)