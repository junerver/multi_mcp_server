这是一个MCP服务测试项目，包含了文件服务、知识库服务等。



## 使用项目

项目使用 uv 包管理工具，需要先安装 uv：

windows安装：

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

同步项目：

```bash
uv sync
```

## 项目结构

### fs_mcp

文件服务模块，提供文件读写相关操作的mcp服务。

传输协议：`sse`

启动项目：

```bash
uv run fs_mcp
```

### element_plus_mcp

element-plus的mcp服务，提供element-plus的mcp服务，用户可以通过该服务查询 el+ 中组件的详细内容。

传输协议：`stdio` / `streamable-http`

启动项目：

```bash
# stdio 启动
uv run element_plus_mcp
# streamable-http 启动
uv run element_plus_mcp --transport=sse
```



