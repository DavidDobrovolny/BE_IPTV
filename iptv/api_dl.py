import io
import logging
import os
from typing import Any

import requests

from .models import Video


def download_all() -> None:
    """
    Downloads and saves all videos from the API.
    If the request fails or returns with HTTP error downloading is skipped.
    """
    API_URL = os.environ.get("API_URL")
    assert API_URL is not None, "API URL was not provided in the environment variable"

    try:
        result = requests.get(API_URL)
        result.raise_for_status()
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
        logging.warning(f"API request failed. Reason: {e}")
        return

    for video in result.json():
        save_video(video)


def save_video(data: dict[str, Any]) -> None:
    """
    Saves the video data given in JSON into the database,
    downloads the icon and saves the modification time.
    If the video name is empty, ignores the video.

    Args:
        data (dict[str, Any]): Input JSON file with video data.
    """
    name = data.get("name")
    if not name:
        return

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

    if (icon_uri := data.get("iconUri")) and (icon := download_icon(icon_uri)):
        new_video.icon.delete()
        new_video.icon.save(icon_uri.split("/")[-1], icon)

    new_video.save()


def download_icon(uri: str) -> io.BytesIO | None:
    """
    Downloads an icon from a given URI and returns it as a binary file-like object.

    Args:
        uri (str): URI to download the icon from.

    Returns (io.BytesIO): binary file-like object containing the icon or None if request fails

    """
    try:
        result = requests.get(uri, stream=True)
        result.raise_for_status()
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError):
        return None

    return io.BytesIO(result.content)
