import os
from urllib.parse import quote
from typing import List, Dict, Any
import requests


def get_config() -> Dict[str, Any]:
    """获取配置信息"""
    return {
        "github_api_key": os.getenv("GITHUB_API_KEY", ""),
        "element_plus_repo": {"owner": "element-plus", "repo": "element-plus", "branch": "dev"},
        "github_api_base": "https://api.github.com",
    }


class GitHubAPIError(Exception):
    """GitHub API错误异常类"""

    pass


def get_github_headers() -> Dict[str, str]:
    """获取GitHub API请求头"""
    headers = {"Accept": "application/vnd.github.v3+json", "User-Agent": "ElementPlus-MCP-Server"}
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
        if data.get("encoding") == "base64":
            import base64

            return base64.b64decode(data["content"]).decode("utf-8")
        else:
            return data.get("content", "")
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
