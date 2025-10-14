import logging
import sys
from typing import Dict, Any

from mcp.server import FastMCP
from mcp.types import TextContent
from pydantic import Field

from common.mcp_cli import with_mcp_options, run_mcp_server

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


@mcp.tool()
def exec_action(
    product_id: str = Field(..., description="产品ID"),
    device_id: str = Field(..., description="设备ID"),
    action_flag: str = Field(..., description="动作标识"),
    action_params: Dict[str, Any] = Field(..., description="动作参数字典，不同设备参数类型和格式不同")
) -> list[TextContent]:
    """执行设备动作

    Args:
        product_id: 产品ID
        device_id: 设备ID
        action_flag: 动作标识
        action_params: 动作参数字典，根据设备类型和动作不同而变化

    Returns:
        list[TextContent]: 执行结果
    """
    print(f"执行设备动作 - 产品ID: {product_id}, 设备ID: {device_id}, 动作标识: {action_flag}, 动作参数: {action_params}")
    logger.info(f"执行设备动作 - 产品ID: {product_id}, 设备ID: {device_id}, 动作标识: {action_flag}, 动作参数: {action_params}")

    result = f"设备动作执行完成\n"
    result += f"产品ID: {product_id}\n"
    result += f"设备ID: {device_id}\n"
    result += f"动作标识: {action_flag}\n"
    result += f"动作参数: {action_params}\n"

    return [TextContent(type="text", text=result)]


@mcp.tool()
def query_status(
    product_id: str = Field(..., description="产品ID"),
    device_id: str = Field(..., description="设备ID"),
    status_flag: str = Field(..., description="状态标识")
) -> list[TextContent]:
    """查询设备状态

    Args:
        product_id: 产品ID
        device_id: 设备ID
        status_flag: 状态标识

    Returns:
        list[TextContent]: 查询结果
    """
    print(f"查询设备状态 - 产品ID: {product_id}, 设备ID: {device_id}, 状态标识: {status_flag}")
    logger.info(f"查询设备状态 - 产品ID: {product_id}, 设备ID: {device_id}, 状态标识: {status_flag}")

    result = f"设备状态查询完成\n"
    result += f"产品ID: {product_id}\n"
    result += f"设备ID: {device_id}\n"
    result += f"状态标识: {status_flag}\n"
    result += f"状态值: 模拟状态值"  # 这里可以返回模拟的状态值

    return [TextContent(type="text", text=result)]


@with_mcp_options(3006)
def main(transport: str, port: int):
    """主函数，启动MCP服务器"""
    run_mcp_server(mcp, transport, port= port)


if __name__ == "__main__":
    main()
