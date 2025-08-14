# MCP 文件系统服务器 (Python版)

基于 FastMCP 框架实现的 Model Context Protocol (MCP) 文件系统服务器，提供安全的文件和目录操作功能。

## 功能特性

### 🔒 安全特性
- **路径验证**: 防止路径遍历攻击
- **目录访问控制**: 限制访问指定的安全目录
- **权限检查**: 验证文件读写权限

### 📁 文件操作
- `read_text_file`: 读取文本文件内容
- `read_media_file`: 读取媒体文件并转换为base64编码
- `write_file`: 写入文件内容
- `read_multiple_files`: 批量读取多个文件
- `move_file`: 移动/重命名文件和目录

### 📂 目录操作
- `create_directory`: 创建目录
- `list_directory`: 列出目录内容
- `list_allowed_directories`: 列出允许访问的目录

### 🔍 搜索和元数据
- `search_files`: 递归搜索文件和目录（支持通配符）
- `get_file_info`: 获取文件/目录详细信息

### ✏️ 高级编辑
- `edit_file`: 高级文件编辑功能
  - 支持模式匹配和替换
  - 保持缩进风格
  - 干运行模式预览
  - Git风格差异输出

## 安装和使用

### 1. 安装依赖

```bash
pip install fastmcp mcp[cli]
```

### 2. 配置允许访问的目录


1. 复制环境变量配置模板：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，设置允许访问的目录：
```bash
# 配置允许访问的目录列表（用分号分隔多个目录）
MCP_ALLOWED_DIRECTORIES=C:\Users\YourName\Documents;D:\Projects;E:\Data
```


### 3. 启动服务器

```bash
python server.py
```


## 配置说明

### 环境变量

- `MCP_ALLOWED_DIRECTORIES`: 配置允许访问的目录列表
  - 使用分号(`;`)分隔多个目录路径
  - 支持相对路径和绝对路径
  - 如果目录不存在，将被自动忽略
  - 如果未设置，默认只允许访问当前工作目录

### MCP 客户端配置

在您的 MCP 客户端配置中添加：

```json
{
  "mcpServers": {
    "FileSystem": {
      "url": "http://localhost:3001/mcp"
    }
  }
}
```

## 安全注意事项

1. **目录限制**: 服务器只能访问环境变量或代码中指定的目录
2. **路径验证**: 所有路径都会进行安全验证，防止路径遍历攻击
3. **权限检查**: 操作前会检查文件/目录的读写权限
4. **错误处理**: 提供详细的错误信息，便于调试
5. **环境变量安全**: 请确保 `MCP_ALLOWED_DIRECTORIES` 只包含安全的目录路径