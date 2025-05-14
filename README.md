# ✨ YouTube MCP Server ✨

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) server providing structured access to YouTube data for AI assistants and applications. It lets AI systems interact with YouTube content through a standardized interface. The server offers tools for searching videos, retrieving channel information, accessing transcripts, and analyzing comments through clean, structured API endpoints.

## Table of Contents

- [Features](#features)
- [Tools](#tools)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Local package installation](#local-package-installation)
  - [Running with Docker](#running-with-docker)
- [Configuration](#configuration)
  - [YouTube API Credentials](#youtube-api-credentials)
  - [Server Configuration](#server-configuration)
- [Usage](#usage)
  - [Command line](#command-line)
  - [Cursor AI](#cursor-ai)

## Features

- **Video Search** - Search for videos across YouTube by keywords and filters
- **Channel Data** - Retrieve videos from specific YouTube channels
- **Playlist Access** - Get videos from public YouTube playlists
- **Video Metadata** - Access detailed metadata for any YouTube video
- **Comment Retrieval** - Fetch comments from YouTube videos
- **Video Transcripts** - Get video transcripts in multiple languages

## Tools

| Tool | Description |
|------|-------------|
| `search_videos` | Search for YouTube videos by keywords and optional parameters |
| `list_channel_videos` | Retrieve videos from a specific YouTube channel |
| `list_playlist_videos` | Get videos from a YouTube playlist |
| `get_video_metadata` | Fetch detailed metadata for a YouTube video |
| `get_video_comments` | Retrieve comments from a YouTube video |
| `get_video_transcript` | Get the transcript for a YouTube video |

## Installation

### Prerequisites

* [uv](https://github.com/astral-sh/uv) package manager
* Python `3.11` or higher (`uv python install`)
* [Google API credentials](https://developers.google.com/youtube/registering_an_application) for YouTube Data API

### Local package installation

You can install the server locally using the `uv` package manager:

```bash
# Install directly from the repository
uv tool install --repo https://github.com/bzurkowski/mcp-youtube mcp-youtube

# Or, if you have cloned the repository
cd mcp-youtube
uv tool install .
```

After installation, the `mcp-youtube` command will be available globally.

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

### YouTube API Credentials

1. Create a project in the [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the YouTube Data API v3
3. Create API credentials
4. Set the API key in environment variables:

   ```bash
   export YOUTUBE_API_KEY=your_api_key
   ```

### Server Configuration

| Option | Description | Default |
|--------|-------------|---------|
| `--transport` | Transport method (stdio/sse) | stdio |
| `--sse-address` | Address for SSE transport (host:port) | localhost:8000 |

## Usage

### Command line

Run the server with the default STDIO transport:

```bash
mcp-youtube
```

Run with Server-Sent Events (SSE) transport:

```bash
mcp-youtube --transport sse --sse-address localhost:8000
```

### Cursor AI

To use this MCP server with Cursor AI, add the following configuration to your MCP settings:

```json
{
  "mcp": {
    "tools": [
      {
        "name": "youtube",
        "server": {
          "type": "http",
          "url": "http://localhost:8000"
        }
      }
    ]
  }
}
```
```


