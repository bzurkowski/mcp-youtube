import os
from typing import Any, Dict, List, Optional

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class YouTubeClient:
    """
    A client for interacting with the YouTube Data API v3.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("YOUTUBE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "No API key provided. Please provide an API key or "
                "set the YOUTUBE_API_KEY environment variable."
            )
        self.youtube = build("youtube", "v3", developerKey=self.api_key)

    def search_videos(
        self,
        query: str,
        max_results: int = 10,
        order: str = "relevance",
        region_code: Optional[str] = None,
        language: Optional[str] = None,
        published_after: Optional[str] = None,
        published_before: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        try:
            search_response = (
                self.youtube.search()
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

            videos = []
            for item in search_response.get("items", []):
                video_data = {
                    "id": item["id"]["videoId"],
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "published_at": item["snippet"]["publishedAt"],
                    "channel_id": item["snippet"]["channelId"],
                    "channel_title": item["snippet"]["channelTitle"],
                    "thumbnail_url": item["snippet"]["thumbnails"]["default"]["url"],
                }
                videos.append(video_data)

            return videos
        except HttpError as e:
            raise Exception(f"An HTTP error occurred: {e.resp.status} {e.content}")

    def get_video_metadata(self, video_id: str) -> Dict[str, Any]:
        try:
            video_response = (
                self.youtube.videos()
                .list(part="snippet,contentDetails,statistics", id=video_id)
                .execute()
            )

            if not video_response.get("items"):
                raise Exception(f"Video not found with ID: {video_id}")

            video_data = video_response["items"][0]

            metadata = {
                "id": video_data["id"],
                "title": video_data["snippet"]["title"],
                "description": video_data["snippet"]["description"],
                "published_at": video_data["snippet"]["publishedAt"],
                "channel_id": video_data["snippet"]["channelId"],
                "channel_title": video_data["snippet"]["channelTitle"],
                "tags": video_data["snippet"].get("tags", []),
                "category_id": video_data["snippet"].get("categoryId"),
                "duration": video_data["contentDetails"]["duration"],
                "view_count": video_data["statistics"].get("viewCount", 0),
                "like_count": video_data["statistics"].get("likeCount", 0),
                "comment_count": video_data["statistics"].get("commentCount", 0),
            }

            return metadata
        except HttpError as e:
            raise Exception(f"An HTTP error occurred: {e.resp.status} {e.content}")

    def get_video_comments(
        self, video_id: str, max_results: int = 20, order: str = "relevance"
    ) -> List[Dict[str, Any]]:
        try:
            comments_response = (
                self.youtube.commentThreads()
                .list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=max_results,
                    order=order,
                )
                .execute()
            )

            comments = []
            for item in comments_response.get("items", []):
                comment = item["snippet"]["topLevelComment"]["snippet"]
                comment_data = {
                    "id": item["id"],
                    "author": comment["authorDisplayName"],
                    "text": comment["textDisplay"],
                    "like_count": comment["likeCount"],
                    "published_at": comment["publishedAt"],
                    "updated_at": comment["updatedAt"],
                }
                comments.append(comment_data)

            return comments
        except HttpError as e:
            # Comments might be disabled for the video
            if e.resp.status == 403:
                return []
            raise Exception(f"An HTTP error occurred: {e.resp.status} {e.content}")

    def list_channel_videos(
        self, channel_id: str, max_results: int = 10, order: str = "date"
    ) -> List[Dict[str, Any]]:
        try:
            # First, get the upload playlist ID for the channel
            channel_response = (
                self.youtube.channels()
                .list(part="contentDetails", id=channel_id)
                .execute()
            )

            if not channel_response.get("items"):
                raise Exception(f"Channel not found with ID: {channel_id}")

            uploads_playlist_id = channel_response["items"][0]["contentDetails"][
                "relatedPlaylists"
            ]["uploads"]

            # Then, get the videos from the uploads playlist
            return self.list_playlist_videos(uploads_playlist_id, max_results, order)
        except HttpError as e:
            raise Exception(f"An HTTP error occurred: {e.resp.status} {e.content}")

    def list_playlist_videos(
        self, playlist_id: str, max_results: int = 10, order: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        try:
            # Note: order parameter is not supported for playlist items,
            # but included for API consistency
            playlist_response = (
                self.youtube.playlistItems()
                .list(
                    part="snippet,contentDetails",
                    playlistId=playlist_id,
                    maxResults=max_results,
                )
                .execute()
            )

            videos = []
            for item in playlist_response.get("items", []):
                video_data = {
                    "id": item["contentDetails"]["videoId"],
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "published_at": item["snippet"]["publishedAt"],
                    "channel_id": item["snippet"]["channelId"],
                    "channel_title": item["snippet"]["channelTitle"],
                    "position": item["snippet"]["position"],
                    "thumbnail_url": (
                        item["snippet"]["thumbnails"]["default"]["url"]
                        if "thumbnails" in item["snippet"]
                        else None
                    ),
                }
                videos.append(video_data)

            return videos
        except HttpError as e:
            raise Exception(f"An HTTP error occurred: {e.resp.status} {e.content}")
