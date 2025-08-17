# 业务服务实现类模板 (serviceImpl.java.vm)

## 模板功能说明

这个模板用于生成业务服务层实现类（Service Implementation），实现对应的Service接口，提供完整的业务逻辑处理。生成的实现类集成了事务管理、安全控制、数据验证和主子表操作等功能。

## 主要特性

### 1. 基础结构
- **包声明**: 使用`${packageName}.service.impl`作为包路径
- **类定义**: 实现对应的Service接口，以`${ClassName}ServiceImpl`命名
- **注解配置**: 使用`@Service`和`@Transactional`注解
- **依赖注入**: 通过`@Autowired`注入Mapper层

### 2. 核心注解
- **@Service**: 标识为Spring服务组件
- **@Transactional**: 类级别事务管理
- **@Transactional(readOnly = false, rollbackFor = Exception.class)**: 方法级别事务控制
- **@Autowired**: 依赖注入Mapper

### 3. 业务功能

#### 查询操作
- **单条查询**: 直接调用Mapper方法
- **列表查询**: 支持条件查询和分页
- **数据验证**: 查询前的参数验证

#### 数据操作
- **新增操作**: 包含数据初始化和主子表处理
- **修改操作**: 包含数据更新和主子表同步
- **删除操作**: 支持逻辑删除和物理删除

### 4. 高级特性

#### 自动数据填充
- **新增时**: 调用`insertInit()`设置创建信息
- **修改时**: 调用`updateInit()`设置更新信息
- **用户信息**: 自动获取当前登录用户信息

#### 主子表支持
- **新增时**: 自动处理子表数据插入
- **修改时**: 先删除旧子表数据，再插入新数据
- **删除时**: 级联删除子表数据

#### 逻辑删除
- **批量删除**: 使用`logicRemoveByIds()`进行逻辑删除
- **单条删除**: 使用`logicRemoveBy${pkColumn.capJavaField}()`进行逻辑删除
- **物理删除**: 保留物理删除代码（注释状态）

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

## 方法实现说明

### 1. 查询方法

#### `select${ClassName}By${pkColumn.capJavaField}()`
```java
@Override
public ${ClassName} select${ClassName}By${pkColumn.capJavaField}(${pkColumn.javaType} ${pkColumn.javaField}) {
    return ${className}Mapper.select${ClassName}By${pkColumn.capJavaField}(${pkColumn.javaField});
}
```
- **功能**: 直接调用Mapper层方法
- **事务**: 只读事务（默认）

#### `select${ClassName}List()`
```java
@Override
public List<${ClassName}> select${ClassName}List(${ClassName} ${className}) {
    return ${className}Mapper.select${ClassName}List(${className});
}
```
- **功能**: 条件查询列表
- **事务**: 只读事务（默认）

### 2. 数据操作方法

#### `insert${ClassName}()`
```java
@Override
@Transactional(readOnly = false, rollbackFor = Exception.class)
public int insert${ClassName}(${ClassName} ${className}) {
    ${className}.insertInit(SecurityUtils.getLoginUser().getUsername());
    // 主子表处理逻辑
    int rows = ${className}Mapper.insert${ClassName}(${className});
    insert${subClassName}(${className}); // 如果有子表
    return rows;
}
```
- **事务**: 读写事务，异常回滚
- **数据初始化**: 自动设置创建信息
- **主子表**: 处理子表数据插入

#### `update${ClassName}()`
```java
@Override
@Transactional(readOnly = false, rollbackFor = Exception.class)
public int update${ClassName}(${ClassName} ${className}) {
    ${className}.updateInit(SecurityUtils.getLoginUser().getUsername());
    // 主子表处理：先删除后插入
    ${className}Mapper.delete${subClassName}By${subTableFkClassName}(${className}.get${pkColumn.capJavaField}());
    insert${subClassName}(${className});
    return ${className}Mapper.update${ClassName}(${className});
}
```
- **事务**: 读写事务，异常回滚
- **数据更新**: 自动设置更新信息
- **主子表**: 先删除旧数据，再插入新数据

#### `delete${ClassName}ByIds()`
```java
@Override
@Transactional(readOnly = false, rollbackFor = Exception.class)
public int delete${ClassName}ByIds(List<Long> ids) {
    ${className}Mapper.delete${subClassName}ByIds(ids); // 如果有子表
    return ${className}Mapper.logicRemoveByIds(ids);
}
```
- **事务**: 读写事务，异常回滚
- **逻辑删除**: 使用逻辑删除保护数据
- **主子表**: 级联删除子表数据

### 3. 子表操作方法（条件生成）

#### `insert${subClassName}()`
```java
@Transactional(readOnly = false, rollbackFor = Exception.class)
public void insert${subClassName}(${ClassName} ${className}) {
    List<${subClassName}> ${subclassName}List = ${className}.get${subClassName}List();
    ${pkColumn.javaType} ${pkColumn.javaField} = ${className}.get${pkColumn.capJavaField}();
    if (JkrStringUtils.isNotNull(${subclassName}List)) {
        List<${subClassName}> list = new ArrayList<${subClassName}>();
        for (${subClassName} ${subclassName} : ${subclassName}List) {
            ${subclassName}.set${subTableFkClassName}(${pkColumn.javaField});
            list.add(${subclassName});
        }
        if (list.size() > 0) {
            ${className}Mapper.batch${subClassName}(list);
        }
    }
}
```
- **功能**: 批量插入子表数据
- **关联**: 自动设置外键关联
- **验证**: 检查数据有效性

## 生成示例

```java
package com.jkr.project.system.service.impl;

import java.util.List;
import com.jkr.common.utils.SecurityUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.jkr.project.system.mapper.SysUserMapper;
import com.jkr.project.system.domain.SysUser;
import com.jkr.project.system.service.ISysUserService;
import org.springframework.transaction.annotation.Transactional;

/**
 * 用户信息Service业务层处理
 *
 * @author jkr
 * @date 2024-01-01
 */
@Service
@Transactional
public class SysUserServiceImpl implements ISysUserService {
    @Autowired
    private SysUserMapper sysUserMapper;

    /**
     * 查询用户信息
     *
     * @param userId 用户信息主键
     * @return 用户信息
     */
    @Override
    public SysUser selectSysUserByUserId(Long userId) {
        return sysUserMapper.selectSysUserByUserId(userId);
    }

    /**
     * 查询用户信息列表
     *
     * @param sysUser 用户信息
     * @return 用户信息
     */
    @Override
    public List<SysUser> selectSysUserList(SysUser sysUser) {
        return sysUserMapper.selectSysUserList(sysUser);
    }

    /**
     * 新增用户信息
     *
     * @param sysUser 用户信息
     * @return 结果
     */
    @Override
    @Transactional(readOnly = false, rollbackFor = Exception.class)
    public int insertSysUser(SysUser sysUser) {
        sysUser.insertInit(SecurityUtils.getLoginUser().getUsername());
        return sysUserMapper.insertSysUser(sysUser);
    }

    /**
     * 修改用户信息
     *
     * @param sysUser 用户信息
     * @return 结果
     */
    @Override
    @Transactional(readOnly = false, rollbackFor = Exception.class)
    public int updateSysUser(SysUser sysUser) {
        sysUser.updateInit(SecurityUtils.getLoginUser().getUsername());
        return sysUserMapper.updateSysUser(sysUser);
    }

    /**
     * 批量删除用户信息
     *
     * @param userIds 需要删除的用户信息主键
     * @return 结果
     */
    @Override
    @Transactional(readOnly = false, rollbackFor = Exception.class)
    public int deleteSysUserByIds(List<Long> ids) {
        return sysUserMapper.logicRemoveByIds(ids);
    }

    /**
     * 删除用户信息信息
     *
     * @param userId 用户信息主键
     * @return 结果
     */
    @Override
    @Transactional(readOnly = false, rollbackFor = Exception.class)
    public int deleteSysUserByUserId(Long userId) {
        return sysUserMapper.logicRemoveByUserId(userId);
    }
}
```

## 原始模板内容

```velocity
package ${packageName}.service.impl;

import java.util.List;
#foreach ($column in $columns)
#if($column.javaField == 'createTime' || $column.javaField == 'updateTime')
#break
#end
#end
import com.jkr.common.utils.SecurityUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
#if($table.sub)
import java.util.ArrayList;
import com.jkr.common.utils.JkrStringUtils;
import ${packageName}.domain.${subClassName};
#end
import ${packageName}.mapper.${ClassName}Mapper;
import ${packageName}.domain.${ClassName};
import ${packageName}.service.I${ClassName}Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * ${functionName}Service业务层处理
 *
 * @author ${author}
 * @date ${datetime}
 */
@Service
@Transactional
public class ${ClassName}ServiceImpl implements I${ClassName}Service {
    @Autowired
    private ${ClassName}Mapper ${className}Mapper;

    /**
     * 查询${functionName}
     *
     * @param ${pkColumn.javaField} ${functionName}主键
     * @return ${functionName}
     */
    @Override
    public ${ClassName} select${ClassName}By${pkColumn.capJavaField}(${pkColumn.javaType} ${pkColumn.javaField}) {
        return ${className}Mapper.select${ClassName}By${pkColumn.capJavaField}(${pkColumn.javaField});
    }

    /**
     * 查询${functionName}列表
     *
     * @param ${className} ${functionName}
     * @return ${functionName}
     */
    @Override
    public List<${ClassName}> select${ClassName}List(${ClassName} ${className}) {
        return ${className}Mapper.select${ClassName}List(${className});
    }

    /**
     * 新增${functionName}
     *
     * @param ${className} ${functionName}
     * @return 结果
     */
    @Override
    @Transactional(readOnly = false, rollbackFor = Exception.class)
    public int insert${ClassName}(${ClassName} ${className}) {
        ${className}.insertInit(SecurityUtils.getLoginUser().getUsername());
#if($table.sub)
        int rows = ${className}Mapper.insert${ClassName}(${className});
        insert${subClassName}(${className});
        return rows;
#else
        return ${className}Mapper.insert${ClassName}(${className});
#end
    }

    /**
     * 修改${functionName}
     *
     * @param ${className} ${functionName}
     * @return 结果
     */
    @Override
    @Transactional(readOnly = false, rollbackFor = Exception.class)
    public int update${ClassName}(${ClassName} ${className}) {
        ${className}.updateInit(SecurityUtils.getLoginUser().getUsername());
#if($table.sub)
        ${className}Mapper.delete${subClassName}By${subTableFkClassName}(${className}.get${pkColumn.capJavaField}());
        insert${subClassName}(${className});
#end
        return ${className}Mapper.update${ClassName}(${className});
    }

    /**
     * 批量删除${functionName}
     *
     * @param ${pkColumn.javaField}s 需要删除的${functionName}主键
     * @return 结果
     */
    @Override
    @Transactional(readOnly = false, rollbackFor = Exception.class)
    public int delete${ClassName}ByIds(List<Long> ids) {
#if($table.sub)
        ${className}Mapper.delete${subClassName}ByIds(ids);
#end
        return ${className}Mapper.logicRemoveByIds(ids);
        //return ${className}Mapper.delete${ClassName}ByIds(ids);
    }

    /**
     * 删除${functionName}信息
     *
     * @param ${pkColumn.javaField} ${functionName}主键
     * @return 结果
     */
    @Override
    @Transactional(readOnly = false, rollbackFor = Exception.class)
    public int delete${ClassName}By${pkColumn.capJavaField}(${pkColumn.javaType} ${pkColumn.javaField}) {
#if($table.sub)
        ${className}Mapper.delete${subClassName}By${subTableFkClassName}(${pkColumn.javaField});
#end
        return ${className}Mapper.logicRemoveBy${pkColumn.capJavaField}(${pkColumn.javaField});
        //return ${className}Mapper.delete${ClassName}By${pkColumn.capJavaField}(${pkColumn.javaField});
    }

#if($table.sub)
    /**
     * 新增${subTable.functionName}信息
     *
     * @param ${className} ${functionName}对象
     */
    @Transactional(readOnly = false, rollbackFor = Exception.class)
    public void insert${subClassName}(${ClassName} ${className}) {
        List<${subClassName}> ${subclassName}List = ${className}.get${subClassName}List();
        ${pkColumn.javaType} ${pkColumn.javaField} = ${className}.get${pkColumn.capJavaField}();
        if (JkrStringUtils.isNotNull(${subclassName}List)) {
            List<${subClassName}> list = new ArrayList<${subClassName}>();
            for (${subClassName} ${subclassName} : ${subclassName}List) {
                ${subclassName}.set${subTableFkClassName}(${pkColumn.javaField});
                list.add(${subclassName});
            }
            if (list.size() > 0) {
                ${className}Mapper.batch${subClassName}(list);
            }
        }
    }
#end
}
```

## 使用说明

### 1. 事务管理
- **类级别**: `@Transactional`提供默认只读事务
- **方法级别**: 写操作使用`@Transactional(readOnly = false, rollbackFor = Exception.class)`
- **异常回滚**: 所有异常都会触发事务回滚

### 2. 安全控制
- **用户信息**: 通过`SecurityUtils.getLoginUser()`获取当前用户
- **数据初始化**: 自动设置创建人、创建时间、更新人、更新时间
- **权限验证**: 在Controller层进行权限验证

### 3. 数据验证
- **参数检查**: 使用`JkrStringUtils.isNotNull()`等工具类
- **业务验证**: 在方法中添加业务规则验证
- **数据完整性**: 确保主子表数据一致性

### 4. 性能优化
- **批量操作**: 使用批量插入、批量删除提高性能
- **逻辑删除**: 使用逻辑删除避免数据丢失
- **事务控制**: 合理控制事务范围

## 扩展功能

### 1. 缓存支持
```java
@Cacheable(value = "sysUser", key = "#userId")
public SysUser selectSysUserByUserId(Long userId) {
    return sysUserMapper.selectSysUserByUserId(userId);
}
```

### 2. 异步处理
```java
@Async
public CompletableFuture<Void> asyncProcessData(List<SysUser> users) {
    // 异步处理逻辑
    return CompletableFuture.completedFuture(null);
}
```

### 3. 事件发布
```java
@EventListener
public void handleUserCreated(UserCreatedEvent event) {
    // 处理用户创建事件
}
```

### 4. 数据验证
```java
private void validateUser(SysUser user) {
    if (StringUtils.isEmpty(user.getUserName())) {
        throw new ServiceException("用户名不能为空");
    }
}
```

## 最佳实践

1. **异常处理**: 使用自定义业务异常，提供清晰的错误信息
2. **日志记录**: 在关键业务节点记录操作日志
3. **参数验证**: 在方法入口进行参数有效性验证
4. **事务控制**: 合理设计事务边界，避免长事务
5. **性能监控**: 监控方法执行时间，优化慢查询
6. **代码复用**: 提取公共逻辑，减少代码重复
7. **单元测试**: 编写完整的单元测试用例
8. **文档维护**: 保持代码注释和文档的及时更新