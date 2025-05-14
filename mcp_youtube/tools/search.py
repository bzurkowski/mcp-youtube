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
    client = YouTubeClient()
    return client.search_videos(
        query,
        max_results,
        order,
        region_code,
        language,
        published_after,
        published_before,
    )
