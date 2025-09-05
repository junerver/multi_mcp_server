from pydantic import BaseModel, Field
from typing import Optional, List, Literal, Dict, Any
from datetime import datetime


class GenTable(BaseModel):
    """代码生成表配置模型"""
    
    tableName: Optional[str] = Field(default=None, description="表名")
    tableComment: Optional[str] = Field(default=None, description="表注释")
    className: Optional[str] = Field(default=None, description="类名")
    tplCategory: Optional[Literal["crud", "tree", "sub"]] = Field(default=None, description="使用的模板（crud单表操作 tree树表操作 sub主子表操作）")
    tplWebType: Optional[Literal["element-ui", "element-plus"]] = Field(default=None, description="前端类型（element-ui模版 element-plus模版）")
    packageName: Optional[str] = Field(default=None, description="生成包路径")
    moduleName: Optional[str] = Field(default=None, description="生成模块名")
    businessName: Optional[str] = Field(default=None, description="生成业务名")
    functionName: Optional[str] = Field(default=None, description="生成功能名")
    functionAuthor: Optional[str] = Field(default=None, description="生成作者")
    genType: Optional[str] = Field(default=None, description="生成代码方式（0zip压缩包 1自定义路径）")
    genPath: Optional[str] = Field(default=None, description="生成路径（不填默认项目路径）")
    pkColumn: Optional["GenTableColumn"] = Field(default=None, description="主键信息")
    columns: Optional[List["GenTableColumn"]] = Field(default_factory=list, description="表列信息")
    options: Optional[str] = Field(default=None, description="其它生成选项")
    treeCode: Optional[str] = Field(default=None, description="树编码字段")
    treeParentCode: Optional[str] = Field(default=None, description="树父编码字段")
    treeName: Optional[str] = Field(default=None, description="树名称字段")
    parentMenuId: Optional[str] = Field(default=None, description="上级菜单ID字段")
    parentMenuName: Optional[str] = Field(default=None, description="上级菜单名称字段")

class GenTableColumn(BaseModel):
    """代码生成表列配置模型"""
    
    tableId: Optional[int] = Field(default=None, description="归属表编号")
    columnName: Optional[str] = Field(default=None, description="列名称")
    columnComment: Optional[str] = Field(default=None, description="列描述")
    columnType: Optional[str] = Field(default=None, description="列类型")
    javaType: Optional[str] = Field(default=None, description="JAVA类型")
    javaField: Optional[str] = Field(default=None, description="JAVA字段名")
    isPk: Optional[str] = Field(default=None, description="是否主键（1是）")
    isIncrement: Optional[str] = Field(default=None, description="是否自增（1是）")
    isRequired: Optional[str] = Field(default=None, description="是否必填（1是）")
    isInsert: Optional[str] = Field(default=None, description="是否为插入字段（1是）")
    isEdit: Optional[str] = Field(default=None, description="是否编辑字段（1是）")
    isList: Optional[str] = Field(default=None, description="是否列表字段（1是）")
    isQuery: Optional[str] = Field(default=None, description="是否查询字段（1是）")
    queryType: Optional[str] = Field(default=None, description="查询方式（EQ等于、NE不等于、GT大于、LT小于、LIKE模糊、BETWEEN范围）")
    htmlType: Optional[str] = Field(default=None, description="显示类型（input文本框、textarea文本域、select下拉框、checkbox复选框、radio单选框、datetime日期控件、image图片上传控件、upload文件上传控件、editor富文本控件）")
    dictType: Optional[str] = Field(default="", description="字典类型")
    sort: Optional[int] = Field(default=None, description="排序")


class VelocityContext(BaseModel):
    """Velocity模板上下文模型"""
    
    tplCategory: Optional[str] = Field(default=None, description="模板类型")
    tableName: Optional[str] = Field(default=None, description="表名")
    functionName: Optional[str] = Field(default=None, description="功能名称")
    ClassName: Optional[str] = Field(default=None, description="类名（首字母大写）")
    className: Optional[str] = Field(default=None, description="类名（首字母小写）")
    moduleName: Optional[str] = Field(default=None, description="模块名")
    BusinessName: Optional[str] = Field(default=None, description="业务名（首字母大写）")
    businessName: Optional[str] = Field(default=None, description="业务名")
    basePackage: Optional[str] = Field(default=None, description="基础包名")
    packageName: Optional[str] = Field(default=None, description="包名")
    author: Optional[str] = Field(default=None, description="作者")
    datetime: Optional[str] = Field(default=None, description="生成时间")
    pkColumn: Optional[GenTableColumn] = Field(default=None, description="主键列信息")
    importList: Optional[List[str]] = Field(default_factory=list, description="导入列表")
    permissionPrefix: Optional[str] = Field(default=None, description="权限前缀")
    columns: Optional[List[GenTableColumn]] = Field(default_factory=list, description="列信息")
    table: Optional[GenTable] = Field(default=None, description="表信息")
    dicts: Optional[List[str]] = Field(default_factory=list, description="字典列表")
    # 树形表相关字段
    treeCode: Optional[str] = Field(default=None, description="树编码字段")
    treeParentCode: Optional[str] = Field(default=None, description="树父编码字段")
    treeName: Optional[str] = Field(default=None, description="树名称字段")
    # 菜单相关字段
    parentMenuId: Optional[str] = Field(default=None, description="上级菜单ID")
    parentMenuName: Optional[str] = Field(default=None, description="上级菜单名称")
    # 子表相关字段
    subTable: Optional[GenTable] = Field(default=None, description="子表信息")
    subTableName: Optional[str] = Field(default=None, description="子表名")
    subTableFkName: Optional[str] = Field(default=None, description="子表外键名")
    subClassName: Optional[str] = Field(default=None, description="子表类名")
    subTableFkClassName: Optional[str] = Field(default=None, description="子表外键类名")
    # 其他扩展字段
    hasDatetimeQuery: Optional[bool] = Field(default=False, description="是否有日期时间查询")
    extra: Optional[Dict[str, Any]] = Field(default_factory=dict, description="额外字段")
