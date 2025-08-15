#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
向量搜索测试脚本

功能说明：
1. 连接到PostgreSQL数据库的向量表
2. 监听控制台输入，接收用户查询
3. 将查询文本向量化
4. 在数据库中执行向量相似度搜索
5. 返回最相关的搜索结果

使用方法：
运行脚本后，在控制台输入查询文本，按回车执行搜索
输入 'quit' 或 'exit' 退出程序

作者：AI Assistant
创建时间：2025-08-15
"""

import os
import sys
import logging
from typing import List, Dict, Optional, Tuple

import psycopg
import requests
import json

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# 配置参数
CONFIG = {
    'ollama_url': 'http://localhost:11434',                      # Ollama服务地址
    'model_name': 'rjmalagon/gte-qwen2-1.5b-instruct-embed-f16', # 使用的embedding模型名称
    'db_config': {                                               # 数据库连接配置
        'host': 'localhost',     # 数据库主机地址
        'port': 5432,           # 数据库端口
        'dbname': 'postgres',   # 数据库名称
        'user': 'postgres',     # 数据库用户名
        'password': '1qaz2wsx'  # 数据库密码
    },
    'schema': 'code_gen',           # 数据库模式名
    'table': 'open_ai_embeddings',  # 存储向量的表名
    'top_k': 5,                     # 返回最相似的前K个结果
    'similarity_threshold': 0.3     # 相似度阈值（降低以获得更多结果）
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
            
            # 检查向量维度是否正确
            if embedding and len(embedding) == 1536:
                return embedding
            else:
                logger.warning(f"向量维度不正确: {len(embedding) if embedding else 0}")
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
    
    def format_search_results(self, results: List[Dict]) -> str:
        """
        格式化搜索结果为可读的字符串
        
        Args:
            results: 搜索结果列表
            
        Returns:
            str: 格式化后的结果字符串
        """
        if not results:
            return "未找到相关结果"
        
        formatted_output = []
        formatted_output.append(f"\n找到 {len(results)} 个相关结果:\n")
        formatted_output.append("=" * 80)
        
        for i, result in enumerate(results, 1):
            formatted_output.append(f"\n结果 {i}:")
            formatted_output.append(f"相似度: {result['similarity']:.4f}")
            formatted_output.append(f"文件路径: {result['file_path']}")
            formatted_output.append(f"块类型: {result['chunk_type']}")
            
            # 如果是子块且有父块ID，尝试获取父块上下文
            if result['chunk_type'] == 'child' and result['parent_id']:
                parent_content = self.get_parent_context(result['parent_id'])
                if parent_content:
                    formatted_output.append(f"\n父块上下文 (前200字符):")
                    formatted_output.append(parent_content[:200] + "..." if len(parent_content) > 200 else parent_content)
            
            formatted_output.append(f"\n匹配内容:")
            # 限制显示内容长度
            content = result['content']
            if len(content) > 300:
                content = content[:300] + "..."
            formatted_output.append(content)
            formatted_output.append("-" * 80)
        
        return "\n".join(formatted_output)
    
    def interactive_search(self):
        """
        交互式搜索模式
        
        持续监听用户输入，执行向量搜索并显示结果
        """
        print("\n=== 向量搜索测试工具 ===")
        print("输入查询文本进行向量搜索")
        print("输入 'quit' 或 'exit' 退出程序")
        print("=" * 50)
        
        while True:
            try:
                # 获取用户输入
                query = input("\n请输入查询内容: ").strip()
                
                # 检查退出命令
                if query.lower() in ['quit', 'exit', '退出']:
                    print("程序退出")
                    break
                
                # 检查输入是否为空
                if not query:
                    print("请输入有效的查询内容")
                    continue
                
                print(f"\n正在搜索: {query}")
                
                # 将查询文本向量化
                query_embedding = self.get_embedding(query)
                if query_embedding is None:
                    print("查询向量化失败，请重试")
                    continue
                
                # 执行向量搜索
                results = self.search_similar_vectors(query_embedding)
                
                # 显示搜索结果
                formatted_results = self.format_search_results(results)
                print(formatted_results)
                
            except KeyboardInterrupt:
                print("\n\n程序被用户中断")
                break
            except Exception as e:
                logger.error(f"搜索过程中发生错误: {e}")
                print(f"搜索失败: {e}")
    
    def close_connection(self):
        """
        关闭数据库连接
        """
        if self.db_conn:
            self.db_conn.close()
            logger.info("数据库连接已关闭")

def main():
    """
    主函数
    
    初始化向量搜索器并启动交互式搜索模式
    """
    # 创建向量搜索器实例
    searcher = VectorSearcher(CONFIG)
    
    try:
        # 连接数据库
        if not searcher.connect_database():
            print("数据库连接失败，程序退出")
            return
        
        # 启动交互式搜索
        searcher.interactive_search()
        
    except Exception as e:
        logger.error(f"程序运行失败: {e}")
    finally:
        # 确保关闭数据库连接
        searcher.close_connection()

if __name__ == "__main__":
    main()