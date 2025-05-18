import os
from typing import Any, Optional

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from mcp_youtube.common.exceptions import YouTubeAPIError


class YouTubeClient:
    """
    A lightweight wrapper around the YouTube Data API v3 client.

    This class provides unified error handling for YouTube operations.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("YOUTUBE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "No API key provided. Please provide an API key or "
                "set the YOUTUBE_API_KEY environment variable."
            )
        self.client = build("youtube", "v3", developerKey=self.api_key)

    def __getattr__(self, name: str) -> Any:
        attr = getattr(self.client, name)
        if callable(attr):

            def wrapper(*args, **kwargs):
                try:
                    return attr(*args, **kwargs)
                except HttpError as e:
                    raise YouTubeAPIError(
                        f"YouTube API error: {e.status_code} - {e.reason}"
                    ) from e
                except Exception as e:
                    raise YouTubeAPIError(
                        f"Error during YouTube API call: {str(e)}"
                    ) from e

            return wrapper
        return attr
