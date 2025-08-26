from typing import List, Optional

from pydantic import BaseModel, Field


# Pydantic模型定义
class FileInfo(BaseModel):
    """文件信息结构"""
    name: str = Field(description="文件名")
    size: int = Field(description="文件大小（字节）")
    type: str = Field(description="文件类型/扩展名")

class ComponentMetadata(BaseModel):
    """组件元数据信息结构"""
    name: str = Field(description="组件名称")
    description: str = Field(description="组件描述")
    files: List[FileInfo] = Field(description="组件包含的文件列表")
    dependencies: List[str] = Field(description="组件依赖项列表")

class SourceFile(BaseModel):
    """源码文件结构"""
    filename: str = Field(description="文件名")
    language: str = Field(description="编程语言类型")
    content: str = Field(description="文件内容")

class ComponentSource(BaseModel):
    """组件源码信息结构"""
    component_name: str = Field(description="组件名称")
    source_files: List[SourceFile] = Field(description="源码文件列表")
    found: bool = Field(description="是否找到组件")
    error_message: Optional[str] = Field(description="错误信息（如果有）")

class DemoFile(BaseModel):
    """演示文件结构"""
    filename: str = Field(description="演示文件名")
    content: str = Field(description="演示代码内容")

class ComponentDemo(BaseModel):
    """组件演示代码信息结构"""
    component_name: str = Field(description="组件名称")
    demo_files: List[DemoFile] = Field(description="演示文件列表")
    found: bool = Field(description="是否找到演示代码")
    error_message: Optional[str] = Field(description="错误信息（如果有）")

class ComponentList(BaseModel):
    """组件列表信息结构"""
    components: List[str] = Field(description="组件名称列表")
    total_count: int = Field(description="组件总数")
    found: bool = Field(description="是否成功获取组件列表")
    error_message: Optional[str] = Field(description="错误信息（如果有）")

class DirectoryItem(BaseModel):
    """目录项结构"""
    name: str = Field(description="项目名称")
    type: str = Field(description="类型：dir（目录）或file（文件）")
    size: Optional[int] = Field(description="文件大小（字节），目录为None")

class DirectoryStructure(BaseModel):
    """目录结构信息"""
    path: str = Field(description="目录路径")
    owner: str = Field(description="仓库所有者")
    repo: str = Field(description="仓库名称")
    branch: str = Field(description="分支名称")
    items: List[DirectoryItem] = Field(description="目录项列表")
    directory_count: int = Field(description="目录数量")
    file_count: int = Field(description="文件数量")
    found: bool = Field(description="是否成功获取目录结构")
    error_message: Optional[str] = Field(description="错误信息（如果有）")
