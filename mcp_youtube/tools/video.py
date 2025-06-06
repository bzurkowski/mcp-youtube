from typing import Any, Dict

from mcp_youtube.common.clients.youtube import YouTubeClient
from mcp_youtube.common.exceptions import YouTubeAPIError
from mcp_youtube.common.utils import extract_video_id


def get_video_details(
    video: str,
) -> Dict[str, Any]:
    """
    Get details for a specific YouTube video.

    Args:
        video: The video ID or URL to get details for.

    Returns:
        A dictionary containing video details.
    """
    video_id = extract_video_id(video) or video

    response = (
        YouTubeClient()
        .videos()
        .list(part="snippet,contentDetails,statistics", id=video_id)
        .execute()
    )

    if not response.get("items"):
        raise YouTubeAPIError("Video not found")

    video_data = response["items"][0]
    snippet = video_data["snippet"]
    stats = video_data["statistics"]

    return {
        "id": video_data["id"],
        "title": snippet["title"],
        "description": snippet["description"],
        "published_at": snippet["publishedAt"],
        "channel_id": snippet["channelId"],
        "channel_title": snippet["channelTitle"],
        "tags": snippet.get("tags", []),
        "duration": video_data["contentDetails"]["duration"],
        "view_count": stats.get("viewCount", 0),
        "like_count": stats.get("likeCount", 0),
        "comment_count": stats.get("commentCount", 0),
    }
