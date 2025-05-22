# ✨ YouTube MCP Server ✨

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) server providing structured access to YouTube data for AI assistants and applications. It lets AI systems interact with YouTube content through a standardized interface. The server offers tools for searching videos, retrieving channel information, accessing transcripts, and analyzing comments.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Running with Docker](#running-with-docker)
- [Configuration](#configuration)
  - [Cursor AI](#cursor-ai)
- [Tools](#tools)
  - [search_videos](#search_videos)
  - [list_channels](#list_channels)
  - [list_playlist_videos](#list_playlist_videos)
  - [get_video_details](#get_video_details)
  - [list_video_comments](#list_video_comments)
  - [get_video_transcript](#get_video_transcript)
  - [list_video_transcripts](#list_video_transcripts)
  - [translate_video_transcript](#translate_video_transcript)

## Features

- **Video Search** - Search for videos across YouTube by keywords and filters
- **Channel Information** - Retrieve details about YouTube channels by ID, handle, or username
- **Playlist Access** - Get videos from public YouTube playlists
- **Video Metadata** - Access detailed metadata for any YouTube video
- **Comment Retrieval** - Fetch comments from YouTube videos
- **Video Transcripts** - Get and list video transcripts in multiple languages
- **Transcript Translation** - Translate video transcripts to different languages

## Installation

### Prerequisites

* [Docker](https://www.docker.com/products/docker-desktop/)
* [Google API credentials](https://developers.google.com/youtube/registering_an_application) for YouTube Data API

### Running with Docker

Build the Docker image:
```bash
docker build -t mcp-youtube .
```

Run the container:
```bash
docker run -p 8000:8000 -e YOUTUBE_API_KEY=<your_api_key> mcp-youtube
```

## Configuration

### Cursor AI

To use this MCP server with Cursor AI, add the following configuration to your MCP settings:

```json
{
  "mcp": {
    "tools": [
      {
        "name": "youtube",
        "server": {
          "url": "http://localhost:8000"
        }
      }
    ]
  }
}
```

## Tools

The following tools are available for interacting with YouTube:

### `search_videos`
Search for videos on YouTube.

**Arguments:**
- `query` (required): The search query
- `max_results` (optional, default: 10): Maximum number of results to return
- `order` (optional, default: "relevance"): Order of the results ('relevance', 'date', 'rating', 'viewCount')
- `region_code` (optional): ISO 3166-1 alpha-2 country code (e.g., 'US', 'GB')
- `language` (optional): ISO 639-1 language code (e.g., 'en', 'fr')
- `published_after` (optional): Only return videos published after this datetime (RFC 3339 format)
- `published_before` (optional): Only return videos published before this datetime (RFC 3339 format)

### `list_channels`
List YouTube channel details.

**Arguments:**
- One of the following is required:
  - `channel_id`: The YouTube channel ID to retrieve details for
  - `handle`: The YouTube handle to retrieve details for
  - `username`: The YouTube username to retrieve details for
- `max_results` (optional, default: 10): Maximum number of channels to return

### `list_playlist_videos`
List videos from a specific YouTube playlist.

**Arguments:**
- `playlist` (required): The playlist ID or URL to list videos from
- `max_results` (optional, default: 10): Maximum number of videos to return

### `get_video_details`
Get details for a specific YouTube video.

**Arguments:**
- `video` (required): The video ID or URL to get details for

### `list_video_comments`
Get comments for a specific YouTube video.

**Arguments:**
- `video` (required): The video ID or URL to get comments for
- `max_results` (optional, default: 20): Maximum number of comments to return
- `order` (optional, default: "relevance"): Order of the comments ('relevance' or 'time')

### `get_video_transcript`
Get transcript for a specific YouTube video.

**Arguments:**
- `video` (required): The video ID or URL to get transcript for
- `language_code` (required): ISO 639-1 language code of the transcript (e.g., 'en', 'fr')
- `preserve_formatting` (optional, default: false): Whether to preserve HTML formatting in the transcript
- `include_timestamps` (optional, default: false): Whether to include timestamps in the transcript

### `list_video_transcripts`
List available transcripts for a specific YouTube video.

**Arguments:**
- `video` (required): The video ID or URL to list transcripts for

### `translate_video_transcript`
Translate transcript for a specific YouTube video to the specified language.

**Arguments:**
- `video` (required): The video ID or URL to translate transcript for
- `language_code` (required): ISO 639-1 language code of the translation (e.g., 'en', 'fr').
- `preserve_formatting` (optional, default: false): Whether to preserve HTML formatting in the transcript

