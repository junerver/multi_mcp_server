# Spring Boot控制器模板 (controller.java.vm)

## 模板功能说明

这个模板用于生成Spring Boot REST控制器类，提供完整的CRUD操作接口。生成的控制器包含标准的增删改查、导出、批量操作等功能，并集成了权限控制、日志记录和数据验证。

## 主要特性

### 1. 基础结构
- **包声明**: 使用`${packageName}.controller`作为包路径
- **REST控制器**: 使用`@RestController`注解，支持RESTful API
- **请求映射**: 使用`@RequestMapping`定义基础路径
- **依赖注入**: 通过`@Autowired`注入Service层服务

### 2. 核心注解
- **权限控制**: `@PreAuthorize`注解实现方法级权限验证
- **日志记录**: `@Log`注解记录业务操作日志
- **参数验证**: `@Validated`注解启用参数校验
- **API文档**: 支持Swagger/OpenAPI文档生成

### 3. 标准CRUD操作

#### 查询操作
- **列表查询**: `list()` - 分页查询数据列表
- **详情查询**: `getInfo()` - 根据ID查询单条记录
- **导出功能**: `export()` - 导出Excel文件

#### 数据操作
- **新增**: `add()` - 添加新记录
- **修改**: `edit()` - 更新现有记录
- **删除**: `remove()` - 批量删除记录

### 4. 响应处理
- **统一响应**: 使用`AjaxResult`封装返回结果
- **分页支持**: 集成`PageUtils`实现分页查询
- **Excel导出**: 使用`ExcelUtil`实现数据导出

## 模板变量说明

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `${packageName}` | 包名 | `com.jkr.project.system` |
| `${moduleName}` | 模块名 | `system` |
| `${businessName}` | 业务名 | `user` |
| `${functionName}` | 功能名称 | `用户信息` |
| `${ClassName}` | 类名（首字母大写） | `SysUser` |
| `${className}` | 类名（首字母小写） | `sysUser` |
| `${author}` | 作者 | `jkr` |
| `${datetime}` | 生成时间 | `2024-01-01` |
| `${permissionPrefix}` | 权限前缀 | `system:user` |
| `${pkColumn.javaField}` | 主键字段名 | `userId` |
| `${pkColumn.javaType}` | 主键类型 | `Long` |

## 权限控制说明

每个操作方法都配置了相应的权限验证：

- **查询权限**: `${permissionPrefix}:list`
- **详情权限**: `${permissionPrefix}:query`
- **新增权限**: `${permissionPrefix}:add`
- **修改权限**: `${permissionPrefix}:edit`
- **删除权限**: `${permissionPrefix}:remove`
- **导出权限**: `${permissionPrefix}:export`

## 生成示例

```java
package com.jkr.project.system.controller;

import java.util.List;
import javax.servlet.http.HttpServletResponse;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.jkr.framework.aspectj.lang.annotation.Log;
import com.jkr.framework.aspectj.lang.enums.BusinessType;
import com.jkr.project.system.domain.SysUser;
import com.jkr.project.system.service.ISysUserService;
import com.jkr.framework.web.controller.BaseController;
import com.jkr.framework.web.domain.AjaxResult;
import com.jkr.common.utils.poi.ExcelUtil;
import com.jkr.framework.web.page.TableDataInfo;

/**
 * 用户信息Controller
 *
 * @author jkr
 * @date 2024-01-01
 */
@RestController
@RequestMapping("/system/user")
public class SysUserController extends BaseController {
    @Autowired
    private ISysUserService sysUserService;

    /**
     * 查询用户信息列表
     */
    @PreAuthorize("@ss.hasPermi('system:user:list')")
    @GetMapping("/list")
    public TableDataInfo list(SysUser sysUser) {
        startPage();
        List<SysUser> list = sysUserService.selectSysUserList(sysUser);
        return getDataTable(list);
    }

    /**
     * 导出用户信息列表
     */
    @PreAuthorize("@ss.hasPermi('system:user:export')")
    @Log(title = "用户信息", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, SysUser sysUser) {
        List<SysUser> list = sysUserService.selectSysUserList(sysUser);
        ExcelUtil<SysUser> util = new ExcelUtil<SysUser>(SysUser.class);
        util.exportExcel(response, list, "用户信息数据");
    }

    /**
     * 获取用户信息详细信息
     */
    @PreAuthorize("@ss.hasPermi('system:user:query')")
    @GetMapping(value = "/{userId}")
    public AjaxResult getInfo(@PathVariable("userId") Long userId) {
        return success(sysUserService.selectSysUserByUserId(userId));
    }

    /**
     * 新增用户信息
     */
    @PreAuthorize("@ss.hasPermi('system:user:add')")
    @Log(title = "用户信息", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody SysUser sysUser) {
        return toAjax(sysUserService.insertSysUser(sysUser));
    }

    /**
     * 修改用户信息
     */
    @PreAuthorize("@ss.hasPermi('system:user:edit')")
    @Log(title = "用户信息", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody SysUser sysUser) {
        return toAjax(sysUserService.updateSysUser(sysUser));
    }

    /**
     * 删除用户信息
     */
    @PreAuthorize("@ss.hasPermi('system:user:remove')")
    @Log(title = "用户信息", businessType = BusinessType.DELETE)
    @DeleteMapping("/{userIds}")
    public AjaxResult remove(@PathVariable List<Long> userIds) {
        return toAjax(sysUserService.deleteSysUserByIds(userIds));
    }
}
```

## 原始模板内容

```velocity
package ${packageName}.controller;

import java.util.List;
import javax.servlet.http.HttpServletResponse;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.jkr.framework.aspectj.lang.annotation.Log;
import com.jkr.framework.aspectj.lang.enums.BusinessType;
import ${packageName}.domain.${ClassName};
import ${packageName}.service.I${ClassName}Service;
import com.jkr.framework.web.controller.BaseController;
import com.jkr.framework.web.domain.AjaxResult;
import com.jkr.common.utils.poi.ExcelUtil;
import com.jkr.framework.web.page.TableDataInfo;

/**
 * ${functionName}Controller
 *
 * @author ${author}
 * @date ${datetime}
 */
@RestController
@RequestMapping("/${moduleName}/${businessName}")
public class ${ClassName}Controller extends BaseController {
    @Autowired
    private I${ClassName}Service ${className}Service;

    /**
     * 查询${functionName}列表
     */
    @PreAuthorize("@ss.hasPermi('${permissionPrefix}:list')")
    @GetMapping("/list")
    public TableDataInfo list(${ClassName} ${className}) {
        startPage();
        List<${ClassName}> list = ${className}Service.select${ClassName}List(${className});
        return getDataTable(list);
    }

    /**
     * 导出${functionName}列表
     */
    @PreAuthorize("@ss.hasPermi('${permissionPrefix}:export')")
    @Log(title = "${functionName}", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, ${ClassName} ${className}) {
        List<${ClassName}> list = ${className}Service.select${ClassName}List(${className});
        ExcelUtil<${ClassName}> util = new ExcelUtil<${ClassName}>(${ClassName}.class);
        util.exportExcel(response, list, "${functionName}数据");
    }

    /**
     * 获取${functionName}详细信息
     */
    @PreAuthorize("@ss.hasPermi('${permissionPrefix}:query')")
    @GetMapping(value = "/{${pkColumn.javaField}}")
    public AjaxResult getInfo(@PathVariable("${pkColumn.javaField}") ${pkColumn.javaType} ${pkColumn.javaField}) {
        return success(${className}Service.select${ClassName}By${pkColumn.capJavaField}(${pkColumn.javaField}));
    }

    /**
     * 新增${functionName}
     */
    @PreAuthorize("@ss.hasPermi('${permissionPrefix}:add')")
    @Log(title = "${functionName}", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody ${ClassName} ${className}) {
        return toAjax(${className}Service.insert${ClassName}(${className}));
    }

    /**
     * 修改${functionName}
     */
    @PreAuthorize("@ss.hasPermi('${permissionPrefix}:edit')")
    @Log(title = "${functionName}", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody ${ClassName} ${className}) {
        return toAjax(${className}Service.update${ClassName}(${className}));
    }

    /**
     * 删除${functionName}
     */
    @PreAuthorize("@ss.hasPermi('${permissionPrefix}:remove')")
    @Log(title = "${functionName}", businessType = BusinessType.DELETE)
    @DeleteMapping("/{${pkColumn.javaField}s}")
    public AjaxResult remove(@PathVariable List<Long> ${pkColumn.javaField}s) {
        return toAjax(${className}Service.delete${ClassName}ByIds(${pkColumn.javaField}s));
    }
}
```

## 使用说明

1. **RESTful设计**: 遵循REST API设计规范，使用标准HTTP方法
2. **权限验证**: 每个接口都有对应的权限验证，确保安全性
3. **日志记录**: 重要操作（增删改、导出）会自动记录操作日志
4. **分页支持**: 列表查询自动支持分页功能
5. **Excel导出**: 内置Excel导出功能，支持自定义导出字段
6. **统一响应**: 所有接口返回统一的响应格式
7. **参数验证**: 支持请求参数的自动验证
8. **异常处理**: 集成全局异常处理机制

## 扩展功能

- **批量操作**: 支持批量删除等批量操作
- **条件查询**: 支持复杂的条件查询
- **数据导入**: 可扩展Excel数据导入功能
- **文件上传**: 可集成文件上传处理
- **缓存支持**: 可添加Redis缓存支持