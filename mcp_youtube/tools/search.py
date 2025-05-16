from typing import Any, Dict, List, Optional

from mcp_youtube.common.clients.youtube import YouTubeClient


def search_videos(
    query: str,
    max_results: int = 10,
    order: str = "relevance",
    region_code: Optional[str] = None,
    language: Optional[str] = None,
    published_after: Optional[str] = None,
    published_before: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Search for videos on YouTube.

    Args:
        query: The search query.
        max_results: Maximum number of results to return (default: 10).
        order: Order of the results ('relevance', 'date', 'rating', 'viewCount').
        region_code: ISO 3166-1 alpha-2 country code (e.g., 'US', 'GB').
        language: ISO 639-1 language code (e.g., 'en', 'fr').
        published_after: Only return videos published after this datetime
            (RFC 3339 format).
        published_before: Only return videos published before this datetime
            (RFC 3339 format).

    Returns:
        A list of video items matching the search criteria.
    """
    search_response = (
        YouTubeClient()
        .search()
        .list(
            q=query,
            part="id,snippet",
            maxResults=max_results,
            type="video",
            order=order,
            regionCode=region_code,
            relevanceLanguage=language,
            publishedAfter=published_after,
            publishedBefore=published_before,
        )
        .execute()
    )

    result = []
    for item in search_response.get("items", []):
        snippet = item["snippet"]
        video_data = {
            "id": item["id"]["videoId"],
            "title": snippet["title"],
            "description": snippet["description"],
            "published_at": snippet["publishedAt"],
            "channel_id": snippet["channelId"],
            "channel_title": snippet["channelTitle"],
        }
        result.append(video_data)

    return result
