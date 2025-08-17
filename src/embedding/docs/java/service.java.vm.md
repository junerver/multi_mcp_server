# 业务服务接口模板 (service.java.vm)

## 模板功能说明

这个模板用于生成业务服务层接口（Service Interface），定义了业务逻辑的标准操作方法。生成的接口遵循面向接口编程的原则，为业务层提供清晰的方法定义和契约规范。

## 主要特性

### 1. 基础结构
- **包声明**: 使用`${packageName}.service`作为包路径
- **接口定义**: 定义业务服务接口，以`I${ClassName}Service`命名
- **方法契约**: 提供标准的业务方法签名和文档
- **返回类型**: 明确定义每个方法的返回类型和参数

### 2. 核心业务方法

#### 查询操作
- **单条查询**: 根据主键查询单条记录
- **列表查询**: 根据条件查询记录列表
- **条件查询**: 支持复杂的业务查询逻辑

#### 数据操作
- **新增操作**: 新增业务数据
- **修改操作**: 更新现有业务数据
- **删除操作**: 删除业务数据（支持单条和批量）

### 3. 方法设计原则
- **简洁明确**: 方法名清晰表达业务意图
- **参数合理**: 参数设计符合业务逻辑
- **返回统一**: 统一的返回类型设计
- **文档完整**: 每个方法都有完整的JavaDoc注释

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

## 方法说明

### 1. 查询方法

#### `select${ClassName}By${pkColumn.capJavaField}()`
- **功能**: 根据主键查询单条记录
- **参数**: 主键值
- **返回**: 实体对象或null
- **用途**: 详情查询、数据验证

#### `select${ClassName}List()`
- **功能**: 根据条件查询记录列表
- **参数**: 查询条件对象
- **返回**: 实体对象列表
- **用途**: 列表展示、条件查询

### 2. 数据操作方法

#### `insert${ClassName}()`
- **功能**: 新增记录
- **参数**: 实体对象
- **返回**: 影响行数（int）
- **用途**: 数据新增操作

#### `update${ClassName}()`
- **功能**: 更新记录
- **参数**: 实体对象
- **返回**: 影响行数（int）
- **用途**: 数据修改操作

#### `delete${ClassName}ByIds()`
- **功能**: 批量删除记录
- **参数**: 主键ID列表
- **返回**: 影响行数（int）
- **用途**: 批量删除操作

#### `delete${ClassName}By${pkColumn.capJavaField}()`
- **功能**: 单条删除记录
- **参数**: 主键值
- **返回**: 影响行数（int）
- **用途**: 单条删除操作

## 生成示例

```java
package com.jkr.project.system.service;

import java.util.List;
import com.jkr.project.system.domain.SysUser;

/**
 * 用户信息Service接口
 *
 * @author jkr
 * @date 2024-01-01
 */
public interface ISysUserService {
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
     * 批量删除用户信息
     *
     * @param ids 需要删除的用户信息主键集合
     * @return 结果
     */
    int deleteSysUserByIds(List<Long> ids);

    /**
     * 删除用户信息信息
     *
     * @param userId 用户信息主键
     * @return 结果
     */
    int deleteSysUserByUserId(Long userId);
}
```

## 原始模板内容

```velocity
package ${packageName}.service;

import java.util.List;
import ${packageName}.domain.${ClassName};

/**
 * ${functionName}Service接口
 *
 * @author ${author}
 * @date ${datetime}
 */
public interface I${ClassName}Service {
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
     * 批量删除${functionName}
     *
     * @param ids 需要删除的${functionName}主键集合
     * @return 结果
     */
    int delete${ClassName}ByIds(List<Long> ids);

    /**
     * 删除${functionName}信息
     *
     * @param ${pkColumn.javaField} ${functionName}主键
     * @return 结果
     */
    int delete${ClassName}By${pkColumn.capJavaField}(${pkColumn.javaType} ${pkColumn.javaField});
}
```

## 设计原则

### 1. 接口隔离原则
- **职责单一**: 每个接口专注于特定的业务领域
- **方法内聚**: 相关的业务方法组织在同一接口中
- **依赖最小**: 客户端只依赖它需要的接口方法

### 2. 契约设计
- **明确签名**: 方法签名清晰表达输入输出
- **异常处理**: 在实现类中处理业务异常
- **返回约定**: 统一的返回值约定（如影响行数）

### 3. 扩展性考虑
- **预留接口**: 为未来功能扩展预留接口方法
- **版本兼容**: 接口变更时保持向后兼容
- **实现灵活**: 支持多种实现方式

## 使用说明

1. **接口实现**: 需要对应的ServiceImpl实现类
2. **依赖注入**: 在Controller中注入接口而非实现类
3. **事务管理**: 在实现类中处理事务逻辑
4. **业务验证**: 在实现类中进行业务规则验证
5. **异常处理**: 在实现类中处理业务异常
6. **日志记录**: 在实现类中记录业务日志
7. **缓存策略**: 在实现类中实现缓存逻辑
8. **性能优化**: 在实现类中进行性能优化

## 扩展功能

### 常见扩展方法
- **分页查询**: `selectPageList()` - 分页查询方法
- **条件统计**: `countByCondition()` - 条件统计方法
- **批量操作**: `batchInsert()` - 批量插入方法
- **状态更新**: `updateStatus()` - 状态更新方法
- **导入导出**: `importData()` / `exportData()` - 数据导入导出

### 业务特定方法
- **业务查询**: 根据具体业务需求添加查询方法
- **业务操作**: 添加特定的业务操作方法
- **数据验证**: 添加数据验证相关方法
- **关联操作**: 添加关联数据操作方法

## 最佳实践

1. **命名规范**: 遵循统一的方法命名规范
2. **参数设计**: 合理设计方法参数，避免过多参数
3. **返回类型**: 选择合适的返回类型，考虑null安全
4. **文档注释**: 提供完整的JavaDoc注释
5. **接口稳定**: 保持接口的稳定性，谨慎修改
6. **版本管理**: 接口变更时考虑版本兼容性
7. **测试友好**: 设计易于单元测试的接口
8. **性能考虑**: 考虑方法调用的性能影响