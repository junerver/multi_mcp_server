# Element Plus MCP 服务器

这是一个基于 Model Context Protocol (MCP) 的 Element Plus 组件库服务器，允许 AI 助手访问和获取 Element Plus Vue.js 组件的源码、演示代码和元数据信息。

## 功能特性

- 🎯 **组件源码获取** - 获取指定 Element Plus 组件的完整源码
- 📖 **演示代码** - 获取组件的使用演示和示例代码
- 📋 **组件列表** - 列出所有可用的 Element Plus 组件
- 🔍 **元数据信息** - 获取组件的详细元数据，包括文件结构和依赖
- 📁 **目录结构** - 浏览 Element Plus 仓库的目录结构
- 🔑 **GitHub API 集成** - 支持 GitHub API Token 以提高请求限制

## 可用工具

### 1. get_component
获取指定 Element Plus 组件的源码
- **参数**: `componentName` (string) - 组件名称，如 'button', 'input', 'table'
- **返回**: 组件的完整源码文件内容

### 2. get_component_demo
获取组件的演示代码和使用示例
- **参数**: `componentName` (string) - 组件名称
- **返回**: 组件的演示代码和使用示例

### 3. list_components
列出所有可用的 Element Plus 组件
- **参数**: 无
- **返回**: 所有可用组件的列表

### 4. get_component_metadata
获取组件的元数据信息
- **参数**: `componentName` (string) - 组件名称
- **返回**: 组件的文件结构、依赖项等元数据

### 5. get_directory_structure
获取仓库的目录结构
- **参数**: 
  - `path` (string, 可选) - 仓库路径，默认为 "packages/components"
  - `owner` (string, 可选) - 仓库所有者，默认为 "element-plus"
  - `repo` (string, 可选) - 仓库名称，默认为 "element-plus"
  - `branch` (string, 可选) - 分支名称，默认为 "dev"
- **返回**: 指定路径的目录结构

## 配置

### GitHub API Token (推荐)
为了获得更高的 API 请求限制，建议配置 GitHub API Token：

```bash
# 设置环境变量
export GITHUB_API_KEY=your_github_token_here
```

### 服务器配置
- **主机**: 0.0.0.0
- **端口**: 3003
- **传输协议**: streamable-http

## 使用方法

### 启动服务器
```bash
# 使用 uv 运行
uv run element_plus_mcp

# 或者直接运行 Python 文件
python src/element_plus_mcp/server.py
```

### 示例用法

1. **获取按钮组件源码**:
   ```
   工具: get_component
   参数: {"componentName": "button"}
   ```

2. **列出所有组件**:
   ```
   工具: list_components
   参数: {}
   ```

3. **获取表格组件演示**:
   ```
   工具: get_component_demo
   参数: {"componentName": "table"}
   ```

## 技术实现

- **框架**: FastMCP (Model Context Protocol)
- **语言**: Python 3.13+
- **依赖**: requests, pydantic
- **数据源**: Element Plus GitHub 仓库 (https://github.com/element-plus/element-plus)

## 错误处理

服务器包含完善的错误处理机制：
- GitHub API 请求失败时的重试和错误报告
- 组件不存在时的友好提示
- 网络超时和连接错误的处理
- 详细的日志记录用于调试

## 注意事项

- 默认使用 Element Plus 的 `dev` 分支
- 组件名称不区分大小写
- 建议配置 GitHub API Token 以避免请求限制
- 服务器启动时会显示 GitHub API Token 的配置状态