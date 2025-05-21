from typing import Any, Dict, List

from mcp_youtube.common.clients.youtube import YouTubeClient
from mcp_youtube.common.utils import extract_video_id


def list_video_comments(
    video: str,
    max_results: int = 20,
    order: str = "relevance",
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
    video_id = extract_video_id(video) or video

    response = (
        YouTubeClient()
        .commentThreads()
        .list(
            part="snippet",
            videoId=video_id,
            maxResults=max_results,
            order=order,
        )
        .execute()
    )

    result = []
    for item in response.get("items", []):
        comment = item["snippet"]["topLevelComment"]["snippet"]
        result.append(
            {
                "id": item["id"],
                "author": comment["authorDisplayName"],
                "text": comment["textDisplay"],
                "like_count": comment["likeCount"],
                "published_at": comment["publishedAt"],
                "updated_at": comment["updatedAt"],
            }
        )

    return result
