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
    """
    运行MCP服务器，支持多种传输方式
    
    Args:
        mcp: FastMCP服务器实例
        transport: 传输方式 ("stdio", "sse", "streamable")
        host: 服务器主机地址
        port: 服务器端口
    """
    if transport == "sse":
        run_server_with_cors(mcp.sse_app(), host=host, port=port)
    elif transport == "streamable":
        run_server_with_cors(mcp.streamable_http_app(), host=host, port=port)
    else:
        # 在Windows系统上使用stdio时，需要处理stdout flush的问题
        import sys
        import os
        
        # 检查是否在Windows系统上
        if os.name == 'nt':
            # 在Windows上，重定向stderr到避免flush错误
            import io
            import contextlib
            
            # 创建一个自定义的stdout包装器来处理flush错误
            class SafeStdout:
                def __init__(self, original_stdout):
                    self.original_stdout = original_stdout
                
                def write(self, data):
                    return self.original_stdout.write(data)
                
                def flush(self):
                    try:
                        return self.original_stdout.flush()
                    except OSError:
                        # 忽略Windows上的flush错误
                        pass
                
                def __getattr__(self, name):
                    return getattr(self.original_stdout, name)
            
            # 临时替换stdout
            original_stdout = sys.stdout
            sys.stdout = SafeStdout(original_stdout)
            
            try:
                mcp.run(transport="stdio")
            finally:
                # 恢复原始stdout
                sys.stdout = original_stdout
        else:
            mcp.run(transport="stdio")