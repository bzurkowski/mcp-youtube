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

    mcp.add_tool(tools.get_video_details)
    mcp.add_tool(tools.get_video_transcript)
    mcp.add_tool(tools.list_playlist_videos)
    mcp.add_tool(tools.list_video_comments)
    mcp.add_tool(tools.list_video_transcripts)
    mcp.add_tool(tools.search_videos)
    mcp.add_tool(tools.translate_video_transcript)

    if transport == Transport.SSE:
        host, port = sse_address.split(":")
        mcp.settings.host = host
        mcp.settings.port = int(port)

    mcp.run(transport=transport.value)


if __name__ == "__main__":
    typer.run(main)
