from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from iptv.models import Video


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    context = {
        "videos": Video.objects.all().order_by("name"),
    }
    return render(request, "iptv/video_list.html", context)
