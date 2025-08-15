# MyBatis数据访问层模板 (mapper.java.vm)

## 模板功能说明

这个模板用于生成MyBatis数据访问层接口（Mapper），提供完整的数据库操作方法。生成的Mapper接口继承MyBatis Plus的BaseMapper，同时扩展了自定义的业务方法，支持标准CRUD操作、批量操作和逻辑删除。

## 主要特性

### 1. 基础结构
- **包声明**: 使用`${packageName}.mapper`作为包路径
- **继承关系**: 继承`BaseMapper<${ClassName}>`，获得基础的CRUD方法
- **注解标识**: 使用`@Mapper`注解标识为MyBatis映射器
- **泛型支持**: 通过泛型指定操作的实体类型

### 2. 核心功能

#### 查询操作
- **单条查询**: 根据主键查询单条记录
- **列表查询**: 根据条件查询记录列表
- **条件查询**: 支持复杂的条件查询

#### 数据操作
- **插入操作**: 新增单条记录
- **更新操作**: 修改现有记录
- **删除操作**: 物理删除和逻辑删除
- **批量操作**: 批量删除、批量插入

### 3. 逻辑删除支持
- **逻辑删除**: `logicRemoveByIds()` - 批量逻辑删除
- **单条逻辑删除**: `logicRemoveBy${pkColumn.capJavaField}()` - 单条逻辑删除
- **物理删除**: 保留物理删除方法（注释状态）

### 4. 主子表支持
当存在子表关系时，自动生成子表相关操作方法：
- **子表删除**: 根据主表ID删除子表数据
- **子表批量插入**: 批量插入子表数据
- **子表批量删除**: 批量删除子表数据

## 模板变量说明

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `${packageName}` | 包名 | `com.jkr.project.system` |
| `${ClassName}` | 类名（首字母大写） | `SysUser` |
| `${className}` | 类名（首字母小写） | `sysUser` |
| `${functionName}` | 功能名称 | `用户信息` |
| `${author}` | 作者 | `jkr` |
| `${datetime}` | 生成时间 | `2024-01-01` |
| `${pkColumn.javaField}` | 主键字段名 | `userId` |
| `${pkColumn.javaType}` | 主键类型 | `Long` |
| `${pkColumn.capJavaField}` | 主键字段名（首字母大写） | `UserId` |
| `${subClassName}` | 子表类名 | `SysUserRole` |
| `${subclassName}` | 子表类名（首字母小写） | `sysUserRole` |
| `${subTableFkClassName}` | 子表外键字段名 | `UserId` |

## 方法说明

### 基础CRUD方法

1. **查询方法**
   - `select${ClassName}By${pkColumn.capJavaField}()`: 根据主键查询
   - `select${ClassName}List()`: 条件查询列表

2. **插入方法**
   - `insert${ClassName}()`: 新增记录

3. **更新方法**
   - `update${ClassName}()`: 更新记录

4. **删除方法**
   - `delete${ClassName}By${pkColumn.capJavaField}()`: 单条物理删除
   - `delete${ClassName}By${pkColumn.capJavaField}s()`: 批量物理删除
   - `logicRemoveByIds()`: 批量逻辑删除
   - `logicRemoveBy${pkColumn.capJavaField}()`: 单条逻辑删除

### 子表操作方法（条件生成）

当`$table.sub`为true时生成：
- `delete${subClassName}By${subTableFkClassName}s()`: 批量删除子表数据
- `batch${subClassName}()`: 批量插入子表数据
- `delete${subClassName}By${subTableFkClassName}()`: 根据主表ID删除子表数据

## 生成示例

```java
package com.jkr.project.system.mapper;

import java.util.List;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Mapper;
import com.jkr.project.system.domain.SysUser;

/**
 * 用户信息Mapper接口
 *
 * @author jkr
 * @date 2024-01-01
 */
@Mapper
public interface SysUserMapper extends BaseMapper<SysUser> {
    /**
     * 查询用户信息
     *
     * @param userId 用户信息主键
     * @return 用户信息
     */
    SysUser selectSysUserByUserId(Long userId);

    /**
     * 查询用户信息列表
     *
     * @param sysUser 用户信息
     * @return 用户信息集合
     */
    List<SysUser> selectSysUserList(SysUser sysUser);

    /**
     * 新增用户信息
     *
     * @param sysUser 用户信息
     * @return 结果
     */
    int insertSysUser(SysUser sysUser);

    /**
     * 修改用户信息
     *
     * @param sysUser 用户信息
     * @return 结果
     */
    int updateSysUser(SysUser sysUser);

    /**
     * 删除用户信息
     *
     * @param userId 用户信息主键
     * @return 结果
     */
    int deleteSysUserByUserId(Long userId);

    /**
     * 批量删除用户信息
     *
     * @param userIds 需要删除的数据主键集合
     * @return 结果
     */
    int deleteSysUserByUserIds(Long[] userIds);

    /**
     * 批量逻辑删除用户信息
     *
     * @param ids 用户信息主键
     * @return 结果
     */
    int logicRemoveByIds(List<Long> ids);

    /**
     * 通过用户信息主键id逻辑删除信息
     *
     * @param userId 用户信息主键
     * @return 结果
     */
    int logicRemoveByUserId(Long userId);
}
```

## 原始模板内容

```velocity
package ${packageName}.mapper;

import java.util.List;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Mapper;
import ${packageName}.domain.${ClassName};
#if($table.sub)
import ${packageName}.domain.${subClassName};
#end

/**
 * ${functionName}Mapper接口
 *
 * @author ${author}
 * @date ${datetime}
 */
@Mapper
public interface ${ClassName}Mapper extends BaseMapper<${ClassName}> {
    /**
     * 查询${functionName}
     *
     * @param ${pkColumn.javaField} ${functionName}主键
     * @return ${functionName}
     */
    ${ClassName} select${ClassName}By${pkColumn.capJavaField}(${pkColumn.javaType} ${pkColumn.javaField});

    /**
     * 查询${functionName}列表
     *
     * @param ${className} ${functionName}
     * @return ${functionName}集合
     */
    List<${ClassName}> select${ClassName}List(${ClassName} ${className});

    /**
     * 新增${functionName}
     *
     * @param ${className} ${functionName}
     * @return 结果
     */
    int insert${ClassName}(${ClassName} ${className});

    /**
     * 修改${functionName}
     *
     * @param ${className} ${functionName}
     * @return 结果
     */
    int update${ClassName}(${ClassName} ${className});

    /**
     * 删除${functionName}
     *
     * @param ${pkColumn.javaField} ${functionName}主键
     * @return 结果
     */
    int delete${ClassName}By${pkColumn.capJavaField}(${pkColumn.javaType} ${pkColumn.javaField});

    /**
     * 批量删除${functionName}
     *
     * @param ${pkColumn.javaField}s 需要删除的数据主键集合
     * @return 结果
     */
    int delete${ClassName}By${pkColumn.capJavaField}s(${pkColumn.javaType}[] ${pkColumn.javaField}s);

    /**
     * 批量逻辑删除${functionName}
     *
     * @param ids ${functionName}主键
     * @return 结果
     */
    int logicRemoveByIds(List<Long> ids);

    /**
     * 通过${functionName}主键id逻辑删除信息
     *
     * @param ${pkColumn.javaField} ${functionName}主键
     * @return 结果
     */
    int logicRemoveBy${pkColumn.capJavaField}(${pkColumn.javaType} ${pkColumn.javaField});
#if($table.sub)

    /**
     * 批量删除${subTable.functionName}
     *
     * @param ${pkColumn.javaField}s 需要删除的数据主键集合
     * @return 结果
     */
    int delete${subClassName}By${subTableFkClassName}s(${pkColumn.javaType}[] ${pkColumn.javaField}s);

    /**
     * 批量新增${subTable.functionName}
     *
     * @param ${subclassName}List ${subTable.functionName}列表
     * @return 结果
     */
    int batch${subClassName}(List<${subClassName}> ${subclassName}List);

    /**
     * 通过${functionName}主键删除${subTable.functionName}信息
     *
     * @param ${pkColumn.javaField} ${functionName}ID
     * @return 结果
     */
    int delete${subClassName}By${subTableFkClassName}(${pkColumn.javaType} ${pkColumn.javaField});
#end
}
```

## 使用说明

1. **MyBatis Plus集成**: 继承BaseMapper获得基础CRUD功能
2. **自定义方法**: 扩展业务特定的数据访问方法
3. **逻辑删除**: 支持逻辑删除，保护数据安全
4. **批量操作**: 提供批量操作方法，提高性能
5. **主子表**: 自动处理主子表关联操作
6. **XML映射**: 需要配合对应的XML映射文件实现具体SQL
7. **事务支持**: 在Service层控制事务，Mapper层专注数据访问
8. **参数映射**: 支持复杂参数和结果映射

## 配套XML文件

生成的Mapper接口需要配套的XML映射文件来实现具体的SQL语句：
- 文件位置：`resources/mapper/${moduleName}/${ClassName}Mapper.xml`
- SQL实现：包含所有自定义方法的SQL实现
- 结果映射：定义复杂的结果集映射关系
- 动态SQL：支持动态条件查询

## 扩展功能

- **分页查询**: 集成MyBatis Plus分页插件
- **条件构造**: 使用QueryWrapper构造复杂查询条件
- **性能优化**: 支持SQL性能监控和优化
- **多数据源**: 支持多数据源配置
- **读写分离**: 支持主从数据库读写分离