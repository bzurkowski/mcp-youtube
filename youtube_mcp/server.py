import argparse
from mcp.server.fastmcp import FastMCP

import youtube_mcp.tools as tools


def main():
    parser = argparse.ArgumentParser(description="YouTube MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default="stdio",
        help="Transport method (stdio, sse, or streamable-http)",
    )
    parser.add_argument(
        "--sse-address",
        default="127.0.0.1:8000",
        help="Address for SSE transport in format host:port",
    )
    args = parser.parse_args()

    mcp = FastMCP("YouTube")

    mcp.tool()(tools.search_videos)
    mcp.tool()(tools.list_channel_videos)
    mcp.tool()(tools.list_playlist_videos)
    mcp.tool()(tools.get_video_metadata)
    mcp.tool()(tools.get_video_comments)
    mcp.tool()(tools.get_video_transcript)
    mcp.tool()(tools.list_video_transcripts)
    mcp.tool()(tools.translate_video_transcript)

    if args.transport == "sse":
        host, port = args.sse_address.split(":")
        mcp.settings.host = host
        mcp.settings.port = int(port)

    mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()
