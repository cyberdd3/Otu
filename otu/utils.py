import json
import os
from PIL import Image
import datetime
from django.http import HttpResponse
from django.utils import dateformat
from otu.models import Message


def manage_avatar(img, img_path):
    small = 50
    medium = 200

    width, height = img.size
    ratio = width / height

    img.save(img_path + "_full.jpg", "JPEG")

    if ratio < 1:
        new_small_size = (small * ratio, small)
        new_med_size = (medium * ratio, medium)
    else:
        new_small_size = (small, small * ratio)
        new_med_size = (medium, medium * ratio)

    img.thumbnail(new_med_size, Image.ANTIALIAS)
    img.save(img_path + '_med.jpg', "JPEG", quality=95)

    img.thumbnail(new_small_size, Image.ANTIALIAS)
    img.save(img_path + '_small.jpg', 'JPEG', quality=95)


    os.remove(img_path)

def json_response(obj):
    return HttpResponse(json.dumps(obj), content_type='application/json')