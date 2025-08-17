# 子表实体类模板 (sub-domain.java.vm)

## 模板功能说明

这个模板用于生成子表实体类（Sub Domain对象），专门用于主子表关系中的子表数据模型。生成的子表实体类包含完整的字段定义、Excel导出注解和标准的getter/setter方法，支持与主表的关联操作。

## 主要特性

### 1. 基础结构
- **包声明**: 使用`${packageName}.domain`作为包路径
- **继承关系**: 继承`BaseEntity`基类，获得通用字段和方法
- **序列化**: 实现`Serializable`接口，支持对象序列化
- **命名规范**: 以`${subClassName}`命名，与主表实体区分

### 2. 注解支持
- **Excel导出注解**: 
  - `@Excel`: 支持字段导出到Excel，包含名称、宽度、日期格式等配置
  - **条件渲染**: 只有标记为列表显示的字段才添加Excel注解
- **JSON格式化**:
  - `@JsonFormat`: 日期字段的JSON序列化格式控制
- **数据转换**:
  - `readConverterExp`: 支持数据字典值的转换显示

### 3. 字段生成逻辑
- **排除超类字段**: 使用`$table.isSuperColumn()`排除BaseEntity中的字段
- **条件渲染**: 根据`$column.list`判断字段是否在列表中显示
- **注释处理**: 自动提取字段注释，去除括号内容作为Excel列名
- **类型适配**: 根据Java类型自动选择合适的注解配置

### 4. 方法生成
- **Getter/Setter**: 为每个字段生成标准的访问器方法
- **toString方法**: 使用Apache Commons Lang的ToStringBuilder生成
- **字段命名**: 支持特殊的字段命名规则（如首字母大写的字段）

## 模板变量说明

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `${packageName}` | 包名 | `com.jkr.project.system` |
| `${subImportList}` | 子表导入列表 | 自动生成的import语句 |
| `${subTable.functionName}` | 子表功能名称 | `用户角色` |
| `${subTableName}` | 子表数据库表名 | `sys_user_role` |
| `${author}` | 作者 | `jkr` |
| `${datetime}` | 生成时间 | `2024-01-01` |
| `${subClassName}` | 子表类名（首字母大写） | `SysUserRole` |
| `${subTable.columns}` | 子表字段列表 | 子表的所有字段信息 |

## 字段处理逻辑

### 1. 字段过滤
```velocity
#if(!$table.isSuperColumn($column.javaField))
    // 只处理非超类字段
#end
```
- **排除字段**: 排除BaseEntity中已定义的字段（如createTime、updateTime等）
- **保留字段**: 只生成子表特有的业务字段

### 2. Excel注解生成
```velocity
#if($column.list)
    #set($parentheseIndex=$column.columnComment.indexOf("（"))
    #if($parentheseIndex != -1)
        #set($comment=$column.columnComment.substring(0, $parentheseIndex))
    #else
        #set($comment=$column.columnComment)
    #end
    // 根据字段类型和注释生成相应的Excel注解
#end
```
- **条件生成**: 只有列表显示字段才生成Excel注解
- **注释处理**: 提取括号前的注释作为Excel列名
- **类型判断**: 根据字段类型选择合适的注解配置

### 3. 方法名生成
```velocity
#if($column.javaField.length() > 2 && $column.javaField.substring(1,2).matches("[A-Z]"))
    #set($AttrName=$column.javaField)
#else
    #set($AttrName=$column.javaField.substring(0,1).toUpperCase() + ${column.javaField.substring(1)})
#end
```
- **特殊命名**: 处理首字母大写的特殊字段命名
- **标准命名**: 普通字段按驼峰命名规则生成方法名

## 生成示例

```java
package com.jkr.project.system.domain;

import java.util.Date;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.jkr.framework.aspectj.lang.annotation.Excel;
import com.jkr.framework.web.domain.BaseEntity;

/**
 * 用户角色对象 sys_user_role
 *
 * @author jkr
 * @date 2024-01-01
 */
public class SysUserRole extends BaseEntity {
    private static final long serialVersionUID = 1L;

    /** 用户ID */
    @Excel(name = "用户ID")
    private Long userId;

    /** 角色ID */
    @Excel(name = "角色ID")
    private Long roleId;

    /** 状态 */
    @Excel(name = "状态", readConverterExp = "0=正常,1=停用")
    private String status;

    /** 创建时间 */
    @JsonFormat(pattern = "yyyy-MM-dd")
    @Excel(name = "创建时间", width = 30, dateFormat = "yyyy-MM-dd")
    private Date createTime;

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    public Long getUserId() {
        return userId;
    }

    public void setRoleId(Long roleId) {
        this.roleId = roleId;
    }

    public Long getRoleId() {
        return roleId;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getStatus() {
        return status;
    }

    public void setCreateTime(Date createTime) {
        this.createTime = createTime;
    }

    public Date getCreateTime() {
        return createTime;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this, ToStringStyle.MULTI_LINE_STYLE)
            .append("userId", getUserId())
            .append("roleId", getRoleId())
            .append("status", getStatus())
            .append("createTime", getCreateTime())
            .toString();
    }
}
```

## 原始模板内容

```velocity
package ${packageName}.domain;

#foreach ($import in $subImportList)
import ${import};
#end
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.jkr.framework.aspectj.lang.annotation.Excel;
import com.jkr.framework.web.domain.BaseEntity;

/**
 * ${subTable.functionName}对象 ${subTableName}
 *
 * @author ${author}
 * @date ${datetime}
 */
public class ${subClassName} extends BaseEntity {
    private static final long serialVersionUID = 1L;

#foreach ($column in $subTable.columns)
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
    @JsonFormat(pattern = "yyyy-MM-dd")
    @Excel(name = "${comment}", width = 30, dateFormat = "yyyy-MM-dd")
#else
    @Excel(name = "${comment}")
#end
#end
    private $column.javaType $column.javaField;

#end
#end
#foreach ($column in $subTable.columns)
#if(!$table.isSuperColumn($column.javaField))
#if($column.javaField.length() > 2 && $column.javaField.substring(1,2).matches("[A-Z]"))
#set($AttrName=$column.javaField)
#else
#set($AttrName=$column.javaField.substring(0,1).toUpperCase() + ${column.javaField.substring(1)})
#end
    public void set${AttrName}($column.javaType $column.javaField) {
        this.$column.javaField = $column.javaField;
    }

    public $column.javaType get${AttrName}() {
        return $column.javaField;
    }
#end
#end

    @Override
    public String toString() {
        return new ToStringBuilder(this, ToStringStyle.MULTI_LINE_STYLE)
#foreach ($column in $subTable.columns)
#if($column.javaField.length() > 2 && $column.javaField.substring(1,2).matches("[A-Z]"))
#set($AttrName=$column.javaField)
#else
#set($AttrName=$column.javaField.substring(0,1).toUpperCase() + ${column.javaField.substring(1)})
#end
            .append("${column.javaField}", get${AttrName}())
#end
            .toString();
    }
}
```

## 使用场景

### 1. 主子表关系
- **一对多关系**: 主表包含多个子表记录
- **关联操作**: 主表操作时同步处理子表数据
- **数据完整性**: 保证主子表数据的一致性

### 2. 业务场景示例
- **订单明细**: 订单（主表） - 订单明细（子表）
- **用户角色**: 用户（主表） - 用户角色（子表）
- **部门员工**: 部门（主表） - 员工（子表）
- **商品规格**: 商品（主表） - 商品规格（子表）

## 设计特点

### 1. 轻量级设计
- **简单结构**: 不使用Lombok，保持代码可读性
- **标准方法**: 生成标准的getter/setter方法
- **清晰继承**: 继承BaseEntity获得基础功能

### 2. Excel集成
- **导出支持**: 内置Excel导出注解配置
- **数据转换**: 支持字典数据的转换显示
- **格式控制**: 支持日期、数字等格式控制

### 3. 扩展性
- **注解扩展**: 可添加更多业务注解
- **方法扩展**: 可添加业务特定方法
- **验证支持**: 可添加数据验证注解

## 使用说明

### 1. 关联配置
- **外键字段**: 子表必须包含指向主表的外键字段
- **关联注解**: 可使用JPA注解标识关联关系
- **级联操作**: 在主表实体中配置级联操作

### 2. 数据操作
- **批量插入**: 支持批量插入子表数据
- **级联删除**: 删除主表时同步删除子表数据
- **数据同步**: 更新主表时同步更新子表数据

### 3. 查询优化
- **懒加载**: 配置懒加载避免N+1查询问题
- **连接查询**: 使用JOIN查询优化性能
- **分页处理**: 合理处理主子表的分页查询

## 最佳实践

### 1. 字段设计
- **必要字段**: 只包含业务必需的字段
- **外键约束**: 正确设置外键字段和约束
- **索引优化**: 为常用查询字段添加索引

### 2. 性能优化
- **批量操作**: 使用批量插入、更新提高性能
- **缓存策略**: 对热点数据进行缓存
- **查询优化**: 避免不必要的关联查询

### 3. 数据一致性
- **事务控制**: 确保主子表操作在同一事务中
- **约束检查**: 添加必要的数据约束
- **异常处理**: 处理主子表操作的异常情况

### 4. 代码维护
- **命名规范**: 遵循统一的命名规范
- **注释完整**: 提供完整的字段和方法注释
- **版本控制**: 谨慎处理字段的增删改操作