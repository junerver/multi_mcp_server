#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文档向量化脚本
遍历docs目录中的文档，使用ollama的nomic-embed-text模型进行向量化，
并将结果存储到pgvector数据库中。
"""

import os
import sys
import hashlib
import logging
from pathlib import Path
from typing import List, Tuple, Optional

import psycopg
import requests
import json

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('embedding.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# 配置参数
CONFIG = {
    'docs_dir': 'docs',
    'ollama_url': 'http://localhost:11434',
    'model_name': 'rjmalagon/gte-qwen2-1.5b-instruct-embed-f16',
    'db_config': {
        'host': 'localhost',
        'port': 5432,
        'dbname': 'postgres',
        'user': 'postgres',
        'password': '1qaz2wsx'
    },
    'schema': 'code_gen',
    'table': 'open_ai_embeddings',
    'chunk_size': 1000,  # 文档分块大小
    'overlap': 200       # 分块重叠大小
}

class DocumentEmbedder:
    """文档向量化处理器"""
    
    def __init__(self, config: dict):
        """初始化文档向量化处理器
        
        Args:
            config: 配置参数字典
        """
        self.config = config
        self.db_conn = None
        
    def connect_database(self) -> bool:
        """连接数据库
        
        Returns:
            bool: 连接是否成功
        """
        try:
            self.db_conn = psycopg.connect(**self.config['db_config'], autocommit=True)
            logger.info("数据库连接成功")
            return True
        except Exception as e:
            logger.error(f"数据库连接失败: {e}")
            return False
    
    def close_database(self):
        """关闭数据库连接"""
        if self.db_conn:
            self.db_conn.close()
            logger.info("数据库连接已关闭")
    
    def get_embedding(self, text: str) -> Optional[List[float]]:
        """使用ollama获取文本向量
        
        Args:
            text: 待向量化的文本
            
        Returns:
            List[float]: 向量结果，失败时返回None
        """
        try:
            url = f"{self.config['ollama_url']}/api/embeddings"
            payload = {
                "model": self.config['model_name'],
                "prompt": text
            }
            
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            embedding = result.get('embedding')
            # 检查向量维度
            if embedding and len(embedding) == 1536:
                return embedding
            else:
                logger.warning(f"向量维度不正确: {len(embedding) if embedding else 0}")
                return None
                
        except Exception as e:
            logger.error(f"获取向量失败: {e}")
            return None
    
    def chunk_text(self, text: str) -> List[str]:
        """将文本分块处理
        
        Args:
            text: 原始文本
            
        Returns:
            List[str]: 分块后的文本列表
        """
        if len(text) <= self.config['chunk_size']:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.config['chunk_size']
            
            # 如果不是最后一块，尝试在单词边界分割
            if end < len(text):
                # 向后查找空格或换行符
                for i in range(end, max(start + self.config['chunk_size'] - 100, start), -1):
                    if text[i] in [' ', '\n', '\t', '.', '!', '?']:
                        end = i + 1
                        break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # 设置下一块的起始位置，考虑重叠
            start = max(start + 1, end - self.config['overlap'])
            
        return chunks
    
    def generate_id(self, content: str) -> str:
        """生成内容的唯一ID
        
        Args:
            content: 文本内容
            
        Returns:
            str: 生成的唯一ID
        """
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def save_embedding(self, content: str, embedding: List[float]) -> bool:
        """保存向量到数据库
        
        Args:
            content: 文本内容
            embedding: 向量数据
            
        Returns:
            bool: 保存是否成功
        """
        try:
            cursor = self.db_conn.cursor()
            
            # 生成唯一ID
            doc_id = self.generate_id(content)
            
            # 检查是否已存在
            cursor.execute(
                f"SELECT id FROM {self.config['schema']}.{self.config['table']} WHERE id = %s",
                (doc_id,)
            )
            
            if cursor.fetchone():
                logger.info(f"文档已存在，跳过: {doc_id[:8]}...")
                return True
            
            # 插入新记录
            insert_sql = f"""
                INSERT INTO {self.config['schema']}.{self.config['table']} 
                (id, content, embedding) 
                VALUES (%s, %s, %s)
            """
            
            cursor.execute(insert_sql, (doc_id, content, embedding))
            logger.info(f"向量保存成功: {doc_id[:8]}...")
            return True
            
        except Exception as e:
            logger.error(f"保存向量失败: {e}")
            return False
    
    def read_file_content(self, file_path: Path) -> Optional[str]:
        """读取文件内容
        
        Args:
            file_path: 文件路径
            
        Returns:
            str: 文件内容，失败时返回None
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    return content
                else:
                    logger.warning(f"文件为空: {file_path}")
                    return None
        except Exception as e:
            logger.error(f"读取文件失败 {file_path}: {e}")
            return None
    
    def process_file(self, file_path: Path) -> bool:
        """处理单个文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 处理是否成功
        """
        logger.info(f"处理文件: {file_path}")
        
        # 读取文件内容
        content = self.read_file_content(file_path)
        if not content:
            return False
        
        # 分块处理
        chunks = self.chunk_text(content)
        logger.info(f"文件分为 {len(chunks)} 个块")
        
        success_count = 0
        for i, chunk in enumerate(chunks):
            logger.info(f"处理块 {i+1}/{len(chunks)}")
            
            # 获取向量
            embedding = self.get_embedding(chunk)
            if not embedding:
                logger.error(f"块 {i+1} 向量化失败")
                continue
            
            # 保存到数据库
            if self.save_embedding(chunk, embedding):
                success_count += 1
            
        logger.info(f"文件处理完成: {success_count}/{len(chunks)} 块成功")
        return success_count > 0
    
    def scan_documents(self) -> List[Path]:
        """扫描文档目录
        
        Returns:
            List[Path]: 文档文件路径列表
        """
        docs_path = Path(self.config['docs_dir'])
        if not docs_path.exists():
            logger.error(f"文档目录不存在: {docs_path}")
            return []
        
        # 支持的文件扩展名
        supported_extensions = {'.md', '.txt', '.py', '.java', '.js', '.vue', '.sql', '.xml'}
        
        files = []
        for file_path in docs_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                files.append(file_path)
        
        logger.info(f"找到 {len(files)} 个文档文件")
        return files
    
    def run(self) -> bool:
        """运行文档向量化处理
        
        Returns:
            bool: 处理是否成功
        """
        logger.info("开始文档向量化处理")
        
        # 连接数据库
        if not self.connect_database():
            return False
        
        try:
            # 扫描文档
            files = self.scan_documents()
            if not files:
                logger.warning("没有找到可处理的文档")
                return False
            
            # 处理每个文件
            success_count = 0
            for file_path in files:
                if self.process_file(file_path):
                    success_count += 1
            
            logger.info(f"处理完成: {success_count}/{len(files)} 个文件成功")
            return success_count > 0
            
        finally:
            self.close_database()

def main():
    """主函数"""
    try:
        # 切换到脚本所在目录
        script_dir = Path(__file__).parent
        os.chdir(script_dir)
        
        # 创建处理器并运行
        embedder = DocumentEmbedder(CONFIG)
        success = embedder.run()
        
        if success:
            logger.info("文档向量化处理成功完成")
            sys.exit(0)
        else:
            logger.error("文档向量化处理失败")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("用户中断处理")
        sys.exit(1)
    except Exception as e:
        logger.error(f"程序异常: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()