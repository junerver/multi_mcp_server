import logging
import sys

import click
from mcp.server import FastMCP
from mcp.types import TextContent
from starlette.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp

from common.mcp_cli import with_mcp_options, run_server_with_cors, run_mcp_server

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Create an MCP server
mcp = FastMCP("DemoMcpServer")

@mcp.tool()
def add(a: int, b: int)-> list[TextContent]:
    """Add two numbers."""
    return [TextContent(type="text", text=f"{a} + {b} = {a + b}")]


@with_mcp_options(3006)
def main(transport: str, port: int):
    """主函数，启动MCP服务器"""
    run_mcp_server(mcp, transport, port= port)


if __name__ == "__main__":
    main()
