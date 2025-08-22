from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
import logging
import os
import sys
from typing import List, Dict, Optional, Any, Annotated
import json
import requests
from urllib.parse import quote
from pathlib import Path
import click

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Create an MCP server
mcp = FastMCP("ElementPlusServer", host="0.0.0.0", port=3003)

def get_config() -> Dict[str, Any]:
    """获取配置信息"""
    return {
        "github_api_key": os.getenv('GITHUB_API_KEY', ''),
        "element_plus_repo": {
            "owner": "element-plus",
            "repo": "element-plus",
            "branch": "dev"
        },
        "github_api_base": "https://api.github.com"
    }

class GitHubAPIError(Exception):
    """GitHub API错误异常类"""
    pass

def get_github_headers() -> Dict[str, str]:
    """获取GitHub API请求头"""
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "ElementPlus-MCP-Server"
    }
    if get_config()["github_api_key"]:
        headers["Authorization"] = f"token {get_config()['github_api_key']}"
    return headers

def make_github_request(url: str) -> Dict[str, Any]:
    """发送GitHub API请求"""
    try:
        response = requests.get(url, headers=get_github_headers(), timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"GitHub API请求失败: {e}")
        raise GitHubAPIError(f"GitHub API请求失败: {e}")

def get_file_content(path: str, branch: str = None) -> str:
    """获取GitHub仓库中文件的内容"""
    if branch is None:
        branch = get_config()["element_plus_repo"]["branch"]
    
    owner = get_config()["element_plus_repo"]["owner"]
    repo = get_config()["element_plus_repo"]["repo"]
    
    url = f"{get_config()['github_api_base']}/repos/{owner}/{repo}/contents/{quote(path)}?ref={branch}"
    
    try:
        data = make_github_request(url)
        if data.get('encoding') == 'base64':
            import base64
            return base64.b64decode(data['content']).decode('utf-8')
        else:
            return data.get('content', '')
    except GitHubAPIError:
        return f"无法获取文件内容: {path}"

def get_directory_contents(path: str = "", branch: str = None) -> List[Dict[str, Any]]:
    """获取GitHub仓库目录内容"""
    if branch is None:
        branch = get_config()["element_plus_repo"]["branch"]
    
    owner = get_config()["element_plus_repo"]["owner"]
    repo = get_config()["element_plus_repo"]["repo"]
    
    url = f"{get_config()['github_api_base']}/repos/{owner}/{repo}/contents/{quote(path)}?ref={branch}"
    
    try:
        data = make_github_request(url)
        if isinstance(data, list):
            return data
        else:
            return [data]
    except GitHubAPIError:
        return []

@mcp.tool()
def get_component(componentName: Annotated[str, Field(description="Name of the element-plus component (e.g., 'avatar', 'button')")]) -> str:
    """
    获取指定element-plus组件的源码
    """
    try:
        # element-plus组件通常在packages/components目录下
        component_path = f"packages/components/{componentName.lower()}"
        
        # 首先检查组件目录是否存在
        contents = get_directory_contents(component_path)
        if not contents:
            return f"组件 '{componentName}' 不存在或无法访问"
        
        # 查找主要的源码文件
        source_files = []
        for item in contents:
            if item['type'] == 'file' and item['name'].endswith(('.vue', '.ts', '.tsx')):
                file_content = get_file_content(item['path'])
                source_files.append(f"## {item['name']}\n```{item['name'].split('.')[-1]}\n{file_content}\n```")
        
        if source_files:
            return f"# Element Plus 组件: {componentName}\n\n" + "\n\n".join(source_files)
        else:
            return f"未找到组件 '{componentName}' 的源码文件"
            
    except Exception as e:
        logger.error(f"获取组件源码时出错: {e}")
        return f"获取组件 '{componentName}' 源码时出错: {str(e)}"

@mcp.tool()
def get_component_demo(componentName: Annotated[str, Field(description="Name of the element-plus component (e.g., 'avatar', 'button')")]) -> str:
    """
    获取指定element-plus组件的演示代码
    """
    try:
        # 查找文档中的演示代码
        docs_path = f"docs/examples/{componentName.lower()}"
        
        # 首先尝试在docs/examples目录下查找
        contents = get_directory_contents(docs_path)
        
        if not contents:
            # 如果没有找到，尝试在packages/components下的__tests__或demo目录
            test_path = f"packages/components/{componentName.lower()}/__tests__"
            contents = get_directory_contents(test_path)
        
        if not contents:
            # 尝试查找demo目录
            demo_path = f"packages/components/{componentName.lower()}/demo"
            contents = get_directory_contents(demo_path)
        
        if not contents:
            return f"未找到组件 '{componentName}' 的演示代码"
        
        # 查找演示文件
        demo_files = []
        for item in contents:
            if item['type'] == 'file' and (item['name'].endswith('.vue') or 'demo' in item['name'].lower() or 'example' in item['name'].lower()):
                file_content = get_file_content(item['path'])
                demo_files.append(f"## {item['name']}\n```vue\n{file_content}\n```")
        
        if demo_files:
            return f"# Element Plus 组件演示: {componentName}\n\n" + "\n\n".join(demo_files)
        else:
            return f"未找到组件 '{componentName}' 的演示文件"
            
    except Exception as e:
        logger.error(f"获取组件演示代码时出错: {e}")
        return f"获取组件 '{componentName}' 演示代码时出错: {str(e)}"

@mcp.tool()
def list_components() -> str:
    """
    列出所有可用的element-plus组件
    """
    try:
        # 获取packages/components目录下的所有组件
        components_path = "packages/components"
        contents = get_directory_contents(components_path)
        
        if not contents:
            return "无法获取组件列表"
        
        # 过滤出组件目录
        components = []
        for item in contents:
            if item['type'] == 'dir' and not item['name'].startswith('.'):
                components.append(item['name'])
        
        components.sort()
        
        if components:
            component_list = "\n".join([f"- {comp}" for comp in components])
            return f"# Element Plus 可用组件列表\n\n{component_list}\n\n总计: {len(components)} 个组件"
        else:
            return "未找到任何组件"
            
    except Exception as e:
        logger.error(f"获取组件列表时出错: {e}")
        return f"获取组件列表时出错: {str(e)}"

@mcp.tool()
def get_component_metadata(componentName: Annotated[str, Field(description="Name of the element-plus component (e.g., 'avatar', 'button')")]) -> str:
    """
    获取指定element-plus组件的元数据信息
    """
    try:
        component_path = f"packages/components/{componentName.lower()}"
        
        # 获取组件目录内容
        contents = get_directory_contents(component_path)
        if not contents:
            return f"组件 '{componentName}' 不存在"
        
        metadata = {
            "name": componentName,
            "files": [],
            "dependencies": [],
            "description": ""
        }
        
        # 分析文件结构
        for item in contents:
            if item['type'] == 'file':
                metadata["files"].append({
                    "name": item['name'],
                    "size": item.get('size', 0),
                    "type": item['name'].split('.')[-1] if '.' in item['name'] else 'unknown'
                })
        
        # 尝试读取package.json获取依赖信息
        package_json_path = f"{component_path}/package.json"
        package_content = get_file_content(package_json_path)
        if package_content and not package_content.startswith("无法获取文件内容"):
            try:
                package_data = json.loads(package_content)
                metadata["description"] = package_data.get("description", "")
                metadata["dependencies"] = list(package_data.get("dependencies", {}).keys())
            except json.JSONDecodeError:
                pass
        
        # 格式化输出
        result = f"# Element Plus 组件元数据: {componentName}\n\n"
        result += f"**描述**: {metadata['description'] or '暂无描述'}\n\n"
        result += f"**文件列表**:\n"
        for file_info in metadata["files"]:
            result += f"- {file_info['name']} ({file_info['type']}, {file_info['size']} bytes)\n"
        
        if metadata["dependencies"]:
            result += f"\n**依赖项**:\n"
            for dep in metadata["dependencies"]:
                result += f"- {dep}\n"
        
        return result
        
    except Exception as e:
        logger.error(f"获取组件元数据时出错: {e}")
        return f"获取组件 '{componentName}' 元数据时出错: {str(e)}"

@mcp.tool()
def get_directory_structure(
    path: Annotated[str, Field(description="Path within the repository (default: packages/components)")] = "packages/components",
    owner: Annotated[str, Field(description="Repository owner (default: element-plus)")] = "element-plus",
    repo: Annotated[str, Field(description="Repository name (default: element-plus)")] = "element-plus",
    branch: Annotated[str, Field(description="Branch name (default: dev)")] = "dev"
) -> str:
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
            return f"无法获取目录结构: {path}"
        
        # 构建目录树
        result = f"# 目录结构: {owner}/{repo}/{path}\n\n"
        
        directories = []
        files = []
        
        for item in contents:
            if item['type'] == 'dir':
                directories.append(f"📁 {item['name']}/")
            else:
                size = item.get('size', 0)
                size_str = f" ({size} bytes)" if size > 0 else ""
                files.append(f"📄 {item['name']}{size_str}")
        
        # 先显示目录，再显示文件
        all_items = sorted(directories) + sorted(files)
        
        for item in all_items:
            result += f"{item}\n"
        
        result += f"\n总计: {len(directories)} 个目录, {len(files)} 个文件"
        
        return result
        
    except Exception as e:
        logger.error(f"获取目录结构时出错: {e}")
        return f"获取目录结构时出错: {str(e)}"
    
@click.command()
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="stdio",
    help="Transport type",
)
def main(transport: str):
    """主函数，启动MCP服务器"""
    logger.info("启动Element Plus MCP服务器...")
    logger.info(f"GitHub API Token: {'已配置' if get_config()['github_api_key'] else '未配置'}")
    if transport == "sse":
        # 加载环境变量，更新配置对象信息
        env_file = Path(__file__).parent.parent.parent / ".env"
        if env_file.exists():
            # 加载 .env 文件
            from dotenv import load_dotenv
            load_dotenv(env_file)
        mcp.run(transport="streamable-http")
    else:
        mcp.run(transport="stdio")

if __name__ == "__main__":
    main()