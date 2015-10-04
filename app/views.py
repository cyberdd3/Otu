import json
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

from app.models import Post, UserProfile, Comment

from app.utils import compose_and_save_avatar, create_avatar_placeholder


def index(request):
    return render_to_response('jay/index.html', {}, RequestContext(request))


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
            create_avatar_placeholder(new_user.pk)

            return HttpResponseRedirect('/edit_profile')
    return render_to_response('jay/register.html', {}, context)


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

    return render_to_response('jay/login.html', {'error_msg': error_msg}, context)


@login_required
def edit_profile(request):
    context = RequestContext(request)
    user = request.user
    userprofile = UserProfile.objects.get_or_create(user=user)[0]

    if request.method == 'POST':
        userprofile.fullname = request.POST['fullname']
        userprofile.username = request.POST['username']
        userprofile.about = request.POST['about']

        if request.FILES.get('avatar', None):
            userprofile.avatar = request.FILES['avatar']
            userprofile.save()

            compose_and_save_avatar(user.pk)

        userprofile.save()
        changed = True
    else:
        changed = False

    return render_to_response('jay/edit_profile.html', {'changed': changed, 'user_data': user}, context)


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
    return render_to_response('jay/settings.html', {'change_password_form': change_password_form,
                                                    'changed': changed}, context)


@login_required
def feed(request):
    context = RequestContext(request)
    following = request.user.profile.following.all()
    posts = list(request.user.post_set.all())
    for followee in following:
        posts += list(followee.user.post_set.all())

    posts.sort(key=lambda r: r.timestamp, reverse=True)
    print(len(posts))
    return render_to_response('jay/feed.html', {'posts': posts}, context)


@login_required
def profile(request, pk=None):
    context = RequestContext(request)

    user = get_user(pk, request)
    followers = user.profile.followers

    is_following = False
    if user != request.user:
        for follower in list(followers.all()):
            if request.user == follower.user:
                is_following = True
                break

    posts = Post.objects.filter(user=user).order_by('-timestamp').all()
    context_dict = {'posts': posts, 'user_data': user, 'is_following': is_following}

    return render_to_response('jay/profile.html', context_dict, context)


def get_user(pk, request):
    if not pk:
        pk = request.user.pk
    user = User.objects.get(pk=pk)
    return user


def post(request, pk):
    post = Post.objects.get(pk=pk)
    return render_to_response('jay/post.html', {'post': post}, RequestContext(request))


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


@login_required
def followers(request, pk=None):
    user = get_user(pk, request)
    followers = user.profile.followers.all()
    return render_to_response('jay/followers.html', {'followers': followers, 'user_data': user}, RequestContext(request))


@login_required
def following(request, pk=None):
    user = get_user(pk, request)
    following = user.profile.following.all()
    return render_to_response('jay/following.html', {'following': following, 'user_data': user}, RequestContext(request))


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

            resp = serialize('json', [comment, ])
            resp_obj = json.loads(resp)
            resp_obj[0]['fields']['first_name'] = request.user.first_name
            resp_obj[0]['fields']['last_name'] = request.user.last_name
            resp_obj[0]['fields']['username'] = request.user.username
            return HttpResponse(json.dumps(resp_obj))

        return HttpResponse()


@login_required
def manage_post(request):
    if request.method == 'GET':
        action = request.GET['action']
        try:
            post = None if action == 'add' else Post.objects.get(pk=request.GET['pk'])
        except Post.DoesNotExist:
            return render_to_response('jay/manage_post.html', {'user_data': request.user}, RequestContext(request))

        if action == 'delete':
            post.delete()
            return HttpResponse()
        else:
            return render_to_response('jay/manage_post.html', {'post': post, 'user_data': request.user},
                                      RequestContext(request))
    elif request.method == 'POST':  # Button add post was clicked
        post = Post.objects.get(pk=request.POST['pk']) if request.POST['pk'] else Post(user=request.user)

        post.title = request.POST['title']
        post.content = request.POST['content']

        post.save()
        return HttpResponseRedirect('/post/' + str(post.pk))


def check_email(request):
    if request.GET['email']:
        try:
            User.objects.get(email=request.GET['email'])
        except User.DoesNotExist:
            return HttpResponse(status=200)
        return HttpResponse(status=800)
    return HttpResponse(status=200)
