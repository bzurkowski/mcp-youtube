from typing import Any, Dict, List, Optional

from mcp_youtube.common.clients.youtube import YouTubeClient
from mcp_youtube.common.utils import extract_handle


def list_channels(
    channel_id: Optional[str] = None,
    handle: Optional[str] = None,
    username: Optional[str] = None,
    max_results: int = 10,
) -> List[Dict[str, Any]]:
    """
    List YouTube channel details.

    Args:
        channel_id: The YouTube channel ID to retrieve details for.
        handle: The YouTube handle to retrieve details for.
        username: The YouTube username to retrieve details for.
        max_results: Maximum number of channels to return (default: 10).

    Returns:
        A list of channel details.
    """
    params = {
        "maxResults": max_results,
        "part": "snippet,contentDetails,statistics",
    }

    if channel_id is not None:
        params["id"] = channel_id
    elif handle is not None:
        params["forHandle"] = extract_handle(handle)
    elif username is not None:
        params["forUsername"] = username

    response = YouTubeClient().channels().list(**params).execute()

    result = []
    for channel_data in response["items"]:
        snippet = channel_data.get("snippet", {})
        stats = channel_data.get("statistics", {})
        result.append(
            {
                "id": channel_data["id"],
                "title": snippet.get("title", ""),
                "description": snippet.get("description", ""),
                "published_at": snippet.get("publishedAt", ""),
                "view_count": stats.get("viewCount", 0),
                "subscriber_count": stats.get("subscriberCount", 0),
                "video_count": stats.get("videoCount", 0),
            }
        )

    return result
