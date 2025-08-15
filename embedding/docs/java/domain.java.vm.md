# Java实体类模板 (domain.java.vm)

## 模板功能说明

这个模板用于生成Java实体类（Entity/Domain对象），是数据库表对应的Java对象模型。生成的实体类包含完整的字段定义、注解配置和基础方法。

## 主要特性

### 1. 基础结构
- **包声明**: 使用`${packageName}.domain`作为包路径
- **继承关系**: 继承`BaseEntity`基类，获得通用字段和方法
- **序列化**: 实现`Serializable`接口，支持对象序列化

### 2. 注解支持
- **Lombok注解**: 
  - `@Data`: 自动生成getter/setter、toString、equals、hashCode方法
  - `@EqualsAndHashCode(callSuper = true)`: 继承父类的equals和hashCode逻辑
- **MyBatis Plus注解**:
  - `@TableName("${tableName}")`: 指定对应的数据库表名
- **Excel导出注解**:
  - `@Excel`: 支持字段导出到Excel，包含名称、宽度、日期格式等配置
- **JSON格式化**:
  - `@JsonFormat`: 日期字段的JSON序列化格式控制

### 3. 字段生成逻辑
- **条件渲染**: 使用`#if($column.list)`判断字段是否在列表中显示
- **注释处理**: 自动提取字段注释，去除括号内容作为Excel列名
- **类型适配**: 根据Java类型自动选择合适的注解配置
- **日期处理**: 日期类型字段自动添加格式化注解

### 4. 主子表支持
- **主键集合**: 生成`ids`字段用于批量操作的主键收集
- **子表关联**: 当存在子表时，自动生成`${subclassName}List`集合字段

## 模板变量说明

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `${packageName}` | 包名 | `com.jkr.project.system` |
| `${importList}` | 导入列表 | 自动生成的import语句 |
| `${functionName}` | 功能名称 | `用户信息` |
| `${tableName}` | 数据库表名 | `sys_user` |
| `${author}` | 作者 | `jkr` |
| `${datetime}` | 生成时间 | `2024-01-01` |
| `${ClassName}` | 类名（首字母大写） | `SysUser` |
| `${className}` | 类名（首字母小写） | `sysUser` |
| `${columns}` | 字段列表 | 表的所有字段信息 |
| `${subClassName}` | 子表类名 | `SysUserRole` |
| `${subclassName}` | 子表类名（首字母小写） | `sysUserRole` |

## 生成示例

```java
package com.jkr.project.system.domain;

import java.util.Date;
import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;
import com.baomidou.mybatisplus.annotation.TableName;
import com.jkr.framework.aspectj.lang.annotation.Excel;
import com.fasterxml.jackson.annotation.JsonFormat;
import com.jkr.framework.web.domain.BaseEntity;

/**
 * 用户信息对象 sys_user
 *
 * @author jkr
 * @date 2024-01-01
 */
@Data
@EqualsAndHashCode(callSuper = true)
@TableName("sys_user")
public class SysUser extends BaseEntity {
    private static final long serialVersionUID = 1L;

    /** 用户ID */
    private Long userId;

    /** 用户账号 */
    @Excel(name = "用户账号")
    private String userName;

    /** 用户昵称 */
    @Excel(name = "用户昵称")
    private String nickName;

    /** 创建时间 */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    @Excel(name = "创建时间", width = 30, dateFormat = "yyyy-MM-dd HH:mm:ss")
    private Date createTime;

    /** 主键集合 */
    private List<Long> ids;
}
```

## 原始模板内容

```velocity
package ${packageName}.domain;

#foreach ($import in $importList)
import ${import};
#end
import lombok.Data;
import lombok.EqualsAndHashCode;
import com.baomidou.mybatisplus.annotation.TableName;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.jkr.framework.aspectj.lang.annotation.Excel;
import com.jkr.framework.web.domain.BaseEntity;

/**
 * ${functionName}对象 ${tableName}
 *
 * @author ${author}
 * @date ${datetime}
 */
@Data
@EqualsAndHashCode(callSuper = true)
@TableName("${tableName}")
public class ${ClassName} extends BaseEntity {
    private static final long serialVersionUID = 1L;

#foreach ($column in $columns)
#if(!$table.isSuperColumn($column.javaField))
    /** $column.columnComment */
#if($column.list)
#set($parentheseIndex=$column.columnComment.indexOf("（"))
#if($parentheseIndex != -1)
#set($comment=$column.columnComment.substring(0, $parentheseIndex))
#else
#set($comment=$column.columnComment)
#end
#if($parentheseIndex != -1)
    @Excel(name = "${comment}", readConverterExp = "$column.readConverterExp()")
#elseif($column.javaType == 'Date')
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    @Excel(name = "${comment}", width = 30, dateFormat = "yyyy-MM-dd HH:mm:ss")
#else
    @Excel(name = "${comment}")
#end
#end
    private $column.javaType $column.javaField;

#end
#end
    /** 主键集合 */
    private List<Long> ids;
#if($table.sub)

    /** ${subTable.functionName}信息 */
    private List<${subClassName}> ${subclassName}List;
#end
}
```

## 使用说明

1. **字段映射**: 模板会自动将数据库字段映射为Java字段，遵循驼峰命名规范
2. **注解配置**: 根据字段类型和属性自动添加相应的注解
3. **Excel支持**: 标记为列表显示的字段会自动添加Excel导出注解
4. **主子表**: 支持一对多关系的主子表结构生成
5. **扩展性**: 可通过修改模板来调整生成的代码结构和注解配置