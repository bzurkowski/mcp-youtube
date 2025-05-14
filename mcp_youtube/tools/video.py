from typing import Any, Dict, List

from mcp_youtube.common.clients.youtube import YouTubeClient
from mcp_youtube.common.utils import extract_video_id


def get_video_metadata(video: str) -> Dict[str, Any]:
    """
    Get metadata for a specific YouTube video.

    Args:
        video: The video ID or URL to get metadata for.

    Returns:
        A dictionary containing video metadata.
    """
    client = YouTubeClient()
    video_id = extract_video_id(video) or video
    return client.get_video_metadata(video_id)


def get_video_comments(
    video: str, max_results: int = 20, order: str = "relevance"
) -> List[Dict[str, Any]]:
    """
    Get comments for a specific YouTube video.

    Args:
        video: The video ID or URL to get comments for.
        max_results: Maximum number of comments to return (default: 20).
        order: Order of the comments ('relevance' or 'time').

    Returns:
        A list of comments for the video.
    """
    client = YouTubeClient()
    video_id = extract_video_id(video) or video
    return client.get_video_comments(video_id, max_results, order)
