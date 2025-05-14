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


def extract_channel_id(url: str) -> Optional[str]:
    # Check for channel URL format
    if "youtube.com/channel/" in url:
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.split("/")
        for i, part in enumerate(path_parts):
            if part == "channel" and i + 1 < len(path_parts):
                return path_parts[i + 1]

    # Check if the input is already a channel ID (starts with UC)
    if re.match(r"^UC[a-zA-Z0-9_-]+$", url):
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


def format_duration_to_seconds(duration: str) -> int:
    match = re.match(
        r"P(?:(?P<days>\d+)D)?T"
        r"(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?(?:(?P<seconds>\d+)S)?",
        duration,
    )
    if not match:
        return 0

    match_dict = match.groupdict(default="0")
    days = int(match_dict["days"])
    hours = int(match_dict["hours"])
    minutes = int(match_dict["minutes"])
    seconds = int(match_dict["seconds"])

    return days * 86400 + hours * 3600 + minutes * 60 + seconds
