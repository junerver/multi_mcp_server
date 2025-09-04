from functools import wraps

import click
from mcp.server import FastMCP
from starlette.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp


def with_mcp_options(default_port=3001):
    """
    一个封装了常用 click 选项的自定义装饰器，
    可以设置 --port 的默认值。

    Args:
        default_port (int): 用于设置 --port 选项的默认值。
    """

    def decorator(f):
        @click.command()
        @click.option(
            "--transport",
            type=click.Choice(["stdio", "streamable", "sse"]),
            default="stdio",
            help="Transport type",
        )
        @click.option("--port", type=int, default=default_port, help="Port to listen on")
        @wraps(f)
        def decorated_function(*args, **kwargs):
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def run_server_with_cors(app: ASGIApp, host: str = "0.0.0.0", port: int = 3001):
    starlette_app = CORSMiddleware(
        app,
        allow_origins=["*"],  # Allow all origins - adjust as needed for production
        allow_methods=["GET", "POST", "DELETE"],  # MCP streamable HTTP methods
        expose_headers=["Mcp-Session-Id"],
    )
    import uvicorn

    uvicorn.run(starlette_app, host=host, port=port)


def run_mcp_server(mcp: FastMCP, transport: str, host: str = "0.0.0.0", port: int = 3001):
    if transport == "sse":
        run_server_with_cors(mcp.sse_app(), host=host, port=port)
    elif transport == "streamable":
        run_server_with_cors(mcp.streamable_http_app(), host=host, port=port)
    else:
        mcp.run(transport="stdio")