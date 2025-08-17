# 文档向量化脚本

这个脚本用于遍历 `docs` 目录中的文档，使用本地 ollama 的 `nomic-embed-text:v1.5` 模型进行向量化，并将结果存储到 pgvector 数据库中。

## 功能特性

- 自动扫描 `docs` 目录下的所有支持格式文档
- 支持文档分块处理，避免超长文本问题
- 使用 MD5 哈希避免重复处理相同内容
- 完整的日志记录和错误处理
- 支持多种文档格式：`.md`, `.txt`, `.py`, `.java`, `.js`, `.vue`, `.sql`, `.xml`

## 环境要求

### 1. Python 依赖
```bash
# 使用 uv 安装依赖（推荐）
uv sync

# 或使用 pip 安装
pip install psycopg>=3.1.0 requests>=2.31.0
```

### 2. Ollama 服务
确保本地 ollama 服务正在运行，并已安装 `nomic-embed-text:v1.5` 模型：
```bash
# 安装模型
ollama pull nomic-embed-text:v1.5

# 启动服务（如果未运行）
ollama serve
```

### 3. PostgreSQL 数据库
确保 PostgreSQL 数据库正在运行，并已安装 pgvector 扩展：
```sql
-- 创建扩展
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 创建 schema
CREATE SCHEMA IF NOT EXISTS code_gen;

-- 创建父子分块表，首先删除已存在的表
DROP TABLE IF EXISTS code_gen.open_ai_embeddings;
CREATE TABLE IF NOT EXISTS code_gen.open_ai_embeddings (
    id VARCHAR(191) PRIMARY KEY DEFAULT uuid_generate_v4(),
    parent_id VARCHAR(191),  -- 父块ID，如果是父块则为NULL
    content TEXT NOT NULL,
    embedding vector(1536) NOT NULL,
    chunk_type VARCHAR(20) NOT NULL DEFAULT 'child',  -- 'parent' 或 'child'
    file_path TEXT,  -- 源文件路径
    chunk_index INTEGER,  -- 在文件中的块索引
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- 添加外键约束
    FOREIGN KEY (parent_id) REFERENCES code_gen.open_ai_embeddings(id) ON DELETE CASCADE
);

-- 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_parent_id ON code_gen.open_ai_embeddings(parent_id);
CREATE INDEX IF NOT EXISTS idx_chunk_type ON code_gen.open_ai_embeddings(chunk_type);
CREATE INDEX IF NOT EXISTS idx_file_path ON code_gen.open_ai_embeddings(file_path);
```

## 配置说明

脚本中的配置参数可以根据需要修改：

```python
CONFIG = {
    'docs_dir': 'docs',                    # 文档目录
    'ollama_url': 'http://localhost:11434', # Ollama 服务地址
    'model_name': 'nomic-embed-text:v1.5',  # 向量化模型
    'db_config': {                         # 数据库配置
        'host': 'localhost',
        'port': 5432,
        'database': 'postgres',
        'user': 'postgres',
        'password': '1qaz2wsx'
    },
    'schema': 'code_gen',                  # 数据库 schema
    'table': 'open_ai_embeddings',         # 数据表名
    'parent_chunk_size': 2000,             # 父块大小（较大的语义单元）
    'child_chunk_size': 500,               # 子块大小（较小的检索单元）
    'overlap': 100                         # 分块重叠大小
}
```

## 使用方法

1. 确保所有依赖服务正在运行
2. 将需要向量化的文档放入 `docs` 目录
3. 运行脚本：

```bash
uv run embed
```

## 日志输出

脚本会同时输出到控制台和 `embedding.log` 文件，包含：
- 文件处理进度
- 向量化状态
- 数据库操作结果
- 错误信息和警告

## 注意事项

1. 首次运行前请确保数据库表结构已正确创建
2. 脚本会自动跳过已处理的内容（基于 MD5 哈希）
3. 如果 ollama 服务未启动或模型未安装，脚本会报错退出
4. 建议在处理大量文档前先测试少量文件