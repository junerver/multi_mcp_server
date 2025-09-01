# 模板 MCP 服务器

这是一个基于 MCP (Model Context Protocol) 的模板服务器，用于管理和提供代码生成模板文件。

## 功能特性

- 📋 **Prompt 支持**: 提供结构化的模板信息列表
- 🔧 **工具支持**: 根据模板名称获取模板文件内容
- 📁 **分类管理**: 按后端代码、前端代码、数据库脚本分类
- 🛡️ **错误处理**: 完善的错误处理和日志记录

## 支持的模板

### 后端代码模板
- **domain**: Domain实体类模板 (`java/domain.java.vm`)
- **sub_domain**: 子表Domain实体类模板 (`java/sub-domain.java.vm`)
- **mapper**: Mapper接口模板 (`java/mapper.java.vm`)
- **service**: Service接口模板 (`java/service.java.vm`)
- **serviceImpl**: Service实现类模板 (`java/serviceImpl.java.vm`)
- **controller**: Controller控制器模板 (`java/controller.java.vm`)
- **mapper_xml**: MyBatis XML映射文件模板 (`xml/mapper.xml.vm`)

### 前端代码模板
- **api**: API接口文件模板 (`js/api.js.vm`)
- **vue_index**: Vue页面组件模板 (`vue/index.vue.vm`)
- **vue_form**: Vue表单组件模板 (`vue/v3/Form.vue.vm`)
- **vue_tree**: Vue树形页面组件模板 (`vue/index-tree.vue.vm`)
- **vue_v3_index**: Vue3页面组件模板 (`vue/v3/index.vue.vm`)
- **vue_v3_tree**: Vue3树形页面组件模板 (`vue/v3/index-tree.vue.vm`)

### 数据库脚本模板
- **sql**: 菜单SQL脚本模板 (`sql/sql.vm`)

## 可用的 Prompts

### `list_templates`
列出所有可用的代码生成模板信息，包括：
- 模板名称和描述
- 按类别分组显示
- 使用说明

## 可用的工具

### `get_template_content`
根据模板名称获取模板文件内容。

**参数**:
- `template_name` (string): 模板文件名称

**返回**: 包含模板文件内容的格式化文本，包括模板信息和完整的模板代码。

### `get_sample_content`
获取模板文件的示例内容。

**参数**:
- `template_name` (string): 模板文件名称

**返回**: 包含模板文件示例内容的格式化文本，包括模板信息和示例代码。


### `list_template_categories`
列出所有模板类别及其包含的模板。

**返回**: 按类别组织的模板列表。

## 启动服务器

### 使用 stdio 传输 (默认)
```bash
uv run template_mcp
```

### 使用 HTTP 传输
```bash
uv run template_mcp --transport streamable --port 3005
```

### 使用 SSE 传输
```bash
uv run template_mcp --transport sse --port 3005
```

## 使用示例

### 1. 获取所有模板列表
使用 `list_templates` prompt 来查看所有可用的模板。

### 2. 获取特定模板内容
使用 `get_template_content` 工具，传入模板名称：

```json
{
  "template_name": "domain"
}
```

这将返回 Domain 实体类模板的完整内容。

### 3. 查看模板分类
使用 `list_template_categories` 工具来查看按类别组织的模板列表。

## 模板文件结构

```
template/
├── java/
│   ├── controller.java.vm
│   ├── domain.java.vm
│   ├── mapper.java.vm
│   ├── service.java.vm
│   ├── serviceImpl.java.vm
│   └── sub-domain.java.vm
├── js/
│   └── api.js.vm
├── sql/
│   └── sql.vm
├── vue/
│   ├── index-tree.vue.vm
│   ├── index.vue.vm
│   └── v3/
│       ├── Form.vue.vm
│       ├── index-tree.vue.vm
│       └── index.vue.vm
└── xml/
    └── mapper.xml.vm
```

## 示例文件结构

示例文件存储在 `src/template_mcp/sample/` 目录下，按照以下结构组织：

```
sample/
├── java/           # Java 示例文件
│   ├── controller.java
│   ├── domain.java
│   ├── mapper.java
│   ├── service.java
│   └── serviceImpl.java
├── js/             # JavaScript 示例文件
│   └── api.js
├── sql/            # SQL 示例文件
│   └── sql
├── vue/            # Vue 示例文件
│   └── v3/
│       ├── Form.vue
│       └── index.vue
└── xml/            # XML 示例文件
    └── mapper.xml
```

## 错误处理

服务器提供完善的错误处理：
- 无效的模板名称会返回可用模板列表
- 文件不存在会返回详细的错误信息
- 所有错误都会记录到日志中

## 依赖项

- `mcp`: MCP 协议支持
- `click`: 命令行界面
- `pydantic`: 数据验证
- `starlette`: CORS 中间件支持

## 日志

服务器使用标准的 Python logging 模块，日志级别为 INFO，包含时间戳和详细的操作信息。