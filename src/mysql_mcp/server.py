import logging
import os
import sys
from pathlib import Path
from typing import Annotated

import click
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
from mysql.connector import connect, Error
from pydantic import Field
from starlette.middleware.cors import CORSMiddleware

from mysql_mcp.cache import Cache
from mysql_mcp.types import MysqlDatabaseConfig

# 从 .env 文件读取环境变量
env_file = Path(__file__).parent.parent.parent / ".env"
if env_file.exists():
    # 加载 .env 文件
    load_dotenv(env_file)

# 配置log工具
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("mysql_mcp_server")

# 创建全局缓存实例
cache = Cache()

# 读取数据库配置
def get_db_config() -> MysqlDatabaseConfig:
    """Get database configuration from environment variables."""
    # 配置信息从环境变量中读取
    config: MysqlDatabaseConfig = {
        "host": os.getenv("MYSQL_HOST", "localhost"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER", ""),
        "password": os.getenv("MYSQL_PASSWORD", ""),
        "database": os.getenv("MYSQL_DATABASE", ""),
    }
    # 缺少配置信息时抛出错误
    if not all([config["user"], config["password"], config["database"]]):
        logger.error("Missing required database configuration. Please check environment variables:")
        logger.error("MYSQL_USER, MYSQL_PASSWORD, and MYSQL_DATABASE are required")
        raise ValueError("Missing required database configuration")

    return config


# 初始化mcp服务
mcp = FastMCP("mysql_mcp_server")


# 读取资源
@mcp.resource("mysql://{table_name}/data")
def read_resource(table_name: Annotated[str, Field(description="Name of the table to read")]) -> str:
    """Read table contents."""
    config = get_db_config()
    uri_str = f"mysql://{table_name}/data"  # 资源uri转换为字符串
    logger.info(f"Reading resource: {uri_str}")
    # 资源必须是 mysql:// 开头
    if not uri_str.startswith("mysql://"):
        raise ValueError(f"Invalid URI scheme: {uri_str}")

    parts = uri_str[8:].split("/")
    table = parts[0]

    try:
        with connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {table} LIMIT 100")
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                result = [",".join(map(str, row)) for row in rows]
                return "\n".join([",".join(columns)] + result)

    except Error as e:
        logger.error(f"Database error reading resource {table_name}: {str(e)}")
        raise RuntimeError(f"Database error: {str(e)}")


@mcp.tool()
def read_query(query: Annotated[str, Field(description="SELECT SQL query to execute")]) -> list[TextContent]:
    """Execute a SELECT query on the MySQL database and return the results."""
    config = get_db_config()
    logger.info(f"执行查询: {query}")
    if not query.upper().startswith("SELECT"):
        raise ValueError("read_query 只允许 SELECT 查询")
    try:
        with connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                result = [",".join(columns)]
                result.extend([",".join(map(str, row)) for row in rows])
                return [TextContent(type="text", text="\n".join(result))]
    except Error as e:
        logger.error(f"数据库错误: {str(e)}")
        raise RuntimeError(f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"执行错误: {str(e)}")
        raise RuntimeError(f"Execution error: {str(e)}")


@mcp.tool()
def describe_table(table_name: Annotated[str, Field(description="Name of the table to describe")]) -> list[TextContent]:
    """Get the schema information for a specific table"""
    config = get_db_config()
    logger.info(f"获取表 {table_name} 的结构")
    cache_key = f"table_structure_{config['database']}_{table_name}"
    cached_result = cache.get(cache_key)
    if cached_result:
        logger.info(f"从缓存获取表 {table_name} 的结构")
        return [TextContent(type="text", text=cached_result)]
    try:
        with connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SHOW FULL COLUMNS FROM {table_name}")
                columns = cursor.fetchall()
                # 格式化表结构信息
                result = [f"Table {table_name} structure:"]
                # 字段名、类型、是否为空、主键、默认值、额外信息、注释
                result.append("Field | Type | Null | Key | Default | Extra | Comment")
                result.append("-" * 80)
                for col in columns:
                    # 处理每个字段的信息，包括注释
                    field_info = [
                        str(col[0]),  # Field
                        str(col[1]),  # Type
                        str(col[3]),  # Null
                        str(col[4]),  # Key
                        str(col[5]) if col[5] is not None else "NULL",  # Default
                        str(col[6]) if col[6] is not None else "",  # Extra
                        str(col[8]) if col[8] is not None else "",  # Comment
                    ]
                    result.append(" | ".join(field_info))

                result_text = "\n".join(result)
                # 存入缓存
                cache.set(cache_key, result_text)
                return [TextContent(type="text", text=result_text)]
    except Error as e:
        logger.error(f"数据库错误: {str(e)}")
        raise RuntimeError(f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"执行错误: {str(e)}")
        raise RuntimeError(f"Execution error: {str(e)}")


@mcp.tool()
def list_tables() -> list[TextContent]:
    """List all tables in the SQLite database"""
    config = get_db_config()
    logger.info("获取数据库中的所有表")
    cache_key = f"tables_{config['database']}"
    cached_result = cache.get(cache_key)
    if cached_result:
        logger.info("从缓存获取表列表")
        return [TextContent(type="text", text=cached_result)]
    try:
        with connect(**config) as conn:
            with conn.cursor() as cursor:
                # 获取表名和注释信息
                cursor.execute(
                    """
                    SELECT
                        TABLE_NAME,
                        TABLE_COMMENT
                    FROM information_schema.TABLES
                    WHERE TABLE_SCHEMA = %s
                """,
                    (config["database"],),
                )
                tables = cursor.fetchall()
                result = [f"Tables in {config['database']}:"]
                # 使用冒号分隔表名和注释
                result.extend([f"{table[0]}: {table[1] if table[1] else '无注释'}" for table in tables])
                result_text = "\n".join(result)

                # 存入缓存
                cache.set(cache_key, result_text)
                return [TextContent(type="text", text=result_text)]
    except Error as e:
        logger.error(f"数据库错误: {str(e)}")
        raise RuntimeError(f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"执行错误: {str(e)}")
        raise RuntimeError(f"Execution error: {str(e)}")


@mcp.tool()
def prepare_template_content(
    table_name: Annotated[str, Field(description="Name of the table to prepare template content")],
) -> list[TextContent]:
    """Prepare template content for a specific table"""
    pass


@click.command()
@click.option("--port", default=3004, help="Port to listen on")
@click.option(
    "--transport",
    type=click.Choice(["stdio", "streamable", "sse"]),
    default="sse",
    help="Transport type",
)
# 启动服务器的主函数
def main(port: int, transport: str) -> int:
    """Main entry point to run the MCP server."""

    def run_server(app):
        starlette_app = CORSMiddleware(
            app,
            allow_origins=["*"],  # Allow all origins - adjust as needed for production
            allow_methods=["GET", "POST", "DELETE"],  # MCP streamable HTTP methods
            expose_headers=["Mcp-Session-Id"],
        )
        import uvicorn

        uvicorn.run(starlette_app, host="0.0.0.0", port=port)

    try:
        logger.info("Starting MySQL MCP server...")
        config = get_db_config()
        logger.info(f"Database config: {config['host']}/{config['database']} as {config['user']}")
        # 使用 streamable-http 作为传输层
        if transport == "sse":
            run_server(mcp.sse_app())
        elif transport == "streamable":
            run_server(mcp.streamable_http_app())
        else:
            mcp.run(transport="stdio")

        return 0
    except Exception as e:
        logger.error(f"Server error: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
