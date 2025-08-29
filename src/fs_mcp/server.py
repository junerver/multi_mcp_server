"""
MCP服务器
支持文件系统操作
"""

import base64
import logging
import os
import shutil
import stat
import sys
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

import click
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from starlette.middleware.cors import CORSMiddleware

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Create an MCP server
mcp = FastMCP("FileSystem")


# 添加资源支持
@mcp.resource("file://system")
def get_system_resource() -> Dict[str, Any]:
    """
    提供 file://system 资源接口支持。
    允许通过资源URI访问文件系统信息。
    """
    try:
        # 返回允许的目录列表
        return {
            "contents": [
                {
                    "type": "text",
                    "text": "\n".join(ALLOWED_DIRECTORIES)
                    if ALLOWED_DIRECTORIES
                    else "No allowed directories configured",
                }
            ]
        }
    except Exception as e:
        return {"contents": [{"type": "text", "text": f"Error accessing resource: {e}"}]}


# 全局变量：允许访问的目录列表
ALLOWED_DIRECTORIES: List[str] = []


def initialize_allowed_directories(*directories: str) -> None:
    """
    初始化允许访问的目录列表。
    支持通过环境变量 MCP_ALLOWED_DIRECTORIES 配置（用分号分隔多个目录）。
    """
    global ALLOWED_DIRECTORIES
    # 判断 .env 文件是否存在
    env_file = Path(__file__).parent.parent.parent / ".env"
    if env_file.exists():
        # 加载 .env 文件
        from dotenv import load_dotenv

        load_dotenv(env_file)

    # 首先检查环境变量
    env_dirs = os.getenv("MCP_ALLOWED_DIRECTORIES")
    if env_dirs:
        # 使用分号分隔多个目录路径
        env_directories = [d.strip() for d in env_dirs.split(";") if d.strip()]
        directories = tuple(env_directories) + directories
    logger.info(f"MCP FileSystem Server - Configured directories: {directories}")

    ALLOWED_DIRECTORIES = [os.path.abspath(d) for d in directories if os.path.exists(d)]
    if not ALLOWED_DIRECTORIES:
        # 如果没有指定目录，默认允许当前工作目录
        ALLOWED_DIRECTORIES = [os.getcwd()]

    logging.info(f"MCP FileSystem Server - Allowed directories: {ALLOWED_DIRECTORIES}")


def validate_path(path: str) -> str:
    """
    验证路径是否在允许的目录范围内。
    返回规范化的绝对路径。
    """
    abs_path = os.path.abspath(path)

    # 检查路径是否在允许的目录范围内
    for allowed_dir in ALLOWED_DIRECTORIES:
        try:
            # 规范化路径并转换为小写进行比较（Windows大小写不敏感）
            norm_abs_path = os.path.normpath(abs_path).lower()
            norm_allowed_dir = os.path.normpath(allowed_dir).lower()

            # 使用 os.path.commonpath 检查路径是否在允许的目录下
            common_path = os.path.commonpath([norm_abs_path, norm_allowed_dir])
            if common_path == norm_allowed_dir:
                return abs_path
        except ValueError:
            # 不同驱动器的路径会抛出 ValueError
            continue

    raise PermissionError(f"Access denied: Path '{path}' is outside allowed directories")


# 初始化允许的目录（支持环境变量配置）
initialize_allowed_directories()


@mcp.tool()
def read_text_file(
    path: str = Field(..., description="要读取的文件路径"),
    head: int = Field(0, description="要读取的文件的前N行"),
    tail: int = Field(0, description="要读取的文件的后N行"),
    encoding: str = Field("utf-8", description="文件的编码"),
) -> Dict[str, Any]:
    """
    从文件系统中读取文件的完整内容为文本格式。
    支持多种文本编码，并在文件无法读取时提供详细的错误信息。
    当需要检查单个文件的内容时使用此工具。
    使用'head'参数仅读取文件的前N行，
    或使用'tail'参数仅读取文件的最后N行。
    无论文件扩展名如何，都将其作为文本文件处理。
    仅在允许的目录范围内工作。
    """
    try:
        validated_path = validate_path(path)
        with open(validated_path, "r", encoding=encoding) as f:
            content = f.read()

            # Handle head/tail parameters
            if head > 0:
                lines = content.splitlines()
                content = "\n".join(lines[:head])
            elif tail > 0:
                lines = content.splitlines()
                content = "\n".join(lines[-tail:])

        return {"content": [{"type": "text", "text": content}]}

    except FileNotFoundError:
        return {"content": [{"type": "text", "text": f"File not found: {path}"}]}
    except PermissionError:
        return {"content": [{"type": "text", "text": f"Permission denied: {path}"}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error reading file: {e}"}]}


@mcp.tool()
def read_media_file(path: str = Field(..., description="要读取的媒体文件路径")) -> Dict[str, Any]:
    """
    读取媒体文件（图片、音频等）并返回base64编码的数据。
    支持多种媒体格式，包括图片（png, jpg, gif等）和音频（mp3, wav等）。
    根据文件扩展名自动识别MIME类型。
    """
    try:
        validated_path = validate_path(path)
        # 验证文件是否存在
        if not os.path.exists(validated_path):
            raise FileNotFoundError(f"File not found: {path}")

        # 获取文件扩展名
        extension = os.path.splitext(validated_path)[1].lower()

        # 定义MIME类型映射
        mime_types: Dict[str, str] = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".webp": "image/webp",
            ".bmp": "image/bmp",
            ".svg": "image/svg+xml",
            ".mp3": "audio/mpeg",
            ".wav": "audio/wav",
            ".ogg": "audio/ogg",
            ".flac": "audio/flac",
        }

        # 获取MIME类型
        mime_type = mime_types.get(extension, "application/octet-stream")

        # 读取文件并转换为base64
        with open(validated_path, "rb") as f:
            file_data = f.read()
            base64_data = base64.b64encode(file_data).decode("utf-8")

        # 确定内容类型
        if mime_type.startswith("image/"):
            content_type = "image"
        elif mime_type.startswith("audio/"):
            content_type = "audio"
        else:
            content_type = "blob"

        return {"content": [{"type": content_type, "data": base64_data, "mimeType": mime_type}]}

    except FileNotFoundError as e:
        return {"content": [{"type": "text", "text": str(e)}]}
    except PermissionError:
        return {"content": [{"type": "text", "text": f"Permission denied: {path}"}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error reading media file: {e}"}]}


@mcp.tool()
def write_file(
    path: str = Field(..., description="要写入的文件路径"),
    content: str = Field(..., description="要写入的文件内容"),
    encoding: str = Field("utf-8", description="文件的编码"),
) -> Dict[str, Any]:
    """
    向文件系统中写入文本内容。
    支持多种文本编码，并在文件无法写入时提供详细的错误信息。
    当需要将文本内容写入文件时使用此工具。
    仅在允许的目录范围内工作。
    """
    try:
        validated_path = validate_path(path)
        # 确保父目录存在
        os.makedirs(os.path.dirname(validated_path), exist_ok=True)
        with open(validated_path, "w", encoding=encoding) as f:
            f.write(content)
        return {"content": [{"type": "text", "text": f"File written successfully: {path}"}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error writing file: {e}"}]}


@mcp.tool()
def create_directory(path: str = Field(..., description="要创建的目录路径")) -> Dict[str, Any]:
    """
    创建新目录或确保目录存在。
    如果需要，会创建父目录。
    如果目录已存在，则静默成功。
    """
    try:
        validated_path = validate_path(path)
        os.makedirs(validated_path, exist_ok=True)
        return {"content": [{"type": "text", "text": f"Directory created successfully: {path}"}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error creating directory: {e}"}]}


@mcp.tool()
def list_directory(path: str = Field(..., description="要列出内容的目录路径")) -> Dict[str, Any]:
    """
    列出目录内容，文件和目录分别用 [FILE] 和 [DIR] 前缀标识。
    """
    try:
        validated_path = validate_path(path)
        if not os.path.isdir(validated_path):
            return {"content": [{"type": "text", "text": f"Error: '{path}' is not a directory"}]}

        items = []
        for item in sorted(os.listdir(validated_path)):
            item_path = os.path.join(validated_path, item)
            if os.path.isdir(item_path):
                items.append(f"[DIR] {item}")
            else:
                items.append(f"[FILE] {item}")

        if not items:
            return {"content": [{"type": "text", "text": "Directory is empty"}]}

        return {"content": [{"type": "text", "text": "\n".join(items)}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error listing directory: {e}"}]}


@mcp.tool()
def list_allowed_directories() -> Dict[str, Any]:
    """
    列出服务器允许访问的所有目录。
    无需输入参数。
    """
    if not ALLOWED_DIRECTORIES:
        return {"content": [{"type": "text", "text": "No allowed directories configured"}]}

    return {
        "content": [{"type": "text", "text": "\n".join([f"[ALLOWED] {dir_path}" for dir_path in ALLOWED_DIRECTORIES])}]
    }


@mcp.tool()
def read_multiple_files(paths: List[str] = Field(..., description="要读取的文件路径列表")) -> Dict[str, Any]:
    """
    同时读取多个文件。
    失败的读取不会停止整个操作。
    """
    results = []
    for path in paths:
        try:
            validated_path = validate_path(path)
            with open(validated_path, "r", encoding="utf-8") as f:
                content = f.read()
            results.append(f"=== {path} ===\n{content}")
        except Exception as e:
            results.append(f"=== {path} ===\nError: {e}")

    return {"content": [{"type": "text", "text": "\n\n".join(results)}]}


@mcp.tool()
def move_file(
    source: str = Field(..., description="源文件或目录路径"),
    destination: str = Field(..., description="目标文件或目录路径"),
) -> Dict[str, Any]:
    """
    移动或重命名文件和目录。
    如果目标已存在则失败。
    """
    try:
        validated_source = validate_path(source)
        validated_destination = validate_path(destination)

        if not os.path.exists(validated_source):
            return {"content": [{"type": "text", "text": f"Error: Source '{source}' does not exist"}]}

        if os.path.exists(validated_destination):
            return {"content": [{"type": "text", "text": f"Error: Destination '{destination}' already exists"}]}

        # 确保目标目录存在
        dest_dir = os.path.dirname(validated_destination)
        if dest_dir:
            os.makedirs(dest_dir, exist_ok=True)

        shutil.move(validated_source, validated_destination)
        return {"content": [{"type": "text", "text": f"Successfully moved '{source}' to '{destination}'"}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error moving file: {e}"}]}


@mcp.tool()
def search_files(
    path: str = Field(..., description="搜索的起始目录路径"),
    pattern: str = Field(..., description="搜索模式"),
    exclude_patterns: Optional[List[str]] = Field(default=None, description="要排除的模式列表"),
) -> Dict[str, Any]:
    """
    递归搜索文件和目录。
    支持通配符模式匹配，不区分大小写。
    返回匹配项的完整路径。
    """
    try:
        validated_path = validate_path(path)
        if not os.path.isdir(validated_path):
            return {"content": [{"type": "text", "text": f"Error: '{path}' is not a directory"}]}

        matches = []
        pattern_lower = pattern.lower()
        exclude_patterns_lower = [p.lower() for p in (exclude_patterns or [])]

        for root, dirs, files in os.walk(validated_path):
            # 检查目录
            for dir_name in dirs:
                if pattern_lower in dir_name.lower():
                    full_path = os.path.join(root, dir_name)
                    # 检查是否应该排除
                    should_exclude = False
                    for exclude_pattern in exclude_patterns_lower:
                        if exclude_pattern in dir_name.lower():
                            should_exclude = True
                            break
                    if not should_exclude:
                        matches.append(f"[DIR] {full_path}")

            # 检查文件
            for file_name in files:
                if pattern_lower in file_name.lower():
                    full_path = os.path.join(root, file_name)
                    # 检查是否应该排除
                    should_exclude = False
                    for exclude_pattern in exclude_patterns_lower:
                        if exclude_pattern in file_name.lower():
                            should_exclude = True
                            break
                    if not should_exclude:
                        matches.append(f"[FILE] {full_path}")

        if not matches:
            return {
                "content": [{"type": "text", "text": f"No files or directories found matching pattern '{pattern}'"}]
            }

        return {"content": [{"type": "text", "text": "\n".join(matches)}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error searching files: {e}"}]}


@mcp.tool()
def get_file_info(path: str = Field(..., description="要获取信息的文件或目录路径")) -> Dict[str, Any]:
    """
    获取文件或目录的详细元数据。
    包括大小、创建时间、修改时间、访问时间、类型和权限。
    """
    try:
        validated_path = validate_path(path)
        if not os.path.exists(validated_path):
            return {"content": [{"type": "text", "text": f"Error: Path '{path}' does not exist"}]}

        stat_info = os.stat(validated_path)

        # 确定文件类型
        if os.path.isfile(validated_path):
            file_type = "file"
        elif os.path.isdir(validated_path):
            file_type = "directory"
        elif os.path.islink(validated_path):
            file_type = "symlink"
        else:
            file_type = "other"

        # 格式化时间
        def format_time(timestamp):
            return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

        # 获取权限信息
        permissions = stat.filemode(stat_info.st_mode)

        info_text = f"""Path: {path}
Type: {file_type}
Size: {stat_info.st_size} bytes ({_format_size(stat_info.st_size)})
Created: {format_time(stat_info.st_ctime)}
Modified: {format_time(stat_info.st_mtime)}
Accessed: {format_time(stat_info.st_atime)}
Permissions: {permissions}"""

        return {"content": [{"type": "text", "text": info_text}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error getting file info: {e}"}]}


def _format_size(size_bytes: int) -> str:
    """
    将字节大小格式化为人类可读的格式。
    """
    if size_bytes == 0:
        return "0 B"

    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1

    return f"{size_bytes:.1f} {size_names[i]}"


class EditOperation(BaseModel):
    old_text: str = Field(..., description="要搜索的文本（可以是子字符串）")
    new_text: str = Field(..., description="要替换的文本")


@mcp.tool()
def edit_file(
    path: str = Field(..., description="要编辑的文件路径"),
    edits: List[EditOperation] = Field(..., description="编辑操作列表"),
    dry_run: bool = Field(default=False, description="预览更改而不应用（默认：false）"),
) -> Dict[str, Any]:
    """
    使用高级模式匹配和格式化进行选择性编辑。
    功能特性：
    - 基于行和多行内容匹配
    - 空白符规范化与缩进保持
    - 正确定位的多个同时编辑
    - 缩进样式检测和保持
    - Git风格的差异输出与上下文
    - 干运行模式预览更改

    最佳实践：始终先使用干运行预览更改，然后再应用。
    """
    try:
        validated_path = validate_path(path)
        if not os.path.exists(validated_path):
            return {"content": [{"type": "text", "text": f"Error: File '{path}' does not exist"}]}

        # 读取文件内容
        with open(validated_path, "r", encoding="utf-8") as f:
            original_content = f.read()

        lines = original_content.splitlines()
        modified_content = original_content
        changes_made = []

        # 检测缩进样式
        indent_style = _detect_indent_style(lines)

        # 应用编辑操作
        for i, edit_op in enumerate(edits):
            old_text = edit_op.old_text
            new_text = edit_op.new_text

            if old_text in modified_content:
                # 记录更改信息
                old_lines = old_text.splitlines()
                new_lines = new_text.splitlines()

                # 保持缩进风格
                if old_lines and new_lines:
                    # 检测原始文本的缩进
                    original_indent = _get_line_indent(old_lines[0])
                    if original_indent:
                        # 应用相同的缩进到新文本
                        new_lines = [original_indent + line.lstrip() if line.strip() else line for line in new_lines]
                        new_text = "\n".join(new_lines)

                # 执行替换
                modified_content = modified_content.replace(old_text, new_text, 1)

                changes_made.append(
                    {
                        "operation": i + 1,
                        "old_text": old_text,
                        "new_text": new_text,
                        "lines_removed": len(old_lines),
                        "lines_added": len(new_lines),
                    }
                )
            else:
                changes_made.append({"operation": i + 1, "error": f"Text not found: '{old_text[:50]}...'"})

        # 生成差异
        diff_output = _generate_diff(original_content, modified_content, path)

        result = {
            "path": path,
            "dry_run": dry_run,
            "changes_made": changes_made,
            "diff": diff_output,
            "indent_style": indent_style,
        }

        if dry_run:
            result["preview"] = modified_content
            result_text = f"DRY RUN - File: {path}\n"
            result_text += f"Indent style: {indent_style}\n\n"
            result_text += "Changes that would be made:\n"
            for change in changes_made:
                if "error" in change:
                    result_text += f"Operation {change['operation']}: {change['error']}\n"
                else:
                    result_text += f"Operation {change['operation']}: Replace {change['lines_removed']} lines with {change['lines_added']} lines\n"
            result_text += f"\nDiff:\n{diff_output}"
            return {"content": [{"type": "text", "text": result_text}]}
        else:
            # 应用更改
            with open(validated_path, "w", encoding="utf-8") as f:
                f.write(modified_content)
            result_text = f"File edited successfully: {path}\n"
            result_text += f"Indent style: {indent_style}\n\n"
            result_text += "Changes made:\n"
            for change in changes_made:
                if "error" in change:
                    result_text += f"Operation {change['operation']}: {change['error']}\n"
                else:
                    result_text += f"Operation {change['operation']}: Replace {change['lines_removed']} lines with {change['lines_added']} lines\n"
            result_text += f"\nDiff:\n{diff_output}"
            return {"content": [{"type": "text", "text": result_text}]}

    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error editing file: {e}"}]}

@mcp.tool()
def delete_file(path: str = Field(..., description="要删除的文件路径")) -> Dict[str, Any]:
    """
    删除指定的文件，【危险操作】请谨慎使用。
    """
    try:
        validated_path = validate_path(path)
        if not os.path.exists(validated_path):
            return {"content": [{"type": "text", "text": f"Error: File '{path}' does not exist"}]}
        os.remove(validated_path)
        return {"content": [{"type": "text", "text": f"File deleted successfully: {path}"}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error deleting file: {e}"}]}

def _detect_indent_style(lines: List[str]) -> str:
    """
    检测文件的缩进样式。
    """
    tab_count = 0
    space_count = 0

    for line in lines:
        if line.startswith("\t"):
            tab_count += 1
        elif line.startswith(" "):
            space_count += 1

    if tab_count > space_count:
        return "tabs"
    elif space_count > 0:
        return "spaces"
    else:
        return "mixed"


def _get_line_indent(line: str) -> str:
    """
    获取行的缩进部分。
    """
    indent = ""
    for char in line:
        if char in [" ", "\t"]:
            indent += char
        else:
            break
    return indent


def _generate_diff(original: str, modified: str, filename: str) -> str:
    """
    生成Git风格的差异输出。
    """
    import difflib

    original_lines = original.splitlines(keepends=True)
    modified_lines = modified.splitlines(keepends=True)

    diff = difflib.unified_diff(
        original_lines, modified_lines, fromfile=f"a/{filename}", tofile=f"b/{filename}", lineterm=""
    )

    return "".join(diff)


@click.command()
@click.option(
    "--transport",
    type=click.Choice(["stdio", "streamable", "sse"]),
    default="stdio",
    help="Transport type",
)
@click.option("--port", type=int, default=3001, help="Port to listen on")
def main(transport: str, port: int):
    """主函数，启动MCP服务器"""
    def run_server(app):
        starlette_app = CORSMiddleware(
            app,
            allow_origins=["*"],  # Allow all origins - adjust as needed for production
            allow_methods=["GET", "POST", "DELETE"],  # MCP streamable HTTP methods
            expose_headers=["Mcp-Session-Id"],
        )
        import uvicorn
        uvicorn.run(starlette_app, host="0.0.0.0", port=port)
    if transport == "sse":
        run_server(mcp.sse_app())
    elif transport == "streamable":
        run_server(mcp.streamable_http_app())
    else:
        mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
