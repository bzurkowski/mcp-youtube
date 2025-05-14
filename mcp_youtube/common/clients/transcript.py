from typing import Any, Dict, List, Optional

from youtube_transcript_api import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
    YouTubeTranscriptApi,
)


class TranscriptAPIClient:
    """
    A client for retrieving video transcripts using youtube-transcript-api.
    """

    def get_transcript(
        self,
        video_id: str,
        languages: Optional[List[str]] = None,
        preserve_formatting: bool = False,
    ) -> List[Dict[str, Any]]:
        try:
            languages = languages or ["en"]
            transcript = YouTubeTranscriptApi.get_transcript(
                video_id, languages=languages, preserve_formatting=preserve_formatting
            )
            return transcript
        except NoTranscriptFound:
            # No transcript is available for the requested languages
            raise Exception(
                f"No transcript found for video ID {video_id} in languages: {languages}"
            )
        except TranscriptsDisabled:
            # Transcripts are disabled for this video
            raise Exception(f"Transcripts are disabled for video ID {video_id}")
        except VideoUnavailable:
            # The video is no longer available
            raise Exception(f"Video with ID {video_id} is unavailable")
        except Exception as e:
            raise Exception(f"Error retrieving transcript: {str(e)}")

    def list_transcripts(self, video_id: str) -> Dict[str, Any]:
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

            # Format the response
            available_transcripts = []
            for transcript in transcript_list:
                available_transcripts.append(
                    {
                        "language": transcript.language,
                        "language_code": transcript.language_code,
                        "is_generated": transcript.is_generated,
                        "is_translatable": transcript.is_translatable,
                        "translation_languages": (
                            [
                                {
                                    "language": lang["language"],
                                    "language_code": lang["language_code"],
                                }
                                for lang in transcript.translation_languages
                            ]
                            if transcript.is_translatable
                            else []
                        ),
                    }
                )

            return {
                "video_id": video_id,
                "available_transcripts": available_transcripts,
            }
        except TranscriptsDisabled:
            # Transcripts are disabled for this video
            return {
                "video_id": video_id,
                "available_transcripts": [],
                "error": "Transcripts are disabled for this video",
            }
        except VideoUnavailable:
            # The video is no longer available
            return {
                "video_id": video_id,
                "available_transcripts": [],
                "error": "Video is unavailable",
            }
        except Exception as e:
            return {"video_id": video_id, "available_transcripts": [], "error": str(e)}

    def translate_transcript(
        self, video_id: str, language_code: str, preserve_formatting: bool = False
    ) -> List[Dict[str, Any]]:
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

            # Find any available transcript that can be translated
            for transcript in transcript_list:
                if transcript.is_translatable:
                    translated_transcript = transcript.translate(language_code)
                    return translated_transcript.fetch(
                        preserve_formatting=preserve_formatting
                    )

            raise Exception(f"No translatable transcript found for video ID {video_id}")
        except NoTranscriptFound:
            # No transcript is available for the requested language
            raise Exception(
                f"No transcript found that can be translated to {language_code}"
            )
        except TranscriptsDisabled:
            # Transcripts are disabled for this video
            raise Exception(f"Transcripts are disabled for video ID {video_id}")
        except VideoUnavailable:
            # The video is no longer available
            raise Exception(f"Video with ID {video_id} is unavailable")
        except Exception as e:
            raise Exception(f"Error translating transcript: {str(e)}")
