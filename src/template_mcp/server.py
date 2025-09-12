"""模板 MCP 服务器
支持根据模板名称输出模板文件内容
"""

import logging
import sys
from pathlib import Path
from typing import List

from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent, Prompt, PromptMessage
from pydantic import Field

from common.cache import Cache
from common.mcp_cli import with_mcp_options, run_mcp_server

# 创建全局缓存实例
cache = Cache()

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# 创建 MCP 服务器
mcp = FastMCP("template_mcp_server")

# 模板文件配置
TEMPLATE_BASE_DIR = Path(__file__).parent / "template"
SAMPLE_BASE_DIR = Path(__file__).parent / "sample"

# 支持的模板文件映射
TEMPLATE_FILES = {
    # 后端代码模板
    "domain": {"path": "java/domain.java.vm", "description": "Domain实体类模板", "category": "后端代码"},
    "mapper": {"path": "java/mapper.java.vm", "description": "Mapper接口模板", "category": "后端代码"},
    "service": {"path": "java/service.java.vm", "description": "Service接口模板", "category": "后端代码"},
    "serviceImpl": {"path": "java/serviceImpl.java.vm", "description": "Service实现类模板", "category": "后端代码"},
    "controller": {"path": "java/controller.java.vm", "description": "Controller控制器模板", "category": "后端代码"},
    "mapper_xml": {"path": "xml/mapper.xml.vm", "description": "MyBatis XML映射文件模板", "category": "后端代码"},
    "sub_domain": {"path": "java/sub-domain.java.vm", "description": "子表Domain实体类模板", "category": "后端代码"},
    # 前端代码模板
    "api": {"path": "js/api.js.vm", "description": "API接口文件模板", "category": "前端代码"},
    "vue_index": {"path": "vue/index.vue.vm", "description": "Vue页面组件模板", "category": "前端代码"},
    "vue_form": {"path": "vue/v3/Form.vue.vm", "description": "Vue表单组件模板", "category": "前端代码"},
    "vue_tree": {"path": "vue/index-tree.vue.vm", "description": "Vue树形页面组件模板", "category": "前端代码"},
    "vue_v3_index": {"path": "vue/v3/index.vue.vm", "description": "Vue3页面组件模板", "category": "前端代码"},
    "vue_v3_tree": {"path": "vue/v3/index-tree.vue.vm", "description": "Vue3树形页面组件模板", "category": "前端代码"},
    "vue_v3_form": {"path": "vue/v3/Form.vue.vm", "description": "Vue3表单组件模板", "category": "前端代码"},
    # 数据库脚本模板
    "sql": {"path": "sql/sql.vm", "description": "菜单SQL脚本模板", "category": "数据库脚本"},
}


def validate_template_name(template_name: str) -> bool:
    """验证模板名称是否有效

    Args:
        template_name: 模板名称

    Returns:
        bool: 模板名称是否有效
    """
    return template_name in TEMPLATE_FILES


def get_template_file_path(template_name: str) -> Path:
    """获取模板文件的完整路径

    Args:
        template_name: 模板名称

    Returns:
        Path: 模板文件路径
    """
    if not validate_template_name(template_name):
        raise ValueError(f"不支持的模板名称: {template_name}")

    template_info = TEMPLATE_FILES[template_name]
    return TEMPLATE_BASE_DIR / template_info["path"]


def read_template_content(template_name: str) -> str:
    """读取模板文件内容

    Args:
        template_name: 模板名称

    Returns:
        str: 模板文件内容
    """
    template_path = get_template_file_path(template_name)

    if not template_path.exists():
        raise FileNotFoundError(f"模板文件不存在: {template_path}")

    try:
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"读取模板文件失败: {template_path}, 错误: {e}")
        raise


def get_sample_file_path(template_name: str) -> Path:
    """获取示例文件的完整路径

    Args:
        template_name: 模板名称

    Returns:
        Path: 示例文件路径
    """
    if not validate_template_name(template_name):
        raise ValueError(f"不支持的模板名称: {template_name}")

    template_info = TEMPLATE_FILES[template_name]
    sample_path = template_info["path"]

    # 移除 .vm 扩展名
    if sample_path.endswith(".vm"):
        sample_path = sample_path[:-3]

    return SAMPLE_BASE_DIR / sample_path


def read_sample_content(template_name: str) -> str:
    """读取示例文件内容

    Args:
        template_name: 模板名称

    Returns:
        str: 示例文件内容
    """
    sample_path = get_sample_file_path(template_name)

    if not sample_path.exists():
        raise FileNotFoundError(f"示例文件不存在: {sample_path}")

    try:
        with open(sample_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"读取示例文件失败: {sample_path}, 错误: {e}")
        raise


@mcp.prompt()
def list_templates() -> Prompt:
    """列出所有可用的模板信息

    Returns:
        Prompt: 包含所有模板信息的结构化输出
    """
    # 按类别组织模板信息
    categories = {}
    for template_name, template_info in TEMPLATE_FILES.items():
        category = template_info["category"]
        if category not in categories:
            categories[category] = []
        categories[category].append(
            {"name": template_name, "description": template_info["description"], "path": template_info["path"]}
        )

    # 构建结构化输出
    content = "# 可用模板列表\n\n"

    for category, templates in categories.items():
        content += f"## {category}\n\n"
        for template in templates:
            content += f"- **{template['name']}**: {template['description']} (`{template['path']}`)\n"
        content += "\n"

    content += "## 使用说明\n\n"
    content += "使用 `get_template_content` 工具，传入模板名称即可获取对应的模板文件内容。\n\n"
    content += "支持的模板名称:\n"
    for template_name in TEMPLATE_FILES.keys():
        content += f"- `{template_name}`\n"

    return Prompt(
        name="list_templates",
        description="列出所有可用的代码生成模板信息",
        messages=[PromptMessage(role="user", content=TextContent(type="text", text=content))],
    )


@mcp.tool()
def get_template_content(
    template_name: str = Field(..., description="模板文件名称，支持的模板名称请参考 list_templates prompt"),
) -> List[TextContent]:
    """根据模板名称获取模板文件内容

    Args:
        template_name: 模板名称

    Returns:
        List[TextContent]: 包含模板文件内容的文本内容列表
    """
    if cache.get(template_name):
        return [TextContent(type="text", text=cache.get(template_name))]
    try:
        # 验证模板名称
        if not validate_template_name(template_name):
            available_templates = ", ".join(TEMPLATE_FILES.keys())
            return [
                TextContent(
                    type="text",
                    text=f"错误: 不支持的模板名称 '{template_name}'。\n\n可用的模板名称: {available_templates}",
                )
            ]

        # 读取模板内容
        content = read_template_content(template_name)
        template_info = TEMPLATE_FILES[template_name]

        # 构建返回信息
        result = f"# 模板: {template_name}\n\n"
        result += f"**描述**: {template_info['description']}\n"
        result += f"**类别**: {template_info['category']}\n"
        result += f"**路径**: {template_info['path']}\n\n"
        result += "## 模板内容\n\n"
        result += "```velocity\n"
        result += content
        result += "\n```"

        logger.info(f"成功获取模板内容: {template_name}")
        cache.set(template_name, result)
        return [TextContent(type="text", text=result)]

    except FileNotFoundError as e:
        error_msg = f"模板文件不存在: {str(e)}"
        logger.error(error_msg)
        return [TextContent(type="text", text=f"错误: {error_msg}")]

    except Exception as e:
        error_msg = f"获取模板内容时发生错误: {str(e)}"
        logger.error(error_msg)
        return [TextContent(type="text", text=f"错误: {error_msg}")]


@mcp.tool()
def get_sample_content(
    template_name: str = Field(..., description="模板文件名称，获取对应的示例代码"),
) -> List[TextContent]:
    """根据模板名称获取示例代码内容

    Args:
        template_name: 模板名称

    Returns:
        List[TextContent]: 包含示例代码内容的文本内容列表
    """
    try:
        # 验证模板名称
        if not validate_template_name(template_name):
            available_templates = ", ".join(TEMPLATE_FILES.keys())
            return [
                TextContent(
                    type="text",
                    text=f"错误: 不支持的模板名称 '{template_name}'。\n\n可用的模板名称: {available_templates}",
                )
            ]

        # 读取示例内容
        content = read_sample_content(template_name)
        template_info = TEMPLATE_FILES[template_name]

        # 构建返回信息
        result = f"# 示例代码: {template_name}\n\n"
        result += f"**描述**: {template_info['description']}\n"
        result += f"**类别**: {template_info['category']}\n"
        result += f"**模板路径**: {template_info['path']}\n"

        # 获取示例文件路径用于显示
        sample_path = get_sample_file_path(template_name)
        result += f"**示例路径**: {sample_path.relative_to(SAMPLE_BASE_DIR)}\n\n"
        result += "## 示例代码\n\n"

        # 根据文件扩展名确定代码语言
        file_ext = sample_path.suffix.lower()
        if file_ext == ".java":
            lang = "java"
        elif file_ext == ".js":
            lang = "javascript"
        elif file_ext == ".vue":
            lang = "vue"
        elif file_ext == ".xml":
            lang = "xml"
        elif file_ext == ".sql" or sample_path.name == "sql":
            lang = "sql"
        else:
            lang = "text"

        result += f"```{lang}\n"
        result += content
        result += "\n```"

        logger.info(f"成功获取示例代码: {template_name}")

        return [TextContent(type="text", text=result)]

    except FileNotFoundError as e:
        error_msg = f"示例文件不存在: {str(e)}"
        logger.error(error_msg)
        return [TextContent(type="text", text=f"错误: {error_msg}")]

    except Exception as e:
        error_msg = f"获取示例代码时发生错误: {str(e)}"
        logger.error(error_msg)
        return [TextContent(type="text", text=f"错误: {error_msg}")]


@mcp.tool()
def list_template_categories() -> List[TextContent]:
    """列出所有模板类别及其包含的模板

    Returns:
        List[TextContent]: 包含模板类别信息的文本内容列表
    """
    try:
        # 按类别组织模板
        categories = {}
        for template_name, template_info in TEMPLATE_FILES.items():
            category = template_info["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append({"name": template_name, "description": template_info["description"]})

        # 构建输出
        result = "# 模板类别\n\n"

        for category, templates in categories.items():
            result += f"## {category}\n\n"
            for template in templates:
                result += f"- **{template['name']}**: {template['description']}\n"
            result += "\n"

        return [TextContent(type="text", text=result)]

    except Exception as e:
        error_msg = f"获取模板类别时发生错误: {str(e)}"
        logger.error(error_msg)
        return [TextContent(type="text", text=f"错误: {error_msg}")]


@with_mcp_options(3005)
def main(transport: str, port: int):
    """主函数，启动MCP服务器"""
    run_mcp_server(mcp, transport, port= port)

if __name__ == "__main__":
    sys.exit(main())