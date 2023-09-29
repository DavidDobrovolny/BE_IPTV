import io
import os
from typing import Any

import requests

from .models import Video


def download_all() -> None:
    """
    Downloads and saves all videos from the API.
    """
    API_URL = os.environ.get("API_URL")
    assert API_URL is not None

    result = requests.get(API_URL)
    for video in result.json():
        save_video(video)


def save_video(data: dict[str, Any]) -> None:
    """
    Saves the video data given in JSON into the database,
    downloads the icon and saves the modification time.

    Args:
        data (dict[str, Any]): Input JSON file with video data.
    """
    name = data.get("name")
    description = data.get("description")

    features = data.get("features", [])
    has_subtitles = "DEMO_SUBTITLES" in features
    is_multilingual = "DEMO_MULTIPLE_LANGUAGES" in features
    is_hd = "DEMO_HIGH_DEFINITION" in features
    is_uhd = "DEMO_ULTRA_HIGH_DEFINITION" in features

    new_video, _ = Video.objects.update_or_create(
        name=name,
        defaults={
            "raw": data,
            "description": description,
            "has_subtitles": has_subtitles,
            "is_multilingual": is_multilingual,
            "is_hd": is_hd,
            "is_uhd": is_uhd,
        },
    )

    icon_uri = data.get("iconUri")
    if icon_uri and (icon := download_icon(icon_uri)):
        new_video.icon.delete()
        new_video.icon.save(icon_uri.split("/")[-1], icon)

    new_video.save()


def download_icon(uri: str) -> io.BytesIO | None:
    """
    Downloads an icon from a given URI and returns it as a binary file-like object.

    Args:
        uri (str): URI to download the icon from.

    Returns (io.BytesIO): binary file-like object containing the icon

    """
    if not uri:
        return None

    try:
        result = requests.get(uri, stream=True)
    except requests.exceptions.ConnectionError:
        return None

    if result.status_code == 200:
        return io.BytesIO(result.content)

    return None
