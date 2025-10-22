import logging
import sys
from typing import Dict, Any, List

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

# 模拟设备数据库
MOCK_DEVICES = {
    "switch_001": {
        "product_id": "SMART_SWITCH_001",
        "device_id": "switch_001",
        "device_name": "客厅智能开关",
        "device_type": "switch",
        "manufacturer": "智能家居公司",
        "model": "SW-001",
        "firmware_version": "1.0.2",
        "status": {
            "power": {
                "flag": "power_status",
                "name": "开关状态",
                "value": "off",
                "type": "boolean",
                "description": "设备的开关状态"
            }
        },
        "actions": {
            "toggle": {
                "flag": "power_action",
                "name": "开关动作",
                "description": "控制设备开关",
                "params": {
                    "state": {
                        "type": "boolean",
                        "required": True,
                        "description": "开关状态，true为开，false为关"
                    }
                }
            }
        }
    },
    "fan_001": {
        "product_id": "SMART_FAN_001",
        "device_id": "fan_001",
        "device_name": "卧室智能风扇",
        "device_type": "fan",
        "manufacturer": "智能家居公司",
        "model": "FN-001",
        "firmware_version": "2.1.0",
        "status": {
            "power": {
                "flag": "power_status",
                "name": "开关状态",
                "value": "off",
                "type": "boolean",
                "description": "设备的开关状态"
            },
            "speed": {
                "flag": "speed_status",
                "name": "风速状态",
                "value": 0,
                "type": "integer",
                "min": 0,
                "max": 5,
                "description": "风扇风速等级，0-5级"
            }
        },
        "actions": {
            "toggle": {
                "flag": "power_action",
                "name": "开关动作",
                "description": "控制设备开关",
                "params": {
                    "state": {
                        "type": "boolean",
                        "required": True,
                        "description": "开关状态，true为开，false为关"
                    }
                }
            },
            "set_speed": {
                "flag": "speed_action",
                "name": "调节风速动作",
                "description": "调节风扇风速",
                "params": {
                    "speed": {
                        "type": "integer",
                        "required": True,
                        "min": 1,
                        "max": 5,
                        "description": "风速等级，1-5级"
                    }
                }
            }
        }
    },
    "switch_002": {
        "product_id": "SMART_SWITCH_001",
        "device_id": "switch_002",
        "device_name": "书房智能开关",
        "device_type": "switch",
        "manufacturer": "智能家居公司",
        "model": "SW-001",
        "firmware_version": "1.0.2",
        "status": {
            "power": {
                "flag": "power_status",
                "name": "开关状态",
                "value": "on",
                "type": "boolean",
                "description": "设备的开关状态"
            }
        },
        "actions": {
            "toggle": {
                "flag": "power_action",
                "name": "开关动作",
                "description": "控制设备开关",
                "params": {
                    "state": {
                        "type": "boolean",
                        "required": True,
                        "description": "开关状态，true为开，false为关"
                    }
                }
            }
        }
    },
    "fan_002": {
        "product_id": "SMART_FAN_001",
        "device_id": "fan_002",
        "device_name": "客厅智能风扇",
        "device_type": "fan",
        "manufacturer": "智能家居公司",
        "model": "FN-001",
        "firmware_version": "2.1.0",
        "status": {
            "power": {
                "flag": "power_status",
                "name": "开关状态",
                "value": "on",
                "type": "boolean",
                "description": "设备的开关状态"
            },
            "speed": {
                "flag": "speed_status",
                "name": "风速状态",
                "value": 3,
                "type": "integer",
                "min": 0,
                "max": 5,
                "description": "风扇风速等级，0-5级"
            }
        },
        "actions": {
            "toggle": {
                "flag": "power_action",
                "name": "开关动作",
                "description": "控制设备开关",
                "params": {
                    "state": {
                        "type": "boolean",
                        "required": True,
                        "description": "开关状态，true为开，false为关"
                    }
                }
            },
            "set_speed": {
                "flag": "speed_action",
                "name": "调节风速动作",
                "description": "调节风扇风速",
                "params": {
                    "speed": {
                        "type": "integer",
                        "required": True,
                        "min": 1,
                        "max": 5,
                        "description": "风速等级，1-5级"
                    }
                }
            }
        }
    }
}

@mcp.tool()
def exec_action(
    product_id: str = Field(..., description="产品ID"),
    device_id: str = Field(..., description="设备ID"),
    user_id: str = Field(..., description="用户ID"),
    action_flag: str = Field(..., description="动作标识"),
    action_params: Dict[str, Any] = Field(..., description="动作参数字典，不同设备参数类型和格式不同")
) -> list[TextContent]:
    """执行设备动作

    Args:
        product_id: 产品ID
        device_id: 设备ID
        user_id: 用户ID
        action_flag: 动作标识
        action_params: 动作参数字典，根据设备类型和动作不同而变化

    Returns:
        list[TextContent]: 执行结果
    """
    print(f"执行设备动作 - 用户ID: {user_id}, 产品ID: {product_id}, 设备ID: {device_id}, 动作标识: {action_flag}, 动作参数: {action_params}")
    logger.info(
        f"执行设备动作 - 用户ID: {user_id}, 产品ID: {product_id}, 设备ID: {device_id}, 动作标识: {action_flag}, 动作参数: {action_params}"
    )

    # 检查设备是否存在
    if device_id not in MOCK_DEVICES:
        error_msg = f"设备不存在: {device_id}"
        logger.error(error_msg)
        return [TextContent(type="text", text=f"错误: {error_msg}")]

    device = MOCK_DEVICES[device_id]

    # 检查产品ID是否匹配
    if device['product_id'] != product_id:
        error_msg = f"产品ID不匹配。设备 {device_id} 的产品ID为 {device['product_id']}, 请求的产品ID为 {product_id}"
        logger.error(error_msg)
        return [TextContent(type="text", text=f"错误: {error_msg}")]

    # 查找对应的动作
    action_found = False
    action_info = None

    for action_key, action_data in device['actions'].items():
        if action_data['flag'] == action_flag:
            action_found = True
            action_info = action_data
            break

    if not action_found:
        available_actions = [action['flag'] for action in device['actions'].values()]
        error_msg = f"设备 {device_id} 不支持动作 {action_flag}。可用动作: {', '.join(available_actions)}"
        logger.error(error_msg)
        return [TextContent(type="text", text=f"错误: {error_msg}")]

    # 模拟执行动作
    result = f"设备动作执行完成\n"
    result += f"设备名称: {device['device_name']}\n"
    result += f"产品ID: {product_id}\n"
    result += f"设备ID: {device_id}\n"
    result += f"动作: {action_info['name']} ({action_flag})\n"
    result += f"动作参数: {action_params}\n"

    # 根据动作类型更新设备状态
    if action_flag == "power_action":
        if 'state' in action_params:
            new_state = action_params['state']
            device['status']['power']['value'] = new_state
            result += f"状态更新: 设备开关状态已更新为 {'开启' if new_state else '关闭'}\n"

    elif action_flag == "speed_action":
        if 'speed' in action_params:
            new_speed = action_params['speed']
            # 风扇动作前需要确保设备已开启
            if device['status']['power']['value']:
                device['status']['speed']['value'] = new_speed
                result += f"状态更新: 风扇速度已调节为 {new_speed} 级\n"
            else:
                result += "注意: 设备当前处于关闭状态，无法调节风速\n"

    result += f"\n当前设备状态:\n"
    for status_key, status_data in device['status'].items():
        result += f"  - {status_data['name']}: {status_data['value']}\n"

    return [TextContent(type="text", text=result)]


@mcp.tool()
def query_status(
    product_id: str = Field(..., description="产品ID"),
    device_id: str = Field(..., description="设备ID"),
    user_id: str = Field(..., description="用户ID"),
    status_flag: str = Field(..., description="状态标识")
) -> list[TextContent]:
    """查询设备状态

    Args:
        product_id: 产品ID
        device_id: 设备ID
        user_id: 用户ID
        status_flag: 状态标识

    Returns:
        list[TextContent]: 查询结果
    """
    print(f"查询设备状态 - 用户ID: {user_id}, 产品ID: {product_id}, 设备ID: {device_id}, 状态标识: {status_flag}")
    logger.info(
        f"查询设备状态 - 用户ID: {user_id}, 产品ID: {product_id}, 设备ID: {device_id}, 状态标识: {status_flag}"
    )

    # 检查设备是否存在
    if device_id not in MOCK_DEVICES:
        error_msg = f"设备不存在: {device_id}"
        logger.error(error_msg)
        return [TextContent(type="text", text=f"错误: {error_msg}")]

    device = MOCK_DEVICES[device_id]

    # 检查产品ID是否匹配
    if device['product_id'] != product_id:
        error_msg = f"产品ID不匹配。设备 {device_id} 的产品ID为 {device['product_id']}, 请求的产品ID为 {product_id}"
        logger.error(error_msg)
        return [TextContent(type="text", text=f"错误: {error_msg}")]

    # 查找对应的状态
    status_found = False
    status_info = None

    for status_key, status_data in device['status'].items():
        if status_data['flag'] == status_flag:
            status_found = True
            status_info = status_data
            break

    if not status_found:
        available_status = [status['flag'] for status in device['status'].values()]
        error_msg = f"设备 {device_id} 不存在状态 {status_flag}。可用状态: {', '.join(available_status)}"
        logger.error(error_msg)
        return [TextContent(type="text", text=f"错误: {error_msg}")]

    # 返回状态查询结果
    result = f"设备状态查询完成\n"
    result += f"设备名称: {device['device_name']}\n"
    result += f"产品ID: {product_id}\n"
    result += f"设备ID: {device_id}\n"
    result += f"状态: {status_info['name']} ({status_flag})\n"
    result += f"状态值: {status_info['value']}\n"
    result += f"状态类型: {status_info['type']}\n"
    result += f"描述: {status_info['description']}\n"

    # 如果是数值类型，显示额外信息
    if status_info['type'] == 'integer':
        if 'min' in status_info:
            result += f"最小值: {status_info['min']}\n"
        if 'max' in status_info:
            result += f"最大值: {status_info['max']}\n"

    # 显示设备所有状态概览
    result += f"\n设备完整状态:\n"
    for status_key, status_data in device['status'].items():
        result += f"  - {status_data['name']} ({status_data['flag']}): {status_data['value']}\n"

    return [TextContent(type="text", text=result)]


@mcp.tool()
def list_user_devices(
    user_id: str = Field(..., description="用户ID"),
    format_type: str = Field(default="compact", description="返回格式类型: 'compact'(紧凑格式,推荐) 或 'detailed'(详细文本)")
) -> list[TextContent]:
    """列出用户的所有设备,优化后的格式便于大模型解析和定位action_flag

    Args:
        user_id: 用户ID
        format_type: 返回格式类型,默认为structured(结构化表格)

    Returns:
        list[TextContent]: 设备列表,包含设备基本信息、状态和可用动作
    """
    logger.info(f"列出用户设备列表 - 用户ID: {user_id}, 格式: {format_type}")

    if format_type == "compact":
        # 紧凑格式 - 按产品分组,避免重复
        result = "# 用户设备列表 (紧凑格式)\n\n"

        # 按产品分组
        products = {}
        for device_id, device_info in MOCK_DEVICES.items():
            product_id = device_info['product_id']
            if product_id not in products:
                products[product_id] = {
                    'device_type': device_info['device_type'],
                    'actions': device_info['actions'],
                    'status_schema': device_info['status'],
                    'devices': []
                }
            products[product_id]['devices'].append({
                'device_id': device_id,
                'device_name': device_info['device_name'],
                'current_status': {k: v['value'] for k, v in device_info['status'].items()}
            })

        for idx, (product_id, product_info) in enumerate(products.items(), 1):
            result += f"## 产品 {idx}: {product_info['device_type']} (产品ID: `{product_id}`)\n\n"

            # 设备列表
            result += "### 设备列表\n"
            result += "| device_id | 设备名称 | 当前状态 |\n"
            result += "|-----------|----------|----------|\n"
            for device in product_info['devices']:
                power_status = "开启" if device['current_status']['power'] else "关闭"
                result += f"| `{device['device_id']}` | {device['device_name']} | {power_status} |\n"
            result += "\n"

            # 产品统一的动作列表
            result += "### 产品支持的动作\n"
            result += "| 动作名称 | action_flag | 必需参数 |\n"
            result += "|----------|-------------|----------|\n"
            for action_key, action_info in product_info['actions'].items():
                params_str = ", ".join([
                    f"{param_name}({param_info['type']})"
                    for param_name, param_info in action_info.get('params', {}).items()
                ])
                result += f"| {action_info['name']} | **`{action_info['flag']}`** | {params_str} |\n"
            result += "\n"

            # 状态查询
            result += "### 可查询状态\n"
            result += "| 状态名称 | status_flag |\n"
            result += "|----------|-------------|\n"
            for status_key, status_info in product_info['status_schema'].items():
                result += f"| {status_info['name']} | `{status_info['flag']}` |\n"
            result += "\n"

        # 快速参考 - 极简版
        result += "## 快速参考\n\n"
        result += "### 所有 动作标识 对应表\n"
        result += "| 产品ID | 设备ID列表 | 动作标识列表 |\n"
        result += "|--------|---------------|----------------|\n"
        for product_id, product_info in products.items():
            device_ids = ", ".join([f"`{d['device_id']}`" for d in product_info['devices']])
            action_flags = ", ".join([f"`{a['flag']}`" for a in product_info['actions'].values()])
            result += f"| `{product_id}` | {device_ids} | {action_flags} |\n"

    else:
        # 详细文本格式 (保留原有格式)
        result = "用户设备列表\n"
        result += "=" * 50 + "\n\n"

        for device_id, device_info in MOCK_DEVICES.items():
            result += f"设备ID: {device_info['device_id']}\n"
            result += f"产品ID: {device_info['product_id']}\n"
            result += f"设备名称: {device_info['device_name']}\n"
            result += f"设备类型: {device_info['device_type']}\n"
            result += f"制造商: {device_info['manufacturer']}\n"
            result += f"型号: {device_info['model']}\n"
            result += f"固件版本: {device_info['firmware_version']}\n"

            # 状态信息
            result += "\n状态信息:\n"
            for status_key, status_info in device_info['status'].items():
                result += f"  - {status_info['name']} ({status_info['flag']}): {status_info['value']}\n"
                result += f"    类型: {status_info['type']}, 描述: {status_info['description']}\n"

            # 可用动作
            result += "\n可用动作:\n"
            for action_key, action_info in device_info['actions'].items():
                result += f"  - {action_info['name']} ({action_info['flag']}): {action_info['description']}\n"
                if 'params' in action_info:
                    result += "    参数:\n"
                    for param_name, param_info in action_info['params'].items():
                        result += f"      - {param_name}: {param_info['description']}\n"
                        result += f"        类型: {param_info['type']}, 必需: {param_info['required']}\n"
                        if 'min' in param_info:
                            result += f"        最小值: {param_info['min']}\n"
                        if 'max' in param_info:
                            result += f"        最大值: {param_info['max']}\n"

            result += "\n" + "-" * 50 + "\n\n"

        # 添加统计信息
        device_types = {}
        for device_info in MOCK_DEVICES.values():
            device_type = device_info['device_type']
            device_types[device_type] = device_types.get(device_type, 0) + 1

        result += "设备统计:\n"
        for device_type, count in device_types.items():
            result += f"  - {device_type}: {count} 个设备\n"
        result += f"  - 总计: {len(MOCK_DEVICES)} 个设备\n"
    logger.info(f"列出用户设备列表:\n{result}")
    return [TextContent(type="text", text=result)]


@with_mcp_options(3006)
def main(transport: str, port: int):
    """主函数，启动MCP服务器"""
    run_mcp_server(mcp, transport, port= port)


if __name__ == "__main__":
    main()
