"""代码生成器工具函数

@author: Python版本实现
"""

from typing import List, Optional
from datetime import datetime
from mysql_mcp.gen.types import GenTable, GenTableColumn, VelocityContext


# 数据库字符串类型
_COLUMN_TYPE_STR = ["char", "varchar", "nvarchar", "varchar2"]

# 数据库文本类型
_COLUMN_TYPE_TEXT = ["tinytext", "text", "mediumtext", "longtext"]

# 数据库时间类型
_COLUMN_TYPE_TIME = ["datetime", "time", "date", "timestamp"]

# 数据库数字类型
_COLUMN_TYPE_NUMBER = ["tinyint", "smallint", "mediumint", "int", "number", "integer",
                     "bit", "bigint", "float", "double", "decimal"]

# 页面不需要编辑字段
_COLUMN_NAME_NOT_EDIT = ["id", "create_by", "create_time", "del_flag"]

# 页面不需要显示的列表字段
_COLUMN_NAME_NOT_LIST = ["id", "create_by", "create_time", "del_flag", "update_by", "update_time"]

# 页面不需要查询字段
_COLUMN_NAME_NOT_QUERY = ["id", "create_by", "create_time", "del_flag", "update_by", 
                        "update_time", "remark"]

# HTML控件类型
_HTML_INPUT = "input"
_HTML_TEXTAREA = "textarea"
_HTML_SELECT = "select"
_HTML_RADIO = "radio"
_HTML_CHECKBOX = "checkbox"
_HTML_DATETIME = "datetime"
_HTML_IMAGE_UPLOAD = "imageUpload"
_HTML_FILE_UPLOAD = "fileUpload"
_HTML_EDITOR = "editor"

# Java类型
_TYPE_STRING = "String"
_TYPE_INTEGER = "Integer"
_TYPE_LONG = "Long"
_TYPE_DOUBLE = "Double"
_TYPE_BIGDECIMAL = "BigDecimal"
_TYPE_DATE = "Date"

# 查询类型
_QUERY_LIKE = "LIKE"
_QUERY_EQ = "EQ"

# 需要标识
_REQUIRE = "1"


def _arrays_contains(arr: List[str], target_value: str) -> bool:
    """校验数组是否包含指定值
    
    Args:
        arr: 数组
        target_value: 值
        
    Returns:
        是否包含
    """
    return target_value in arr


def _get_db_type(column_type: str) -> str:
    """获取数据库类型字段
    
    Args:
        column_type: 列类型
        
    Returns:
        截取后的列类型
    """
    if "(" in column_type:
        return column_type.split("(")[0]
    return column_type


def _get_column_length(column_type: str) -> int:
    """获取字段长度
    
    Args:
        column_type: 列类型
        
    Returns:
        字段长度
    """
    if "(" in column_type and ")" in column_type:
        length_str = column_type.split("(")[1].split(")")[0]
        try:
            return int(length_str)
        except ValueError:
            return 0
    return 0


def _to_camel_case(snake_str: str) -> Optional[str]:
    """将下划线命名转换为驼峰命名
    
    Args:
        snake_str: 下划线命名字符串
        
    Returns:
        驼峰命名字符串
    """
    if snake_str is None:
        return None
    
    if '_' not in snake_str:
        return snake_str
    
    snake_str = snake_str.lower()
    components = snake_str.split('_')
    return components[0] + ''.join(word.capitalize() for word in components[1:])


def init_column_field(column: GenTableColumn, table: Optional[GenTable] = None) -> None:
    """初始化列属性字段
    
    Args:
        column: 列信息对象
        table: 表信息对象
    """
    data_type = _get_db_type(column.columnType) # 原始数据类型，移除长度
    column_name = column.columnName # 原始列名
    column.tableId = table.id if table and hasattr(table, 'id') else None
    
    # 设置java字段名
    column.javaField = _to_camel_case(column_name)
    
    # 设置默认类型
    column.javaType = _TYPE_STRING
    column.queryType = _QUERY_EQ
    
    # 根据数据类型设置字段属性
    if (_arrays_contains(_COLUMN_TYPE_STR, data_type) or 
        _arrays_contains(_COLUMN_TYPE_TEXT, data_type)):
        # 字符串类型
        column_length = _get_column_length(column.columnType)
        # 填充前端类型，字符串长度超过500设置为文本域
        html_type = (_HTML_TEXTAREA if column_length >= 500 or 
                    _arrays_contains(_COLUMN_TYPE_TEXT, data_type)
                    else _HTML_INPUT)
        column.htmlType = html_type
        
    elif _arrays_contains(_COLUMN_TYPE_TIME, data_type):
        # 时间类型
        column.javaType = _TYPE_DATE
        column.htmlType = _HTML_DATETIME
        
    elif _arrays_contains(_COLUMN_TYPE_NUMBER, data_type):
        # 数字类型
        column.htmlType = _HTML_INPUT
        
        # 解析数字类型的精度
        if "(" in column.columnType and ")" in column.columnType:
            precision_str = column.columnType.split("(")[1].split(")")[0]
            precision_parts = precision_str.split(",")
            
            # 如果是浮点型 统一用BigDecimal
            if len(precision_parts) == 2 and int(precision_parts[1]) > 0:
                column.javaType = _TYPE_BIGDECIMAL
            # 如果是整形
            elif len(precision_parts) == 1 and int(precision_parts[0]) <= 10:
                column.javaType = _TYPE_INTEGER
            # 长整形
            else:
                column.javaType = _TYPE_LONG
    
    # 插入字段（默认所有字段都需要插入）
    column.isInsert = _REQUIRE
    
    # 编辑字段
    if (not _arrays_contains(_COLUMN_NAME_NOT_EDIT, column_name) and 
        column.isPk != "1"):
        column.isEdit = _REQUIRE
        
    # 列表字段
    if (not _arrays_contains(_COLUMN_NAME_NOT_LIST, column_name) and 
        column.isPk != "1"):
        column.isList = _REQUIRE
        
    # 查询字段
    if (not _arrays_contains(_COLUMN_NAME_NOT_QUERY, column_name) and 
        column.isPk != "1"):
        column.isQuery = _REQUIRE
    
    # 查询字段类型
    if column_name.lower().endswith("name"):
        column.queryType = _QUERY_LIKE
        
    # 状态字段设置单选框
    if column_name.lower().endswith("status"):
        column.htmlType = _HTML_RADIO
        
    # 类型&性别字段设置下拉框
    elif (column_name.lower().endswith("type") or 
          column_name.lower().endswith("sex")):
        column.htmlType = _HTML_SELECT
        
    # 图片字段设置图片上传控件
    elif column_name.lower().endswith("image"):
        column.htmlType = _HTML_IMAGE_UPLOAD
        
    # 文件字段设置文件上传控件
    elif column_name.lower().endswith("file"):
        column.htmlType = _HTML_FILE_UPLOAD
        
    # 内容字段设置富文本控件
    elif column_name.lower().endswith("content"):
        column.htmlType = _HTML_EDITOR
        
        
def set_pk_column(columns: List[GenTableColumn], gen_table: GenTable) -> None:
    """设置主键列属性，填充列信息字段
    
    Args:
        columns: 列信息对象列表
        gen_table: 表信息对象
    """
    gen_table.columns = columns
    pk_columns = [column for column in columns if column.isPk == "1"]
    
    if pk_columns:
        # 如果有主键列，取第一个作为主键
        gen_table.pkColumn = pk_columns[0]
    else:
        # 如果没有主键列，设置默认主键
        gen_table.pkColumn = columns[0]


def _uncapitalize(string: Optional[str]) -> Optional[str]:
    """将字符串首字母转为小写
    
    Args:
        string: 输入字符串
        
    Returns:
        首字母小写的字符串
    """
    if not string:
        return string
    return string[0].lower() + string[1:] if len(string) > 1 else string.lower()


def _capitalize(string: Optional[str]) -> Optional[str]:
    """将字符串首字母转为大写
    
    Args:
        string: 输入字符串
        
    Returns:
        首字母大写的字符串
    """
    if not string:
        return string
    return string[0].upper() + string[1:] if len(string) > 1 else string.upper()


def _get_package_prefix(package_name: Optional[str]) -> Optional[str]:
    """获取包前缀
    
    Args:
        package_name: 包名
        
    Returns:
        包前缀
    """
    if not package_name:
        return None
    # 取最后一个点之前的部分作为基础包名
    parts = package_name.split('.')
    return '.'.join(parts[:-1]) if len(parts) > 1 else package_name


def _get_import_list(table: GenTable) -> List[str]:
    """获取导入列表
    
    Args:
        table: 表信息对象
        
    Returns:
        导入列表
    """
    import_list = []
    if not table.columns:
        return import_list
        
    # 检查是否需要导入Date类型
    has_date = any(column.javaType == _TYPE_DATE for column in table.columns)
    if has_date:
        import_list.append("java.util.Date")
        
    # 检查是否需要导入BigDecimal类型
    has_bigdecimal = any(column.javaType == _TYPE_BIGDECIMAL for column in table.columns)
    if has_bigdecimal:
        import_list.append("java.math.BigDecimal")
        
    return import_list


def _get_permission_prefix(module_name: Optional[str], business_name: Optional[str]) -> Optional[str]:
    """获取权限前缀
    
    Args:
        module_name: 模块名
        business_name: 业务名
        
    Returns:
        权限前缀
    """
    if not module_name or not business_name:
        return None
    return f"{module_name}:{business_name}"


def _set_datetime_query_flag(table: GenTable, context: VelocityContext) -> None:
    """设置日期时间查询标志
    
    Args:
        table: 表信息对象
        context: 模板上下文
    """
    if not table.columns:
        context.hasDatetimeQuery = False
        return
        
    # 检查是否有日期时间类型的查询字段
    has_datetime_query = any(
        column.isQuery == "1" and column.javaType == _TYPE_DATE 
        for column in table.columns
    )
    context.hasDatetimeQuery = has_datetime_query


def _get_dicts(table: GenTable) -> List[str]:
    """获取字典列表
    
    Args:
        table: 表信息对象
        
    Returns:
        字典列表
    """
    if not table.columns:
        return []
        
    # 收集所有非空的字典类型
    dicts = []
    for column in table.columns:
        if column.dictType and column.dictType.strip():
            if column.dictType not in dicts:
                dicts.append(column.dictType)
    return dicts


def _set_menu_velocity_context(context: VelocityContext, table: GenTable) -> None:
    """设置菜单相关上下文
    
    Args:
        context: 模板上下文
        table: 表信息对象
    """
    context.parentMenuId = table.parentMenuId
    context.parentMenuName = table.parentMenuName


def _set_tree_velocity_context(context: VelocityContext, table: GenTable) -> None:
    """设置树形表相关上下文
    
    Args:
        context: 模板上下文
        table: 表信息对象
    """
    context.treeCode = table.treeCode
    context.treeParentCode = table.treeParentCode
    context.treeName = table.treeName


def _set_sub_velocity_context(context: VelocityContext, table: GenTable) -> None:
    """设置主子表相关上下文
    
    Args:
        context: 模板上下文
        table: 表信息对象
    """
    # 这里可以根据实际需求设置子表相关信息
    # 暂时留空，等待具体需求
    pass
    

def prepare_context(table: GenTable) -> VelocityContext:
    """准备模板上下文
    
    Args:
        table: 表信息对象
        
    Returns:
        模板上下文
    """
    module_name = table.moduleName
    business_name = table.businessName
    package_name = table.packageName
    tpl_category = table.tplCategory
    function_name = table.functionName
    
    # 创建VelocityContext对象
    context = VelocityContext()
    
    # 设置基础字段
    context.tplCategory = table.tplCategory
    context.tableName = table.tableName
    context.functionName = function_name if function_name else "【请填写功能名称】"
    context.ClassName = table.className
    context.className = _uncapitalize(table.className) if table.className else None
    context.moduleName = table.moduleName
    context.BusinessName = _capitalize(table.businessName) if table.businessName else None
    context.businessName = table.businessName
    context.basePackage = _get_package_prefix(package_name) if package_name else None
    context.packageName = package_name
    context.author = table.functionAuthor
    context.datetime = datetime.now().strftime("%Y-%m-%d")
    context.pkColumn = table.pkColumn
    context.importList = _get_import_list(table)
    context.permissionPrefix = _get_permission_prefix(module_name, business_name)
    context.columns = table.columns or []
    
    # 设置日期时间查询标志
    _set_datetime_query_flag(table, context)
    
    # 设置表信息
    context.table = table
    
    # 设置字典信息
    context.dicts = _get_dicts(table)
    
    # 设置菜单相关信息
    _set_menu_velocity_context(context, table)
    
    # 如果是树形表，设置树形相关信息
    if tpl_category == "tree":
        _set_tree_velocity_context(context, table)
        
    # 如果是主子表，设置子表相关信息
    if tpl_category == "sub":
        _set_sub_velocity_context(context, table)
        
    return context
    