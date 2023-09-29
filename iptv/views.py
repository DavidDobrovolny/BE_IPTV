from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from iptv.models import Video


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    search_name = request.GET.get("search_name", "")
    has_subtitles = request.GET.get("has_subtitles", "None")
    is_multilingual = request.GET.get("is_multilingual", "None")
    quality = request.GET.get("quality", "None")
    sort_by = request.GET.get("sort_by", "AZ")

    videos = Video.objects.all()
    videos = videos.filter(name__icontains=search_name)
    videos = filter_subtitles(videos, has_subtitles)
    videos = filter_multilingual(videos, is_multilingual)
    videos = filter_quality(videos, quality)
    videos = videos.order_by("name" if sort_by == "AZ" else "-name")

    context = {
        "videos": videos,
        "search_name": search_name,
        "has_subtitles": has_subtitles,
        "is_multilingual": is_multilingual,
        "quality": quality,
        "sort_by": sort_by,
    }
    return render(request, "iptv/video_list.html", context)


def filter_subtitles(videos: QuerySet[Video], value: str) -> QuerySet[Video]:
    if value == "True":
        return videos.filter(has_subtitles=True)
    elif value == "False":
        return videos.filter(has_subtitles=False)

    return videos


def filter_multilingual(videos: QuerySet[Video], value: str) -> QuerySet[Video]:
    if value == "True":
        return videos.filter(is_multilingual=True)
    elif value == "False":
        return videos.filter(is_multilingual=False)

    return videos


def filter_quality(videos: QuerySet[Video], value: str) -> QuerySet[Video]:
    if value == "HD":
        return videos.filter(is_hd=True)
    elif value == "UHD":
        return videos.filter(is_uhd=True)

    return videos
