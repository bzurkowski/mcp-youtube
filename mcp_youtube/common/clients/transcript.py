from typing import Any

from youtube_transcript_api import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
    YouTubeTranscriptApi,
)

from mcp_youtube.common.exceptions import TranscriptAPIError


class TranscriptAPIClient:
    """
    A lightweight wrapper around the YouTube Transcript API.

    This class provides unified error handling for transcript operations.
    """

    def __getattr__(self, name: str) -> Any:
        attr = getattr(YouTubeTranscriptApi, name)
        if callable(attr):

            def wrapper(*args, **kwargs):
                try:
                    return attr(*args, **kwargs)
                except NoTranscriptFound:
                    raise TranscriptAPIError(
                        "No transcript found for the requested language"
                    )
                except TranscriptsDisabled:
                    raise TranscriptAPIError("Transcripts are disabled for this video")
                except VideoUnavailable:
                    raise TranscriptAPIError("The video is no longer available")
                except Exception as e:
                    raise TranscriptAPIError(
                        f"Error during transcript API call: {str(e)}"
                    )

            return wrapper
        return attr
