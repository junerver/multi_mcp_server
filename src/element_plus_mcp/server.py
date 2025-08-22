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

# Pydantic模型定义
class FileInfo(BaseModel):
    """文件信息结构"""
    name: str = Field(description="文件名")
    size: int = Field(description="文件大小（字节）")
    type: str = Field(description="文件类型/扩展名")

class ComponentMetadata(BaseModel):
    """组件元数据信息结构"""
    name: str = Field(description="组件名称")
    description: str = Field(description="组件描述")
    files: List[FileInfo] = Field(description="组件包含的文件列表")
    dependencies: List[str] = Field(description="组件依赖项列表")

class SourceFile(BaseModel):
    """源码文件结构"""
    filename: str = Field(description="文件名")
    language: str = Field(description="编程语言类型")
    content: str = Field(description="文件内容")

class ComponentSource(BaseModel):
    """组件源码信息结构"""
    component_name: str = Field(description="组件名称")
    source_files: List[SourceFile] = Field(description="源码文件列表")
    found: bool = Field(description="是否找到组件")
    error_message: Optional[str] = Field(description="错误信息（如果有）")

class DemoFile(BaseModel):
    """演示文件结构"""
    filename: str = Field(description="演示文件名")
    content: str = Field(description="演示代码内容")

class ComponentDemo(BaseModel):
    """组件演示代码信息结构"""
    component_name: str = Field(description="组件名称")
    demo_files: List[DemoFile] = Field(description="演示文件列表")
    found: bool = Field(description="是否找到演示代码")
    error_message: Optional[str] = Field(description="错误信息（如果有）")

class ComponentList(BaseModel):
    """组件列表信息结构"""
    components: List[str] = Field(description="组件名称列表")
    total_count: int = Field(description="组件总数")
    found: bool = Field(description="是否成功获取组件列表")
    error_message: Optional[str] = Field(description="错误信息（如果有）")

class DirectoryItem(BaseModel):
    """目录项结构"""
    name: str = Field(description="项目名称")
    type: str = Field(description="类型：dir（目录）或file（文件）")
    size: Optional[int] = Field(description="文件大小（字节），目录为None")

class DirectoryStructure(BaseModel):
    """目录结构信息"""
    path: str = Field(description="目录路径")
    owner: str = Field(description="仓库所有者")
    repo: str = Field(description="仓库名称")
    branch: str = Field(description="分支名称")
    items: List[DirectoryItem] = Field(description="目录项列表")
    directory_count: int = Field(description="目录数量")
    file_count: int = Field(description="文件数量")
    found: bool = Field(description="是否成功获取目录结构")
    error_message: Optional[str] = Field(description="错误信息（如果有）")

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
def get_component(componentName: Annotated[str, Field(description="Name of the element-plus component (e.g., 'avatar', 'button')")]) -> ComponentSource:
    """
    获取指定element-plus组件的源码
    """
    try:
        # element-plus组件通常在packages/components目录下
        component_path = f"packages/components/{componentName.lower()}"
        
        # 首先检查组件目录是否存在
        contents = get_directory_contents(component_path)
        if not contents:
            return ComponentSource(
                component_name=componentName,
                source_files=[],
                found=False,
                error_message=f"组件 '{componentName}' 不存在或无法访问"
            )
        
        # 查找主要的源码文件
        source_files = []
        for item in contents:
            if item['type'] == 'file' and item['name'].endswith(('.vue', '.ts', '.tsx')):
                file_content = get_file_content(item['path'])
                # 确定文件语言类型
                extension = item['name'].split('.')[-1]
                language_map = {
                    'vue': 'vue',
                    'ts': 'typescript',
                    'tsx': 'typescript'
                }
                language = language_map.get(extension, extension)
                
                source_files.append(SourceFile(
                    filename=item['name'],
                    language=language,
                    content=file_content
                ))
        
        if source_files:
            return ComponentSource(
                component_name=componentName,
                source_files=source_files,
                found=True,
                error_message=None
            )
        else:
            return ComponentSource(
                component_name=componentName,
                source_files=[],
                found=False,
                error_message=f"未找到组件 '{componentName}' 的源码文件"
            )
            
    except Exception as e:
        logger.error(f"获取组件源码时出错: {e}")
        return ComponentSource(
            component_name=componentName,
            source_files=[],
            found=False,
            error_message=f"获取组件 '{componentName}' 源码时出错: {str(e)}"
        )

@mcp.tool()
def get_component_demo(componentName: Annotated[str, Field(description="Name of the element-plus component (e.g., 'avatar', 'button')")]) -> ComponentDemo:
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
            return ComponentDemo(
                component_name=componentName,
                demo_files=[],
                found=False,
                error_message=f"未找到组件 '{componentName}' 的演示代码"
            )
        
        # 查找演示文件
        demo_files = []
        for item in contents:
            if item['type'] == 'file' and (item['name'].endswith('.vue') or 'demo' in item['name'].lower() or 'example' in item['name'].lower()):
                file_content = get_file_content(item['path'])
                demo_files.append(DemoFile(
                    filename=item['name'],
                    content=file_content
                ))
        
        if demo_files:
            return ComponentDemo(
                component_name=componentName,
                demo_files=demo_files,
                found=True,
                error_message=None
            )
        else:
            return ComponentDemo(
                component_name=componentName,
                demo_files=[],
                found=False,
                error_message=f"未找到组件 '{componentName}' 的演示文件"
            )
            
    except Exception as e:
        logger.error(f"获取组件演示代码时出错: {e}")
        return ComponentDemo(
            component_name=componentName,
            demo_files=[],
            found=False,
            error_message=f"获取组件 '{componentName}' 演示代码时出错: {str(e)}"
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
            return ComponentList(
                components=[],
                total_count=0,
                found=False,
                error_message="无法获取组件列表"
            )
        
        # 过滤出组件目录
        components = []
        for item in contents:
            if item['type'] == 'dir' and not item['name'].startswith('.'):
                components.append(item['name'])
        
        components.sort()
        
        if components:
            return ComponentList(
                components=components,
                total_count=len(components),
                found=True,
                error_message=None
            )
        else:
            return ComponentList(
                components=[],
                total_count=0,
                found=False,
                error_message="未找到任何组件"
            )
            
    except Exception as e:
        logger.error(f"获取组件列表时出错: {e}")
        return ComponentList(
            components=[],
            total_count=0,
            found=False,
            error_message=f"获取组件列表时出错: {str(e)}"
        )

@mcp.tool()
def get_component_metadata(componentName: Annotated[str, Field(description="Name of the element-plus component (e.g., 'avatar', 'button')")]) -> ComponentMetadata:
    """
    获取指定element-plus组件的元数据信息
    """
    try:
        component_path = f"packages/components/{componentName.lower()}"
        
        # 获取组件目录内容
        contents = get_directory_contents(component_path)
        if not contents:
            return ComponentMetadata(
                name=componentName,
                description="",
                files=[],
                dependencies=[]
            )
        
        files = []
        dependencies = []
        description = ""
        
        # 分析文件结构
        for item in contents:
            if item['type'] == 'file':
                files.append(FileInfo(
                    name=item['name'],
                    size=item.get('size', 0),
                    type=item['name'].split('.')[-1] if '.' in item['name'] else 'unknown'
                ))
        
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
        
        return ComponentMetadata(
            name=componentName,
            description=description,
            files=files,
            dependencies=dependencies
        )
        
    except Exception as e:
        logger.error(f"获取组件元数据时出错: {e}")
        return ComponentMetadata(
            name=componentName,
            description=f"获取组件 '{componentName}' 元数据时出错: {str(e)}",
            files=[],
            dependencies=[]
        )

@mcp.tool()
def get_directory_structure(
    path: Annotated[str, Field(description="Path within the repository (default: packages/components)")] = "packages/components",
    owner: Annotated[str, Field(description="Repository owner (default: element-plus)")] = "element-plus",
    repo: Annotated[str, Field(description="Repository name (default: element-plus)")] = "element-plus",
    branch: Annotated[str, Field(description="Branch name (default: dev)")] = "dev"
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
                error_message=f"无法获取目录结构: {path}"
            )
        
        # 构建目录项列表
        items = []
        directory_count = 0
        file_count = 0
        
        for item in contents:
            if item['type'] == 'dir':
                directory_count += 1
                items.append(DirectoryItem(
                    name=item['name'],
                    type='dir',
                    size=None
                ))
            else:
                file_count += 1
                items.append(DirectoryItem(
                    name=item['name'],
                    type='file',
                    size=item.get('size', 0)
                ))
        
        # 按类型和名称排序：先目录后文件，同类型按名称排序
        items.sort(key=lambda x: (x.type == 'file', x.name))
        
        return DirectoryStructure(
            path=path,
            owner=owner,
            repo=repo,
            branch=branch,
            items=items,
            directory_count=directory_count,
            file_count=file_count,
            found=True,
            error_message=None
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
            error_message=f"获取目录结构时出错: {str(e)}"
        )
    
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