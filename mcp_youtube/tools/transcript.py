from typing import Dict, List, Optional, Any

from mcp_youtube.common.clients.transcript import TranscriptAPIClient
from mcp_youtube.common.utils import extract_video_id


def get_video_transcript(
    video: str, languages: Optional[List[str]] = None, preserve_formatting: bool = False
) -> List[Dict[str, Any]]:
    """
    Get transcript for a specific YouTube video.

    Args:
        video: The video ID or URL to get transcript for.
        languages: List of language codes in descending priority (default: ['en']).
        preserve_formatting: Whether to preserve HTML formatting in the transcript.

    Returns:
        A list of transcript segments.
    """
    client = TranscriptAPIClient()

    # Extract video ID if a URL was provided
    video_id = extract_video_id(video) or video

    return client.get_transcript(video_id, languages, preserve_formatting)


def list_video_transcripts(video: str) -> Dict[str, Any]:
    """
    List available transcripts for a specific YouTube video.

    Args:
        video: The video ID or URL to list transcripts for.

    Returns:
        A dictionary containing information about available transcripts.
    """
    client = TranscriptAPIClient()

    # Extract video ID if a URL was provided
    video_id = extract_video_id(video) or video

    return client.list_transcripts(video_id)


def translate_video_transcript(
    video: str, language_code: str, preserve_formatting: bool = False
) -> List[Dict[str, Any]]:
    """
    Translate transcript for a specific YouTube video to the specified language.

    Args:
        video: The video ID or URL to translate transcript for.
        language_code: The language code to translate the transcript to.
        preserve_formatting: Whether to preserve HTML formatting in the transcript.

    Returns:
        A list of translated transcript segments.
    """
    client = TranscriptAPIClient()

    # Extract video ID if a URL was provided
    video_id = extract_video_id(video) or video

    return client.translate_transcript(video_id, language_code, preserve_formatting)
