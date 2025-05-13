from typing import Dict, List, Optional, Any

from youtube_mcp.api.youtube import YouTubeClient
from youtube_mcp.utils.helpers import extract_playlist_id


def list_playlist_videos(playlist: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """
    List videos from a specific YouTube playlist.

    Args:
        playlist: The playlist ID or URL to list videos from.
        max_results: Maximum number of videos to return (default: 10).

    Returns:
        A list of videos from the playlist.
    """
    client = YouTubeClient()

    # Extract playlist ID if a URL was provided
    playlist_id = extract_playlist_id(playlist) or playlist

    return client.list_playlist_videos(playlist_id, max_results)
