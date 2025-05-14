from typing import Dict, List, Optional, Any

from mcp_youtube.common.clients.youtube import YouTubeClient
from mcp_youtube.common.utils import extract_channel_id


def list_channel_videos(
    channel: str, max_results: int = 10, order: str = "date"
) -> List[Dict[str, Any]]:
    """
    List videos from a specific YouTube channel.

    Args:
        channel: The channel ID or URL to list videos from.
        max_results: Maximum number of videos to return (default: 10).
        order: Order of the videos ('date', 'rating', 'title', 'viewCount').

    Returns:
        A list of videos from the channel.
    """
    client = YouTubeClient()

    # Extract channel ID if a URL was provided
    channel_id = extract_channel_id(channel) or channel

    return client.list_channel_videos(channel_id, max_results, order)
