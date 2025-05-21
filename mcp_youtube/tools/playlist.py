from typing import Any, Dict, List

from mcp_youtube.common.clients.youtube import YouTubeClient
from mcp_youtube.common.utils import extract_playlist_id


def list_playlist_videos(
    playlist: str,
    max_results: int = 10,
) -> List[Dict[str, Any]]:
    """
    List videos from a specific YouTube playlist.

    Args:
        playlist: The playlist ID or URL to list videos from.
        max_results: Maximum number of videos to return (default: 10).

    Returns:
        A list of videos from the playlist.
    """
    playlist_id = extract_playlist_id(playlist) or playlist

    response = (
        YouTubeClient()
        .playlistItems()
        .list(
            part="snippet,contentDetails",
            playlistId=playlist_id,
            maxResults=max_results,
        )
        .execute()
    )

    result = []
    for item in response.get("items", []):
        snippet = item["snippet"]
        result.append(
            {
                "id": item["contentDetails"]["videoId"],
                "title": snippet["title"],
                "description": snippet["description"],
                "published_at": snippet["publishedAt"],
                "channel_id": snippet["channelId"],
                "channel_title": snippet["channelTitle"],
            }
        )

    return result
