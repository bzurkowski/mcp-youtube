from typing import Annotated

import typer
from mcp.server.fastmcp import FastMCP

import mcp_youtube.tools as tools
from mcp_youtube.common.enums import Transport

app = typer.Typer(
    help="YouTube MCP server",
    pretty_exceptions_short=True,
    pretty_exceptions_show_locals=False,
    no_args_is_help=True,
)


@app.command()
def main(
    transport: Annotated[
        Transport,
        typer.Option(help="Transport method"),
    ] = Transport.STDIO,
    sse_address: Annotated[
        str,
        typer.Option(help="Address for SSE transport in format host:port"),
    ] = "localhost:8000",
):
    mcp = FastMCP("YouTube")

    mcp.tool()(tools.search_videos)
    mcp.tool()(tools.list_channel_videos)
    mcp.tool()(tools.list_playlist_videos)
    mcp.tool()(tools.get_video_metadata)
    mcp.tool()(tools.get_video_comments)
    mcp.tool()(tools.get_video_transcript)
    mcp.tool()(tools.list_video_transcripts)
    mcp.tool()(tools.translate_video_transcript)

    if transport == Transport.SSE:
        host, port = sse_address.split(":")
        mcp.settings.host = host
        mcp.settings.port = int(port)

    mcp.run(transport=transport.value)


if __name__ == "__main__":
    typer.run(main)
