import re
from typing import Optional
from urllib.parse import parse_qs, urlparse


def extract_video_id(url: str) -> Optional[str]:
    # Check for youtu.be format
    if "youtu.be" in url:
        parsed_url = urlparse(url)
        return parsed_url.path.lstrip("/")

    # Check for youtube.com format
    if "youtube.com" in url:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        if "v" in query_params:
            return query_params["v"][0]

    # Check if the input is already a video ID (alphanumeric, underscore, and hyphen)
    if re.match(r"^[a-zA-Z0-9_-]{11}$", url):
        return url

    return None


def extract_playlist_id(url: str) -> Optional[str]:
    # Check for playlist URL format
    if "youtube.com" in url:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        if "list" in query_params:
            return query_params["list"][0]

    # Check if the input is already a playlist ID (starts with PL, UU, or FL)
    if re.match(r"^(PL|UU|FL)[a-zA-Z0-9_-]+$", url):
        return url

    return None


def extract_handle(handle: str) -> str:
    return handle if handle.startswith("@") else f"@{handle}"
