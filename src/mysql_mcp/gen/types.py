from dataclasses import dataclass

@dataclass
class GenTable:
    # 表名
    tableName: str
    # 表注释
    tableComment: str
    # 类名
    className: str
    # 使用的模板（crud单表操作 tree树表操作 sub主子表操作）
    tplCategory: str
    # 前端类型（element-ui模版 element-plus模版）
    tplWebType: str
    # 生成包路径
    packageName: str
    # 生成模块名
    moduleName: str
    # 生成业务名
    businessName: str
    # 生成功能名
    functionName: str
    # 生成作者
    functionAuthor: str
    # 生成代码方式（0zip压缩包 1自定义路径）
    genType: str
    # 生成路径（不填默认项目路径）
    genPath: str
    # 主键信息
    pkColumn: "GenTableColumn"
    # 表列信息
    columns: list["GenTableColumn"]
    # 其它生成选项
    options: str
    # 树编码字段
    treeCode: str
    # 树父编码字段
    treeParentCode: str
    # 树名称字段
    treeName: str
    # 上级菜单ID字段
    parentMenuId: str
    # 上级菜单名称字段
    parentMenuName: str

@dataclass
class GenTableColumn:
    # 归属表编号
    tableId: int
    # 列名称
    columnName: str
    # 列描述
    columnComment: str
    # 列类型
    columnType: str
    # JAVA类型
    javaType: str
    # JAVA字段名
    javaField: str
    # 是否主键（1是）
    isPk: str
    # 是否自增（1是）
    isIncrement: str
    # 是否必填（1是）
    isRequired: str
    # 是否为插入字段（1是）
    isInsert: str
    # 是否编辑字段（1是）
    isEdit: str
    # 是否列表字段（1是）
    isList: str
    # 是否查询字段（1是）
    isQuery: str
    # 查询方式（EQ等于、NE不等于、GT大于、LT小于、LIKE模糊、BETWEEN范围）
    queryType: str
    # 显示类型（input文本框、textarea文本域、select下拉框、checkbox复选框、radio单选框、datetime日期控件、image图片上传控件、upload文件上传控件、editor富文本控件）
    htmlType: str
    # 字典类型
    dictType: str
    # 排序
    sort: int
