#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文档向量化脚本

功能说明：
1. 遍历docs目录中的文档文件（支持.md, .txt, .py, .java, .js, .vue, .sql, .xml格式）
2. 将文档内容按指定大小分块处理，支持重叠分块以保持上下文连续性
3. 使用Ollama的embedding模型对文本块进行向量化
4. 将文本内容和对应的向量存储到PostgreSQL数据库的pgvector扩展表中
5. 支持重复检测，避免重复处理相同内容
6. 提供详细的日志记录和错误处理

依赖要求：
- PostgreSQL数据库（需安装pgvector扩展）
- Ollama服务（需要下载对应的embedding模型）
- Python依赖：psycopg[binary], requests

作者：AI Assistant
创建时间：2025-08-15
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

# 配置日志系统
# 同时输出到文件和控制台，便于调试和监控处理进度
logging.basicConfig(
    level=logging.INFO,  # 设置日志级别为INFO
    format='%(asctime)s - %(levelname)s - %(message)s',  # 日志格式：时间-级别-消息
    handlers=[
        logging.FileHandler('embedding.log'),  # 输出到文件
        logging.StreamHandler(sys.stdout)      # 输出到控制台
    ]
)
logger = logging.getLogger(__name__)

# 全局配置参数
# 可根据实际环境和需求调整这些参数
CONFIG = {
    'docs_dir': 'docs',                                          # 文档目录路径
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
    'chunk_size': 1000,             # 文档分块大小（字符数）
    'overlap': 200                  # 分块重叠大小（字符数），保持上下文连续性
}

class DocumentEmbedder:
    """
    文档向量化处理器
    
    主要功能：
    1. 管理数据库连接
    2. 调用Ollama API进行文本向量化
    3. 处理文档分块和向量存储
    4. 提供完整的文档处理流程
    
    设计特点：
    - 面向对象设计，便于扩展和维护
    - 完善的错误处理和日志记录
    - 支持大文档的分块处理
    - 自动去重，避免重复处理
    """
    
    def __init__(self, config: dict):
        """初始化文档向量化处理器
        
        Args:
            config: 配置参数字典
        """
        self.config = config
        self.db_conn = None
        
    def connect_database(self) -> bool:
        """
        连接PostgreSQL数据库
        
        使用psycopg库连接数据库，设置autocommit=True自动提交事务。
        这样可以避免手动管理事务，简化代码逻辑。
        
        Returns:
            bool: 连接是否成功
        """
        try:
            # 使用配置参数连接数据库，启用自动提交模式
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
        """
        使用Ollama API获取文本向量
        
        通过HTTP POST请求调用Ollama的embeddings API，将文本转换为向量表示。
        向量维度取决于所使用的模型，需要与数据库表结构匹配。
        
        Args:
            text: 待向量化的文本内容
            
        Returns:
            List[float]: 向量结果（浮点数列表），失败时返回None
        """
        try:
            # 构建Ollama API请求
            url = f"{self.config['ollama_url']}/api/embeddings"
            payload = {
                "model": self.config['model_name'],  # 指定使用的embedding模型
                "prompt": text                       # 待向量化的文本
            }
            
            # 发送POST请求，设置30秒超时
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()  # 检查HTTP状态码，如果不是2xx会抛出异常
            
            # 解析响应JSON
            result = response.json()
            embedding = result.get('embedding')
            
            # 检查向量维度是否符合预期
            # 注意：不同模型的向量维度不同，需要根据实际模型调整
            if embedding and len(embedding) == 1536:
                return embedding
            else:
                logger.warning(f"向量维度不正确: {len(embedding) if embedding else 0}")
                return None
                
        except Exception as e:
            logger.error(f"获取向量失败: {e}")
            return None
    
    def chunk_text(self, text: str) -> List[str]:
        """
        将长文本分块处理
        
        为了避免单次处理过长的文本导致向量化失败或效果不佳，
        将文档按指定大小分割成多个块。同时保持块之间的重叠，
        以保持上下文的连续性。
        
        分块策略：
        1. 如果文本长度小于等于chunk_size，直接返回
        2. 否则按chunk_size分割，但尽量在单词边界分割
        3. 相邻块之间保持overlap大小的重叠
        
        Args:
            text: 原始文本内容
            
        Returns:
            List[str]: 分块后的文本列表
        """
        # 如果文本长度不超过分块大小，直接返回
        if len(text) <= self.config['chunk_size']:
            return [text]
        
        chunks = []
        start = 0
        
        # 循环分割文本
        while start < len(text):
            # 计算当前块的结束位置
            end = start + self.config['chunk_size']
            
            # 如果不是最后一块，尝试在合适的位置分割（避免截断单词）
            if end < len(text):
                # 向后查找合适的分割点（空格、换行符、标点符号等）
                # 搜索范围：从end位置向前最多100个字符
                for i in range(end, max(start + self.config['chunk_size'] - 100, start), -1):
                    if text[i] in [' ', '\n', '\t', '.', '!', '?']:
                        end = i + 1  # 包含分隔符
                        break
            
            # 提取当前块并去除首尾空白
            chunk = text[start:end].strip()
            if chunk:  # 只添加非空块
                chunks.append(chunk)
            
            # 计算下一块的起始位置，考虑重叠
            # 重叠可以保持上下文连续性，提高向量化效果
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
        """
        保存文本内容和对应向量到数据库
        
        执行流程：
        1. 根据文本内容生成唯一ID（MD5哈希）
        2. 检查数据库中是否已存在相同内容，避免重复处理
        3. 如果不存在，则插入新记录到pgvector表中
        
        Args:
            content: 文本内容
            embedding: 对应的向量数据（浮点数列表）
            
        Returns:
            bool: 保存是否成功
        """
        try:
            cursor = self.db_conn.cursor()
            
            # 根据内容生成唯一ID，用于去重
            doc_id = self.generate_id(content)
            
            # 检查数据库中是否已存在相同内容
            cursor.execute(
                f"SELECT id FROM {self.config['schema']}.{self.config['table']} WHERE id = %s",
                (doc_id,)
            )
            
            # 如果已存在，跳过处理
            if cursor.fetchone():
                logger.info(f"文档已存在，跳过: {doc_id[:8]}...")
                return True
            
            # 插入新记录到数据库
            # 注意：embedding字段类型为VECTOR，psycopg会自动处理类型转换
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
        """
        处理单个文档文件
        
        完整的文件处理流程：
        1. 读取文件内容
        2. 将内容分块处理
        3. 对每个块进行向量化
        4. 将文本块和向量保存到数据库
        
        Args:
            file_path: 文档文件路径
            
        Returns:
            bool: 处理是否成功（至少有一个块成功处理）
        """
        logger.info(f"处理文件: {file_path}")
        
        # 第一步：读取文件内容
        content = self.read_file_content(file_path)
        if not content:
            return False
        
        # 第二步：将内容分块处理
        chunks = self.chunk_text(content)
        logger.info(f"文件分为 {len(chunks)} 个块")
        
        # 第三步：逐个处理每个文本块
        success_count = 0
        for i, chunk in enumerate(chunks):
            logger.info(f"处理块 {i+1}/{len(chunks)}")
            
            # 获取文本块的向量表示
            embedding = self.get_embedding(chunk)
            if not embedding:
                logger.error(f"块 {i+1} 向量化失败")
                continue
            
            # 将文本块和向量保存到数据库
            if self.save_embedding(chunk, embedding):
                success_count += 1
            
        logger.info(f"文件处理完成: {success_count}/{len(chunks)} 块成功")
        # 只要有一个块成功处理，就认为文件处理成功
        return success_count > 0
    
    def scan_documents(self) -> List[Path]:
        """
        扫描文档目录，查找所有支持的文档文件
        
        使用递归方式遍历整个文档目录树，查找所有支持格式的文件。
        支持多种常见的文档和代码文件格式。
        
        Returns:
            List[Path]: 找到的文档文件路径列表
        """
        docs_path = Path(self.config['docs_dir'])
        if not docs_path.exists():
            logger.error(f"文档目录不存在: {docs_path}")
            return []
        
        # 定义支持的文件扩展名
        # 包括文档格式和常见的代码文件格式
        supported_extensions = {
            '.md',    # Markdown文档
            '.txt',   # 纯文本文件
            '.py',    # Python代码
            '.java',  # Java代码
            '.js',    # JavaScript代码
            '.vue',   # Vue组件
            '.sql',   # SQL脚本
            '.xml'    # XML文件
        }
        
        files = []
        # 使用rglob递归遍历所有子目录
        for file_path in docs_path.rglob('*'):
            # 检查是否为文件且扩展名在支持列表中
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                files.append(file_path)
        
        logger.info(f"找到 {len(files)} 个文档文件")
        return files
    
    def run(self) -> bool:
        """
        运行完整的文档向量化处理流程
        
        主要步骤：
        1. 连接数据库
        2. 扫描文档目录
        3. 逐个处理文档文件
        4. 统计处理结果
        5. 清理资源
        
        Returns:
            bool: 整体处理是否成功（至少有一个文件成功处理）
        """
        logger.info("开始文档向量化处理")
        
        # 第一步：建立数据库连接
        if not self.connect_database():
            return False
        
        try:
            # 第二步：扫描文档目录，获取所有待处理文件
            files = self.scan_documents()
            if not files:
                logger.warning("没有找到可处理的文档")
                return False
            
            # 第三步：逐个处理文档文件
            success_count = 0
            for file_path in files:
                if self.process_file(file_path):
                    success_count += 1
            
            # 第四步：输出处理结果统计
            logger.info(f"处理完成: {success_count}/{len(files)} 个文件成功")
            return success_count > 0
            
        finally:
            # 第五步：确保数据库连接被正确关闭
            self.close_database()

def main():
    """
    主函数 - 程序入口点
    
    功能：
    1. 设置工作目录为脚本所在目录
    2. 创建文档向量化处理器实例
    3. 执行向量化处理流程
    4. 处理各种异常情况
    5. 返回适当的退出码
    """
    try:
        # 切换到脚本所在目录，确保相对路径正确
        script_dir = Path(__file__).parent
        os.chdir(script_dir)
        
        # 创建文档向量化处理器实例并运行
        embedder = DocumentEmbedder(CONFIG)
        success = embedder.run()
        
        # 根据处理结果设置退出码
        if success:
            logger.info("文档向量化处理成功完成")
            sys.exit(0)  # 成功退出
        else:
            logger.error("文档向量化处理失败")
            sys.exit(1)  # 失败退出
            
    except KeyboardInterrupt:
        # 处理用户中断（Ctrl+C）
        logger.info("用户中断处理")
        sys.exit(1)
    except Exception as e:
        # 处理其他未预期的异常
        logger.error(f"程序异常: {e}")
        sys.exit(1)

# 程序入口点
# 当脚本被直接执行时（而不是被导入时）运行main函数
if __name__ == '__main__':
    main()