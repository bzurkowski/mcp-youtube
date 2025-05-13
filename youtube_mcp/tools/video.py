from typing import Dict, List, Optional, Any

from youtube_mcp.api.youtube import YouTubeClient
from youtube_mcp.utils.helpers import extract_video_id, format_duration_to_seconds


def get_video_metadata(video: str) -> Dict[str, Any]:
    """
    Get metadata for a specific YouTube video.

    Args:
        video: The video ID or URL to get metadata for.

    Returns:
        A dictionary containing video metadata.
    """
    client = YouTubeClient()

    # Extract video ID if a URL was provided
    video_id = extract_video_id(video) or video

    # Get the metadata
    metadata = client.get_video_metadata(video_id)

    # Add formatted duration in seconds
    if "duration" in metadata:
        metadata["duration_seconds"] = format_duration_to_seconds(metadata["duration"])

    return metadata


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

    # Extract video ID if a URL was provided
    video_id = extract_video_id(video) or video

    return client.get_video_comments(video_id, max_results, order)
