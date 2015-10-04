from django.contrib.auth.models import User
from django.http import HttpResponse


def check_email(request):
    if request.GET['email']:
        try:
            User.objects.get(username=request.GET['email'])
        except User.DoesNotExist:
            return HttpResponse("0")
        return HttpResponse("1")
    return HttpResponse("0")
