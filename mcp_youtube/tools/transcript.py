from typing import Any, Dict, List

from mcp_youtube.common.clients.transcript import TranscriptAPIClient
from mcp_youtube.common.exceptions import TranscriptAPIError
from mcp_youtube.common.utils import extract_video_id


def get_video_transcript(
    video: str,
    language_code: str,
    preserve_formatting: bool = False,
    include_timestamps: bool = False,
) -> Any:
    """
    Get transcript for a specific YouTube video.

    Args:
        video: The video ID or URL to get transcript for.
        language_code: ISO 639-1 language code of the transcript (e.g., 'en', 'fr').
        preserve_formatting: Whether to preserve HTML formatting in the transcript.
        include_timestamps: Whether to include timestamps in the transcript.

    Returns:
        A list of transcript segments or a string with joined transcript text.
    """
    video_id = extract_video_id(video) or video

    response = TranscriptAPIClient().get_transcript(
        video_id,
        languages=[language_code],
        preserve_formatting=preserve_formatting,
    )

    if not include_timestamps:
        return " ".join(snippet["text"] for snippet in response)

    return response


def list_video_transcripts(video: str) -> List[Dict[str, Any]]:
    """
    List available transcripts for a specific YouTube video.

    Args:
        video: The video ID or URL to list transcripts for.

    Returns:
        A dictionary containing information about available transcripts.
    """
    video_id = extract_video_id(video) or video

    response = TranscriptAPIClient().list_transcripts(video_id)

    result = []
    for transcript in response:
        result.append(
            {
                "language": transcript.language,
                "language_code": transcript.language_code,
                "is_generated": transcript.is_generated,
                "is_translatable": transcript.is_translatable,
                "translation_languages": (
                    [
                        {
                            "language": lang.language,
                            "language_code": lang.language_code,
                        }
                        for lang in transcript.translation_languages
                    ]
                    if transcript.is_translatable
                    else []
                ),
            }
        )

    return result


def translate_video_transcript(
    video: str, language_code: str, preserve_formatting: bool = False
) -> List[Dict[str, Any]]:
    """
    Translate transcript for a specific YouTube video to the specified language.

    Args:
        video: The video ID or URL to translate transcript for.
        language_code: ISO 639-1 language code of the translation (e.g., 'en', 'fr').
        preserve_formatting: Whether to preserve HTML formatting in the transcript.

    Returns:
        A list of translated transcript segments.
    """
    video_id = extract_video_id(video) or video

    response = TranscriptAPIClient().list_transcripts(video_id)

    for transcript in response:
        if transcript.is_translatable:
            translated = transcript.translate(language_code)
            return translated.fetch(preserve_formatting=preserve_formatting)

    raise TranscriptAPIError(
        f"No translatable transcript found for video ID {video_id}"
    )
