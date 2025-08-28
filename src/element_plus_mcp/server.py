import json
import logging
import sys
from pathlib import Path
from typing import Annotated

import click
from mcp.server.fastmcp import FastMCP
from pydantic import Field

from element_plus_mcp.github import get_config, get_directory_contents, get_file_content
from element_plus_mcp.models import (
    DirectoryStructure,
    DirectoryItem,
    ComponentMetadata,
    FileInfo,
    ComponentList,
    ComponentDemo,
    DemoFile,
    ComponentSource,
    SourceFile,
)
from starlette.middleware.cors import CORSMiddleware

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Create an MCP server
mcp = FastMCP("ElementPlusServer", host="0.0.0.0", port=3003)


@mcp.tool()
def get_component(
    component_name: Annotated[str, Field(description="Name of the element-plus component (e.g., 'avatar', 'button')")],
) -> ComponentSource:
    """
    获取指定element-plus组件的源码
    """
    try:
        # element-plus组件通常在packages/components目录下
        component_path = f"packages/components/{component_name.lower()}"

        # 首先检查组件目录是否存在
        contents = get_directory_contents(component_path)
        if not contents:
            return ComponentSource(
                component_name=component_name,
                source_files=[],
                found=False,
                error_message=f"组件 '{component_name}' 不存在或无法访问",
            )

        # 查找主要的源码文件
        source_files = []
        for item in contents:
            if item["type"] == "file" and item["name"].endswith((".vue", ".ts", ".tsx")):
                file_content = get_file_content(item["path"])
                # 确定文件语言类型
                extension = item["name"].split(".")[-1]
                language_map = {"vue": "vue", "ts": "typescript", "tsx": "typescript"}
                language = language_map.get(extension, extension)

                source_files.append(SourceFile(filename=item["name"], language=language, content=file_content))

        if source_files:
            return ComponentSource(
                component_name=component_name, source_files=source_files, found=True, error_message=None
            )
        else:
            return ComponentSource(
                component_name=component_name,
                source_files=[],
                found=False,
                error_message=f"未找到组件 '{component_name}' 的源码文件",
            )

    except Exception as e:
        logger.error(f"获取组件源码时出错: {e}")
        return ComponentSource(
            component_name=component_name,
            source_files=[],
            found=False,
            error_message=f"获取组件 '{component_name}' 源码时出错: {str(e)}",
        )


@mcp.tool()
def get_component_demo(
    component_name: Annotated[str, Field(description="Name of the element-plus component (e.g., 'avatar', 'button')")],
) -> ComponentDemo:
    """
    获取指定element-plus组件的演示代码
    """
    try:
        # 查找文档中的演示代码
        docs_path = f"docs/examples/{component_name.lower()}"

        # 首先尝试在docs/examples目录下查找
        contents = get_directory_contents(docs_path)

        if not contents:
            # 如果没有找到，尝试在packages/components下的__tests__或demo目录
            test_path = f"packages/components/{component_name.lower()}/__tests__"
            contents = get_directory_contents(test_path)

        if not contents:
            # 尝试查找demo目录
            demo_path = f"packages/components/{component_name.lower()}/demo"
            contents = get_directory_contents(demo_path)

        if not contents:
            return ComponentDemo(
                component_name=component_name,
                demo_files=[],
                found=False,
                error_message=f"未找到组件 '{component_name}' 的演示代码",
            )

        # 查找演示文件
        demo_files = []
        for item in contents:
            if item["type"] == "file" and (
                item["name"].endswith(".vue") or "demo" in item["name"].lower() or "example" in item["name"].lower()
            ):
                file_content = get_file_content(item["path"])
                demo_files.append(DemoFile(filename=item["name"], content=file_content))

        if demo_files:
            return ComponentDemo(component_name=component_name, demo_files=demo_files, found=True, error_message=None)
        else:
            return ComponentDemo(
                component_name=component_name,
                demo_files=[],
                found=False,
                error_message=f"未找到组件 '{component_name}' 的演示文件",
            )

    except Exception as e:
        logger.error(f"获取组件演示代码时出错: {e}")
        return ComponentDemo(
            component_name=component_name,
            demo_files=[],
            found=False,
            error_message=f"获取组件 '{component_name}' 演示代码时出错: {str(e)}",
        )


@mcp.tool()
def list_components() -> ComponentList:
    """
    列出所有可用的element-plus组件
    """
    try:
        # 获取packages/components目录下的所有组件
        components_path = "packages/components"
        contents = get_directory_contents(components_path)

        if not contents:
            return ComponentList(components=[], total_count=0, found=False, error_message="无法获取组件列表")

        # 过滤出组件目录
        components = []
        for item in contents:
            if item["type"] == "dir" and not item["name"].startswith("."):
                components.append(item["name"])

        components.sort()

        if components:
            return ComponentList(components=components, total_count=len(components), found=True, error_message=None)
        else:
            return ComponentList(components=[], total_count=0, found=False, error_message="未找到任何组件")

    except Exception as e:
        logger.error(f"获取组件列表时出错: {e}")
        return ComponentList(components=[], total_count=0, found=False, error_message=f"获取组件列表时出错: {str(e)}")


@mcp.tool()
def get_component_metadata(
    component_name: Annotated[str, Field(description="Name of the element-plus component (e.g., 'avatar', 'button')")],
) -> ComponentMetadata:
    """
    获取指定element-plus组件的元数据信息
    """
    try:
        component_path = f"packages/components/{component_name.lower()}"

        # 获取组件目录内容
        contents = get_directory_contents(component_path)
        if not contents:
            return ComponentMetadata(name=component_name, description="", files=[], dependencies=[])

        files = []
        dependencies = []
        description = ""

        # 分析文件结构
        for item in contents:
            if item["type"] == "file":
                files.append(
                    FileInfo(
                        name=item["name"],
                        size=item.get("size", 0),
                        type=item["name"].split(".")[-1] if "." in item["name"] else "unknown",
                    )
                )

        # 尝试读取package.json获取依赖信息
        package_json_path = f"{component_path}/package.json"
        package_content = get_file_content(package_json_path)
        if package_content and not package_content.startswith("无法获取文件内容"):
            try:
                package_data = json.loads(package_content)
                description = package_data.get("description", "")
                dependencies = list(package_data.get("dependencies", {}).keys())
            except json.JSONDecodeError:
                pass

        return ComponentMetadata(name=component_name, description=description, files=files, dependencies=dependencies)

    except Exception as e:
        logger.error(f"获取组件元数据时出错: {e}")
        return ComponentMetadata(
            name=component_name,
            description=f"获取组件 '{component_name}' 元数据时出错: {str(e)}",
            files=[],
            dependencies=[],
        )


@mcp.tool()
def get_directory_structure(
    path: Annotated[
        str, Field(description="Path within the repository (default: packages/components)")
    ] = "packages/components",
    owner: Annotated[str, Field(description="Repository owner (default: element-plus)")] = "element-plus",
    repo: Annotated[str, Field(description="Repository name (default: element-plus)")] = "element-plus",
    branch: Annotated[str, Field(description="Branch name (default: dev)")] = "dev",
) -> DirectoryStructure:
    """
    获取element-plus仓库的目录结构
    """
    try:
        # 临时更新配置以支持自定义仓库
        original_config = get_config()["element_plus_repo"].copy()
        get_config()["element_plus_repo"]["owner"] = owner
        get_config()["element_plus_repo"]["repo"] = repo
        get_config()["element_plus_repo"]["branch"] = branch

        contents = get_directory_contents(path, branch)

        # 恢复原始配置
        get_config()["element_plus_repo"] = original_config

        if not contents:
            return DirectoryStructure(
                path=path,
                owner=owner,
                repo=repo,
                branch=branch,
                items=[],
                directory_count=0,
                file_count=0,
                found=False,
                error_message=f"无法获取目录结构: {path}",
            )

        # 构建目录项列表
        items = []
        directory_count = 0
        file_count = 0

        for item in contents:
            if item["type"] == "dir":
                directory_count += 1
                items.append(DirectoryItem(name=item["name"], type="dir", size=None))
            else:
                file_count += 1
                items.append(DirectoryItem(name=item["name"], type="file", size=item.get("size", 0)))

        # 按类型和名称排序：先目录后文件，同类型按名称排序
        items.sort(key=lambda x: (x.type == "file", x.name))

        return DirectoryStructure(
            path=path,
            owner=owner,
            repo=repo,
            branch=branch,
            items=items,
            directory_count=directory_count,
            file_count=file_count,
            found=True,
            error_message=None,
        )

    except Exception as e:
        logger.error(f"获取目录结构时出错: {e}")
        return DirectoryStructure(
            path=path,
            owner=owner,
            repo=repo,
            branch=branch,
            items=[],
            directory_count=0,
            file_count=0,
            found=False,
            error_message=f"获取目录结构时出错: {str(e)}",
        )

@click.command()
@click.option(
    "--transport",
    type=click.Choice(["stdio", "streamable","sse"]),
    default="stdio",
    help="Transport type",
)
def main(transport: str):
    """主函数，启动MCP服务器"""
    logger.info("启动Element Plus MCP服务器...")
    logger.info(f"GitHub API Token: {'已配置' if get_config()['github_api_key'] else '未配置'}")
    def run_server(app):
        # 加载环境变量，更新配置对象信息
        env_file = Path(__file__).parent.parent.parent / ".env"
        if env_file.exists():
            # 加载 .env 文件
            from dotenv import load_dotenv
            load_dotenv(env_file)
        starlette_app = CORSMiddleware(
            app,
            allow_origins=["*"],  # Allow all origins - adjust as needed for production
            allow_methods=["GET", "POST", "DELETE"],  # MCP streamable HTTP methods
            expose_headers=["Mcp-Session-Id"],
        )
        import uvicorn
        uvicorn.run(starlette_app, host="0.0.0.0", port=3001)
    if transport == "sse":
        run_server(mcp.sse_app())
    elif transport == "streamable":
        run_server(mcp.streamable_http_app())
    else:
        mcp.run(transport="stdio")

if __name__ == "__main__":
    main()