"""
知识库服务
提供基于向量搜索的知识检索功能
"""
import logging
import os
import sys
from typing import List, Dict, Optional, Any

import psycopg
import requests
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

from common.mcp_cli import with_mcp_options, run_mcp_server

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
mcp = FastMCP("KnowledgeServer", host="0.0.0.0", port=3002)

# 配置参数
CONFIG = {
    'ollama_url': os.getenv('OLLAMA_URL', 'http://localhost:11434'),                      # Ollama服务地址
    'model_name': os.getenv('EMBEDDING_MODEL', 'rjmalagon/gte-qwen2-1.5b-instruct-embed-f16'), # 使用的embedding模型名称
    'db_config': {                                               # 数据库连接配置
        'host': os.getenv('DB_HOST', 'localhost'),     # 数据库主机地址
        'port': int(os.getenv('DB_PORT', 5432)),           # 数据库端口
        'dbname': os.getenv('DB_NAME', 'postgres'),   # 数据库名称
        'user': os.getenv('DB_USER', 'postgres'),     # 数据库用户名
        'password': os.getenv('DB_PASSWORD', '1qaz2wsx')  # 数据库密码
    },
    'schema': os.getenv('DB_SCHEMA', 'code_gen'),           # 数据库模式名
    'table': os.getenv('DB_TABLE', 'open_ai_embeddings'),  # 存储向量的表名
    'top_k': int(os.getenv('TOP_K', 5)),                     # 返回最相似的前K个结果
    'similarity_threshold': float(os.getenv('SIMILARITY_THRESHOLD', 0.3))     # 相似度阈值
}


class VectorSearcher:
    """
    向量搜索器类
    
    负责连接数据库、向量化查询文本、执行相似度搜索等功能
    """
    
    def __init__(self, config: dict):
        """
        初始化向量搜索器
        
        Args:
            config: 配置字典，包含数据库连接信息和模型配置
        """
        self.config = config
        self.db_conn = None
        
    def connect_database(self) -> bool:
        """
        连接到PostgreSQL数据库
        
        Returns:
            bool: 连接是否成功
        """
        try:
            # 构建数据库连接字符串
            conn_str = (
                f"host={self.config['db_config']['host']} "
                f"port={self.config['db_config']['port']} "
                f"dbname={self.config['db_config']['dbname']} "
                f"user={self.config['db_config']['user']} "
                f"password={self.config['db_config']['password']}"
            )
            
            # 建立数据库连接
            self.db_conn = psycopg.connect(conn_str)
            logger.info("数据库连接成功")
            return True
            
        except Exception as e:
            logger.error(f"数据库连接失败: {e}")
            return False
    
    def get_embedding(self, text: str) -> Optional[List[float]]:
        """
        使用Ollama API获取文本的向量表示
        
        Args:
            text: 要向量化的文本内容
            
        Returns:
            List[float]: 文本的向量表示，失败时返回None
        """
        try:
            # 构建API请求
            url = f"{self.config['ollama_url']}/api/embeddings"
            payload = {
                "model": self.config['model_name'],
                "prompt": text
            }
            
            # 发送请求获取向量
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            # 解析响应获取向量数据
            result = response.json()
            embedding = result.get('embedding')
            
            # 检查向量维度是否正确 (根据模型调整)
            expected_dim = 1536  # 默认维度
            if embedding and len(embedding) == expected_dim:
                return embedding
            else:
                logger.warning(f"向量维度不正确: {len(embedding) if embedding else 0}, 期望: {expected_dim}")
                return None
                
        except Exception as e:
            logger.error(f"获取向量失败: {e}")
            return None
    
    def search_similar_vectors(self, query_embedding: List[float], top_k: int = None) -> List[Dict]:
        """
        在数据库中搜索相似向量
        
        Args:
            query_embedding: 查询向量
            top_k: 返回最相似的前K个结果，默认使用配置中的值
            
        Returns:
            List[Dict]: 搜索结果列表，每个结果包含内容、相似度、文件路径等信息
        """
        if top_k is None:
            top_k = self.config['top_k']
            
        try:
            cursor = self.db_conn.cursor()
            
            # 构建向量相似度搜索SQL
            # 使用余弦相似度进行搜索，返回最相似的结果
            search_sql = f"""
                SELECT 
                    id,
                    content,
                    chunk_type,
                    file_path,
                    chunk_index,
                    parent_id,
                    1 - (embedding <=> %s::vector) as similarity
                FROM {self.config['schema']}.{self.config['table']}
                WHERE 1 - (embedding <=> %s::vector) > %s
                ORDER BY embedding <=> %s::vector
                LIMIT %s
            """
            
            # 执行搜索查询
            logger.info(f"查询向量维度: {len(query_embedding)}")
            logger.info(f"相似度阈值: {self.config['similarity_threshold']}")
            
            cursor.execute(search_sql, (
                query_embedding, 
                query_embedding, 
                self.config['similarity_threshold'],
                query_embedding,
                top_k
            ))
            
            # 获取搜索结果
            results = cursor.fetchall()
            logger.info(f"找到 {len(results)} 个结果")
            
            # 格式化结果
            formatted_results = []
            for row in results:
                result = {
                    'id': row[0],
                    'content': row[1],
                    'chunk_type': row[2],
                    'file_path': row[3],
                    'chunk_index': row[4],
                    'parent_id': row[5],
                    'similarity': float(row[6])
                }
                formatted_results.append(result)
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"向量搜索失败: {e}")
            return []
    
    def get_parent_context(self, parent_id: str) -> Optional[str]:
        """
        获取父块的完整上下文内容
        
        Args:
            parent_id: 父块ID
            
        Returns:
            str: 父块内容，失败时返回None
        """
        try:
            cursor = self.db_conn.cursor()
            
            # 查询父块内容
            query_sql = f"""
                SELECT content 
                FROM {self.config['schema']}.{self.config['table']}
                WHERE id = %s AND chunk_type = 'parent'
            """
            
            cursor.execute(query_sql, (parent_id,))
            result = cursor.fetchone()
            
            return result[0] if result else None
            
        except Exception as e:
            logger.error(f"获取父块上下文失败: {e}")
            return None
    
    def format_search_results(self, results: List[Dict]) -> List[Dict]:
        """
        格式化搜索结果为结构化数据
        
        Args:
            results: 搜索结果列表
            
        Returns:
            List[Dict]: 格式化后的结果列表
        """
        if not results:
            return []
        
        formatted_results = []
        for result in results:
            # 获取父块上下文
            parent_content = None
            if result['chunk_type'] == 'child' and result['parent_id']:
                parent_content = self.get_parent_context(result['parent_id'])
            
            formatted_result = {
                'id': result['id'],
                'content': result['content'],
                'chunk_type': result['chunk_type'],
                'file_path': result['file_path'],
                'chunk_index': result['chunk_index'],
                'parent_id': result['parent_id'],
                'similarity': result['similarity'],
                'parent_content': parent_content
            }
            formatted_results.append(formatted_result)
        
        return formatted_results
    
    def close_connection(self):
        """
        关闭数据库连接
        """
        if self.db_conn:
            self.db_conn.close()
            logger.info("数据库连接已关闭")


class KnowledgeQueryRequest(BaseModel):
    query: str = Field(..., description="要搜索的知识查询内容")
    top_k: Optional[int] = Field(None, description="返回最相似的前K个结果")


@mcp.tool()
def search_knowledge(request: KnowledgeQueryRequest) -> Dict[str, Any]:
    """
    根据输入内容查找向量数据库，返回知识库中的文本
    该工具用于桥接LLM与知识库，提供基于向量相似度的知识检索功能
    """
    # 创建向量搜索器实例
    searcher = VectorSearcher(CONFIG)
    
    try:
        # 连接数据库
        if not searcher.connect_database():
            return {
                "content": [{
                    "type": "text",
                    "text": "数据库连接失败"
                }]
            }
        
        # 将查询文本向量化
        query_embedding = searcher.get_embedding(request.query)
        if query_embedding is None:
            return {
                "content": [{
                    "type": "text",
                    "text": "查询向量化失败"
                }]
            }
        
        # 执行向量搜索
        results = searcher.search_similar_vectors(query_embedding, request.top_k)
        
        # 格式化搜索结果
        formatted_results = searcher.format_search_results(results)
        
        # 返回结构化结果
        return {
            "content": [{
                "type": "object",
                "data": {
                    "query": request.query,
                    "results": formatted_results
                }
            }]
        }
        
    except Exception as e:
        logger.error(f"知识搜索过程中发生错误: {e}")
        return {
            "content": [{
                "type": "text",
                "text": f"知识搜索失败: {e}"
            }]
        }
    finally:
        # 确保关闭数据库连接
        searcher.close_connection()

@with_mcp_options(3002)
def main(transport: str, port: int):
    """主函数，启动MCP服务器"""
    run_mcp_server(mcp, transport, port= port)

if __name__ == "__main__":
    main()