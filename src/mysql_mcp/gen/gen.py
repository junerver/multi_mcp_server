import mysql.connector
from mysql_mcp.gen.config import GEN_CONFIG
from mysql_mcp.types import MysqlDatabaseConfig
from mysql_mcp.gen.types import GenTable, GenTableColumn
from typing import Optional


def select_table_by_name(cursor: mysql.connector.cursor.MySQLCursor, table_name: str) -> Optional[GenTable]:
    """
    根据表名查询数据库表信息，返回GenTable对象

    Args:
        cursor: MySQL数据库游标
        table_name: 要查询的表名

    Returns:
        GenTable对象，如果表不存在则返回None
    """
    try:
        # 执行查询SQL，参考提供的SQL逻辑
        query = """
        SELECT table_name, table_comment, create_time, update_time 
        FROM information_schema.tables 
        WHERE table_name NOT LIKE 'qrtz_%' 
        AND table_name NOT LIKE 'gen_%' 
        AND table_schema = (SELECT DATABASE()) 
        AND table_name = %s
        """

        cursor.execute(query, (table_name,))
        result = cursor.fetchone()

        if result:
            # 将查询结果转换为GenTable对象
            # 由于SQL只返回基本信息，其他字段使用默认值
            gen_table = GenTable(
                tableName=result["table_name"],
                tableComment=result["table_comment"] or "",
                className=_convert_class_name(result["table_name"]),  #
                tplCategory="crud",
                tplWebType="element-plus",  #
                packageName=GEN_CONFIG["packageName"],  #
                moduleName=_get_module_name(GEN_CONFIG["packageName"]),  #
                businessName=_get_business_name(result["table_name"]),  #
                functionName=_replace_text(result["table_comment"]),  #
                functionAuthor=GEN_CONFIG["author"],  #
                genType="0",
                genPath="",
                pkColumn=None,  # 需要额外查询获取
                columns=[],  # 需要额外查询获取
                options="",
                treeCode="",
                treeParentCode="",
                treeName="",
                parentMenuId="",
                parentMenuName="",
            )
            return gen_table
        else:
            return None

    except mysql.connector.Error as e:
        print(f"数据库查询错误: {e}")
        return None
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()


def select_table_columns_by_name(cursor: mysql.connector.cursor.MySQLCursor, table_name: str) -> list[GenTableColumn]:
    """
    根据表名查询数据库表列信息，返回GenTableColumn列表

    Args:
        cursor: MySQL数据库游标
        table_name: 要查询的表名

    Returns:
        表列信息列表，如果表不存在则返回空列表
    """
    try:
        # 执行查询SQL，参考提供的SQL逻辑
        query = """
        SELECT column_name,
               (CASE WHEN (is_nullable = 'no' AND column_key != 'PRI') THEN '1' ELSE '0' END) as is_required,
               (CASE WHEN column_key = 'PRI' THEN '1' ELSE '0' END) as is_pk,
               ordinal_position as sort,
               column_comment,
               (CASE WHEN extra = 'auto_increment' THEN '1' ELSE '0' END) as is_increment,
               column_type
        FROM information_schema.columns
        WHERE table_schema = (SELECT DATABASE())
          AND table_name = %s
        ORDER BY ordinal_position
        """

        cursor.execute(query, (table_name,))
        results = cursor.fetchall()

        columns = []
        for row in results:
            # 将查询结果转换为GenTableColumn对象
            column = GenTableColumn(
                tableId=0,  # 这里设为0，实际使用时可能需要传入真实的tableId
                columnName=row["column_name"],
                columnComment=row["column_comment"] or "",
                columnType=row["column_type"],
                javaType=_convert_column_type_to_java(row["column_type"]),
                javaField=_convert_to_camel_case_field(row["column_name"]),
                isPk=row["is_pk"],
                isIncrement=row["is_increment"],
                isRequired=row["is_required"],
                isInsert="1",  # 默认为插入字段
                isEdit="1" if row["is_pk"] == "0" else "0",  # 主键不可编辑
                isList="1",  # 默认为列表字段
                isQuery="1" if row["is_pk"] == "1" else "0",  # 主键默认为查询字段
                queryType="EQ",  # 默认查询方式为等于
                htmlType=_convert_column_type_to_html_type(row["column_type"]),
                dictType="",  # 默认无字典类型
                sort=row["sort"],
            )
            columns.append(column)

        return columns

    except mysql.connector.Error as e:
        print(f"数据库查询错误: {e}")
        return []
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()


def _convert_class_name(table_name: str) -> str:
    """
    将表名转换为类名

    Args:
        table_name: 数据库表名

    Returns:
        转换后的类名（驼峰命名）
    """
    from mysql_mcp.gen.config import GEN_CONFIG

    # 获取配置
    auto_remove_pre = GEN_CONFIG.get("autoRemovePre", False)
    table_prefix = GEN_CONFIG.get("tablePrefix", "")

    # 如果启用自动移除前缀且前缀不为空
    if auto_remove_pre and table_prefix:
        # 支持多个前缀，用逗号分隔
        prefixes = [prefix.strip() for prefix in table_prefix.split(",") if prefix.strip()]
        for prefix in prefixes:
            if table_name.startswith(prefix):
                table_name = table_name[len(prefix) :]
                break

    # 转换为驼峰命名
    return _convert_to_camel_case(table_name)


def _convert_to_camel_case(snake_str: str) -> str:
    """
    将下划线命名转换为驼峰命名

    Args:
        snake_str: 下划线命名的字符串

    Returns:
        驼峰命名的字符串
    """
    if not snake_str:
        return snake_str

    # 分割字符串并转换为驼峰命名
    components = snake_str.split("_")
    # 第一个单词首字母大写，其余单词首字母大写
    return "".join(word.capitalize() for word in components if word)


def _get_module_name(package_name: str) -> str:
    """
    将包名转换为模块名

    Args:
        package_name: 包名

    Returns:
        模块名
    """
    # 获取最后一个点号的位置
    last_index = package_name.rfind(".")
    # 如果没有点号，直接返回原字符串
    if last_index == -1:
        return package_name
    # 返回最后一个点号后面的子字符串
    return package_name[last_index + 1 :]


def _get_business_name(table_name: str) -> str:
    """
    将表名转换为业务名

    Args:
        table_name: 表名

    Returns:
        业务名
    """
    # 获取最后一个下划线的位置
    last_index = table_name.rfind("_")
    # 获取字符串长度
    name_length = len(table_name)
    # 截取最后一个下划线后的字符串作为业务名
    return table_name[last_index + 1 : name_length] if last_index != -1 else table_name


def _replace_text(table_comment: str) -> str:
    """
    替换文本中的特殊字符

    Args:
        table_comment: 表注释

    Returns:
        替换后的文本
    """
    import re

    if not table_comment:
        return ""
    # 替换文本中的 "表" 和 "若依" 字符
    return re.sub(r"[表若依]", "", table_comment)


def _convert_column_type_to_java(column_type: str) -> str:
    """
    将MySQL数据类型转换为Java数据类型

    Args:
        column_type: MySQL数据类型

    Returns:
        对应的Java数据类型
    """
    column_type = column_type.lower()

    if "bigint" in column_type:
        return "Long"
    elif any(t in column_type for t in ["int", "tinyint", "smallint", "mediumint"]):
        return "Integer"
    elif any(t in column_type for t in ["float", "double", "decimal", "numeric"]):
        return "BigDecimal"
    elif any(t in column_type for t in ["char", "varchar", "text", "longtext", "mediumtext", "tinytext"]):
        return "String"
    elif any(t in column_type for t in ["date", "time", "datetime", "timestamp"]):
        return "Date"
    elif "bit" in column_type:
        return "Boolean"
    else:
        return "String"


def _convert_to_camel_case_field(snake_str: str) -> str:
    """
    将下划线命名转换为小驼峰命名（字段名）

    Args:
        snake_str: 下划线命名的字符串

    Returns:
        小驼峰命名的字符串
    """
    if not snake_str:
        return snake_str

    # 分割字符串并转换为小驼峰命名
    components = snake_str.split("_")
    # 第一个单词保持小写，其余单词首字母大写
    return components[0].lower() + "".join(word.capitalize() for word in components[1:] if word)


def _convert_column_type_to_html_type(column_type: str) -> str:
    """
    将MySQL数据类型转换为HTML表单控件类型

    Args:
        column_type: MySQL数据类型

    Returns:
        对应的HTML表单控件类型
    """
    column_type = column_type.lower()
    
    if any(t in column_type for t in ['text', 'longtext', 'mediumtext']):
        return 'textarea'
    elif any(t in column_type for t in ['date', 'datetime', 'timestamp']):
        return 'datetime'
    elif 'time' in column_type:
        return 'datetime'
    else:
        return 'input'
