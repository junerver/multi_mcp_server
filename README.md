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



### 在 Trae 中使用

`streamable-http` 传输协议

```json
{
  "mcpServers": {
    "ServerName": {
      "url": "http://localhost:3001/mcp",
      "headers": {
        "X-API-KEY": "application/json"
      }
    }
  }
}
```

`stdio` 传输协议

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
    }
  }
}
```



### 在其他场景使用时的注意事项

1. 跨域访问，当使用 `streamable-http` 传输协议连接远端服务时，会因为跨域访问导致连接拒绝，需要使用 CORS 中间件

2. `stdio` 不能再浏览器中启动服务器，如果你直接在浏览器的客户端使用 client，且配置的服务器为一个 npx、uvx 启动的 mcp 服务，将无法启动服务器，因为浏览器环境不允许执行，错误提示如下：

   ```bash
   Module "node:child_process" has been externalized for browser compatibility. Cannot access "node:child_process.spawn" in client code. See https://vite.dev/guide/troubleshooting.html#module-externalized-for-browser-compatibility for more details.
   ```

3. 

## 项目结构

### fs_mcp

文件服务模块，提供文件读写相关操作的mcp服务。

启动项目：

```bash
uv run fs_mcp
```

默认网络通信接口：3001

### element_plus_mcp

element-plus的mcp服务，提供element-plus的mcp服务，用户可以通过该服务查询 el+ 中组件的详细内容。

启动项目：

```bash
uv run element_plus_mcp
```

默认网络通信接口：3003



### mysql_mcp

与 mysql 数据库通信使用的 mcp 服务，提供如下工具：

- list_tables 列出全部表
- describe_table(table_name) 创建指定表的描述信息
- read_query(sql) 执行表查询

```bash
uv run mysql_mcp
```

默认网络通信接口：3004

### template_mcp

模板服务模块，提供模板相关操作的mcp服务。

启动项目：

```bash
uv run template_mcp
```

默认网络通信接口：3005