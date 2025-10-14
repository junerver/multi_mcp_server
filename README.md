# MCP Server 测试项目

这是一个基于 Model Context Protocol (MCP) 的多功能服务器测试项目，提供了文件系统操作、数据库访问、模板管理、设备控制等多种 MCP 服务。

## 📋 目录

- [快速开始](#快速开始)
- [项目架构](#项目架构)
- [MCP 服务列表](#mcp-服务列表)
- [环境配置](#环境配置)
- [客户端配置](#客户端配置)
- [开发指南](#开发指南)
- [调试与故障排除](#调试与故障排除)

## 🚀 快速开始

### 环境要求

- Python >= 3.13
- uv (现代 Python 包管理工具)

### 安装 uv

**Windows 系统:**
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**其他系统:** 请参考 [uv 官方文档](https://docs.astral.sh/uv/)

### 项目初始化

```bash
# 克隆项目后，同步依赖
uv sync

# 安装 pre-commit hooks
pre-commit install
```

### 启动服务

```bash
# 启动文件系统服务 (端口 3001)
uv run fs_mcp

# 启动 MySQL 服务 (端口 3004)
uv run mysql_mcp

# 启动模板服务 (端口 3005)
uv run template_mcp

# 启动演示服务 (端口 3006)
uv run demo_mcp
```

## 🏗️ 项目架构

```
src/
├── common/                 # 公共组件
│   ├── mcp_cli.py         # MCP CLI 工具和传输协议支持
│   └── cache.py           # 缓存实现
├── fs_mcp/               # 文件系统服务
├── element_plus_mcp/     # Element Plus 组件服务
├── mysql_mcp/            # MySQL 数据库服务
├── template_mcp/         # 模板服务
├── knowledge_mcp/        # 知识库服务
└── demo_mcp/             # 演示服务
```

### 核心特性

- **多传输协议支持**: stdio、streamable-http、SSE
- **CORS 支持**: 内置跨域处理，支持浏览器环境
- **统一错误处理**: 标准化的错误响应格式
- **性能优化**: 内置缓存机制
- **类型安全**: 完整的类型注解和 Pydantic 验证
- **跨平台兼容**: Windows/Linux/macOS 支持

## 🔧 MCP 服务列表

### 1. 文件系统服务 (`fs_mcp`)
**端口**: 3001
**启动命令**: `uv run fs_mcp`

**主要功能:**
- 文件读写操作 (支持多种编码)
- 目录创建、列表、搜索
- 文件编辑 (Git 风格差异输出)
- 媒体文件处理 (图片、音频)
- ZIP 压缩/解压缩
- 路径安全验证

**环境变量:**
```bash
MCP_ALLOWED_DIRECTORIES="/path/to/dir1;/path/to/dir2"
```

### 2. Element Plus 服务 (`element_plus_mcp`)
**端口**: 3003
**启动命令**: `uv run element_plus_mcp`

**主要功能:**
- Element Plus 组件文档查询
- 组件示例代码获取

### 3. MySQL 服务 (`mysql_mcp`)
**端口**: 3004
**启动命令**: `uv run mysql_mcp`

**主要功能:**
- 数据库表结构查询
- SQL 查询执行 (仅支持 SELECT)
- 表信息缓存
- 模板上下文生成

**环境变量:**
```bash
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=username
MYSQL_PASSWORD=password
MYSQL_DATABASE=database_name
```

### 4. 模板服务 (`template_mcp`)
**端口**: 3005
**启动命令**: `uv run template_mcp`

**主要功能:**
- 代码模板管理 (Java、Vue、JavaScript 等)
- 模板分类和搜索
- 示例代码获取
- Velocity 模板支持

**模板类别:**
- 后端代码: Domain、Mapper、Service、Controller
- 前端代码: Vue 组件、API 接口
- 数据库脚本: SQL 脚本

### 5. 知识库服务 (`knowledge_mcp`)
**功能**: 知识库和文档管理服务

### 6. 演示服务 (`demo_mcp`)
**端口**: 3006
**启动命令**: `uv run demo_mcp`

**主要功能:**
- 基础数学运算
- 设备动作执行 (`exec_action`)
- 设备状态查询 (`query_status`)

**设备控制工具:**
```python
# 执行设备动作
exec_action(
    product_id="产品ID",
    device_id="设备ID",
    action_flag="动作标识",
    action_params={"param1": "value1", "param2": "value2"}
)

# 查询设备状态
query_status(
    product_id="产品ID",
    device_id="设备ID",
    status_flag="状态标识"
)
```

### 7. 嵌入工具
- **文本嵌入**: `uv run embed`
- **搜索测试**: `uv run test_search`

## ⚙️ 环境配置

### 环境变量文件

创建 `.env` 文件 (参考 `.env.example`):

```bash
# 文件系统服务
MCP_ALLOWED_DIRECTORIES="/allowed/path1;/allowed/path2"

# MySQL 服务
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=your_database
```

### 开发环境

```bash
# 代码检查
uv run ruff check

# 代码格式化
uv run ruff format

# 运行测试
uv run pytest
```

## 🔌 客户端配置

### Trae 客户端配置

#### HTTP 传输协议
```json
{
  "mcpServers": {
    "FileSystem": {
      "url": "http://localhost:3001/mcp",
      "headers": {
        "X-API-KEY": "your-api-key"
      }
    },
    "MySQL": {
      "url": "http://localhost:3004/mcp"
    }
  }
}
```

#### stdio 传输协议
```json
{
  "mcpServers": {
    "FileSystem": {
      "command": "uv",
      "args": [
        "--directory",
        "E:/GitHub/All_in_Ai/test_mcp_server",
        "run",
        "fs_mcp"
      ],
      "env": {
        "MCP_ALLOWED_DIRECTORIES": "D:\\dev;E:\\app;"
      }
    },
    "MySQL": {
      "command": "uv",
      "args": [
        "--directory",
        "E:/GitHub/All_in_Ai/test_mcp_server",
        "run",
        "mysql_mcp"
      ]
    }
  }
}
```

### 传输协议说明

| 协议 | 描述 | 适用场景 | 注意事项 |
|------|------|----------|----------|
| stdio | 标准输入输出 | 本地开发、命令行 | 浏览器环境不可用 |
| streamable | HTTP 流式 | Web 应用、远程访问 | 需要 CORS 支持 |
| sse | Server-Sent Events | 实时数据推送 | 需要 CORS 支持 |

## 🛠️ 开发指南

### 添加新的 MCP 服务

1. 在 `src/` 目录下创建新服务模块
2. 继承通用 CLI 工具和缓存组件
3. 实现服务特定的工具函数
4. 在 `pyproject.toml` 中添加启动脚本
5. 更新文档和配置示例

### 代码规范

- 使用 `ruff` 进行代码检查和格式化
- 遵循 Python 类型注解规范
- 使用 Pydantic 进行参数验证
- 添加详细的函数文档字符串

### 安全考虑

- 文件系统操作使用路径验证
- SQL 查询限制为 SELECT 语句
- 环境变量存储敏感配置
- 实现 CORS 策略保护 Web 接口

## 🐛 调试与故障排除

### MCP Inspector 调试

```bash
# 调试文件系统服务
npx @modelcontextprotocol/inspector uv --directory E:/GitHub/All_in_Ai/test_mcp_server run fs_mcp

# 调试 MySQL 服务
npx @modelcontextprotocol/inspector uv --directory E:/GitHub/All_in_Ai/test_mcp_server run mysql_mcp
```

### 常见问题

#### 1. 跨域访问错误
**问题**: 使用 `streamable-http` 协议时出现跨域拒绝
**解决**: 服务已内置 CORS 中间件，确保使用正确的协议

#### 2. stdio 在浏览器中不可用
**问题**: 浏览器环境出现 `child_process` 错误
**原因**: 浏览器不支持 `child_process.spawn`
**解决**: 使用 `streamable` 或 `sse` 协议

#### 3. 环境变量未生效
**问题**: 服务无法读取环境变量
**解决**:
- 确保 `.env` 文件在项目根目录
- 检查环境变量名称拼写
- 重启服务使配置生效

#### 4. 权限错误
**问题**: 文件操作出现权限拒绝
**解决**:
- 检查 `MCP_ALLOWED_DIRECTORIES` 配置
- 确保目录路径正确且可访问
- 使用绝对路径

### 日志查看

所有服务都使用标准 Python logging，日志输出到控制台：

```bash
# 查看详细日志
uv run fs_mcp --log-level DEBUG
```

## 📝 许可证

本项目采用 MIT 许可证。详情请参阅 LICENSE 文件。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进项目。

## 📞 支持

如有问题或建议，请通过 GitHub Issues 联系。