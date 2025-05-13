#!/usr/bin/env python
import os
from mcp.server.fastmcp import FastMCP

import youtube_mcp.tools as tools

mcp = FastMCP("YouTube")

mcp.tool()(tools.search_videos)
mcp.tool()(tools.list_channel_videos)
mcp.tool()(tools.list_playlist_videos)
mcp.tool()(tools.get_video_metadata)
mcp.tool()(tools.get_video_comments)
mcp.tool()(tools.get_video_transcript)
mcp.tool()(tools.list_video_transcripts)
mcp.tool()(tools.translate_video_transcript)
