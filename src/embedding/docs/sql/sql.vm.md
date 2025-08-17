# 菜单权限SQL模板 (sql.vm)

## 模板功能说明

这个模板用于生成系统菜单和权限按钮的SQL插入语句，为新生成的业务模块自动创建对应的菜单项和操作权限。生成的SQL包含主菜单和标准的CRUD操作按钮权限，确保新模块能够正确集成到系统的权限管理体系中。

## 主要特性

### 1. 菜单结构
- **主菜单创建**: 创建业务模块的主菜单项
- **按钮权限**: 自动创建标准的操作按钮权限
- **层级关系**: 建立父子菜单的层级关系
- **权限标识**: 为每个操作分配唯一的权限标识符

### 2. 标准权限操作
- **查询权限**: `${permissionPrefix}:query` - 数据查询权限
- **列表权限**: `${permissionPrefix}:list` - 列表查看权限
- **新增权限**: `${permissionPrefix}:add` - 数据新增权限
- **修改权限**: `${permissionPrefix}:edit` - 数据修改权限
- **删除权限**: `${permissionPrefix}:remove` - 单条删除权限
- **批量删除**: `${permissionPrefix}:batchRemove` - 批量删除权限
- **导出权限**: `${permissionPrefix}:export` - 数据导出权限

### 3. 数据库特性
- **自增ID获取**: 使用`LAST_INSERT_ID()`获取父菜单ID
- **变量使用**: 使用MySQL变量存储父菜单ID
- **时间函数**: 使用`sysdate()`设置创建时间
- **事务安全**: 支持事务回滚和提交

### 4. 菜单配置
- **菜单类型**: 区分目录(C)和按钮(F)类型
- **显示状态**: 控制菜单的显示和隐藏
- **缓存设置**: 配置页面缓存策略
- **外链支持**: 支持内部组件和外部链接

## 模板变量说明

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `${functionName}` | 功能名称（中文） | `用户管理` |
| `${parentMenuId}` | 父菜单ID | `1` |
| `${businessName}` | 业务名称（小写） | `user` |
| `${moduleName}` | 模块名称（小写） | `system` |
| `${permissionPrefix}` | 权限前缀 | `system:user` |

## 菜单表结构说明

### sys_menu表字段

| 字段名 | 类型 | 说明 | 示例值 |
|--------|------|------|--------|
| `menu_name` | varchar | 菜单名称 | `用户管理` |
| `parent_id` | bigint | 父菜单ID | `1` |
| `order_num` | int | 显示顺序 | `1` |
| `path` | varchar | 路由地址 | `user` |
| `component` | varchar | 组件路径 | `system/user/index` |
| `is_frame` | int | 是否为外链 | `1`(否) `0`(是) |
| `is_cache` | int | 是否缓存 | `1`(缓存) `0`(不缓存) |
| `menu_type` | char | 菜单类型 | `M`(目录) `C`(菜单) `F`(按钮) |
| `visible` | char | 菜单状态 | `0`(显示) `1`(隐藏) |
| `status` | char | 菜单状态 | `0`(正常) `1`(停用) |
| `perms` | varchar | 权限标识 | `system:user:list` |
| `icon` | varchar | 菜单图标 | `user` |
| `create_by` | varchar | 创建者 | `admin` |
| `create_time` | datetime | 创建时间 | `2024-01-01 12:00:00` |
| `update_by` | varchar | 更新者 | `admin` |
| `update_time` | datetime | 更新时间 | `2024-01-01 12:00:00` |
| `remark` | varchar | 备注 | `用户管理菜单` |

## 生成示例

```sql
-- 菜单 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('用户管理', '1', '1', 'user', 'system/user/index', 1, 0, 'C', '0', '0', 'system:user:list', '#', 'admin', sysdate(), '', null, '用户管理菜单');

-- 按钮父菜单ID
SELECT @parentId := LAST_INSERT_ID();

-- 按钮 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('用户管理查询', @parentId, '1',  '#', '', 1, 0, 'F', '0', '0', 'system:user:query',        '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('用户管理新增', @parentId, '2',  '#', '', 1, 0, 'F', '0', '0', 'system:user:add',          '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('用户管理修改', @parentId, '3',  '#', '', 1, 0, 'F', '0', '0', 'system:user:edit',         '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('用户管理删除', @parentId, '4',  '#', '', 1, 0, 'F', '0', '0', 'system:user:remove',       '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('用户管理批量删除', @parentId, '5',  '#', '', 1, 0, 'F', '0', '0', 'system:user:batchRemove',       '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('用户管理导出', @parentId, '6',  '#', '', 1, 0, 'F', '0', '0', 'system:user:export',       '#', 'admin', sysdate(), '', null, '');
```

## 原始模板内容

```velocity
-- 菜单 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('${functionName}', '${parentMenuId}', '1', '${businessName}', '${moduleName}/${businessName}/index', 1, 0, 'C', '0', '0', '${permissionPrefix}:list', '#', 'admin', sysdate(), '', null, '${functionName}菜单');

-- 按钮父菜单ID
SELECT @parentId := LAST_INSERT_ID();

-- 按钮 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('${functionName}查询', @parentId, '1',  '#', '', 1, 0, 'F', '0', '0', '${permissionPrefix}:query',        '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('${functionName}新增', @parentId, '2',  '#', '', 1, 0, 'F', '0', '0', '${permissionPrefix}:add',          '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('${functionName}修改', @parentId, '3',  '#', '', 1, 0, 'F', '0', '0', '${permissionPrefix}:edit',         '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('${functionName}删除', @parentId, '4',  '#', '', 1, 0, 'F', '0', '0', '${permissionPrefix}:remove',       '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('${functionName}批量删除', @parentId, '5',  '#', '', 1, 0, 'F', '0', '0', '${permissionPrefix}:batchRemove',       '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('${functionName}导出', @parentId, '6',  '#', '', 1, 0, 'F', '0', '0', '${permissionPrefix}:export',       '#', 'admin', sysdate(), '', null, '');
```

## 使用场景

### 1. 代码生成集成
- **自动化部署**: 代码生成后自动创建对应的菜单权限
- **权限初始化**: 为新模块初始化完整的权限体系
- **开发效率**: 减少手动配置菜单的工作量
- **标准化**: 确保所有模块的权限配置标准一致

### 2. 权限管理
- **RBAC模型**: 支持基于角色的访问控制
- **细粒度控制**: 精确控制到按钮级别的操作权限
- **动态权限**: 支持运行时的权限分配和回收
- **权限继承**: 支持角色权限的继承和覆盖

### 3. 系统集成
- **菜单渲染**: 前端根据权限动态渲染菜单
- **按钮控制**: 前端根据权限控制按钮的显示隐藏
- **接口鉴权**: 后端根据权限控制接口访问
- **审计日志**: 记录权限相关的操作日志

## 设计特点

### 1. 标准化权限
- **统一命名**: 所有权限标识符遵循统一的命名规范
- **完整覆盖**: 涵盖标准CRUD操作的所有权限点
- **扩展性**: 支持添加自定义的业务权限
- **层次清晰**: 权限层次结构清晰明确

### 2. 数据库优化
- **批量插入**: 使用单个事务完成所有插入操作
- **关联维护**: 自动维护父子菜单的关联关系
- **索引友好**: 权限查询使用索引优化性能
- **数据一致性**: 确保菜单数据的完整性和一致性

### 3. 维护便利
- **模板化**: 使用模板生成，便于批量处理
- **可追溯**: 记录创建时间和创建人信息
- **可修改**: 支持后续的菜单调整和权限变更
- **可删除**: 支持模块卸载时的权限清理

## 使用说明

### 1. 执行顺序
```sql
-- 1. 首先执行主菜单插入
INSERT INTO sys_menu (...) VALUES (...);

-- 2. 获取主菜单ID
SELECT @parentId := LAST_INSERT_ID();

-- 3. 依次插入按钮权限
INSERT INTO sys_menu (...) VALUES (...);
```

### 2. 事务处理
```sql
-- 开始事务
START TRANSACTION;

-- 执行菜单SQL
-- ... 菜单插入语句 ...

-- 提交事务
COMMIT;

-- 如果出错则回滚
-- ROLLBACK;
```

### 3. 权限验证
```sql
-- 验证菜单是否创建成功
SELECT * FROM sys_menu WHERE menu_name = '用户管理';

-- 验证按钮权限是否创建成功
SELECT * FROM sys_menu WHERE parent_id = @parentId;

-- 验证权限标识是否正确
SELECT * FROM sys_menu WHERE perms LIKE 'system:user:%';
```

## 权限配置详解

### 1. 菜单类型说明
- **M (目录)**: 菜单目录，用于组织菜单结构
- **C (菜单)**: 具体的菜单页面，对应前端路由
- **F (按钮)**: 页面内的操作按钮，用于细粒度权限控制

### 2. 权限标识规范
```
权限格式: ${模块名}:${业务名}:${操作名}

示例:
system:user:list     - 用户列表查看权限
system:user:add      - 用户新增权限
system:user:edit     - 用户编辑权限
system:user:remove   - 用户删除权限
system:user:export   - 用户导出权限
```

### 3. 显示控制
- **visible**: 控制菜单在导航中的显示
  - `0`: 显示（默认）
  - `1`: 隐藏
- **status**: 控制菜单的启用状态
  - `0`: 正常（默认）
  - `1`: 停用

## 最佳实践

### 1. 权限设计
- **最小权限**: 遵循最小权限原则，只分配必要的权限
- **权限分离**: 查询和修改权限分离，读写权限分离
- **角色设计**: 设计合理的角色层次，避免权限冗余
- **权限审计**: 定期审计权限分配，清理无用权限

### 2. 菜单组织
- **层次清晰**: 菜单层次不宜过深，一般不超过3层
- **分类合理**: 按业务模块合理分类组织菜单
- **命名规范**: 菜单命名要简洁明确，便于理解
- **图标统一**: 使用统一的图标风格和规范

### 3. 性能优化
- **索引优化**: 为权限查询字段添加合适的索引
- **缓存策略**: 对权限数据进行合理的缓存
- **批量操作**: 权限变更时使用批量操作提高效率
- **懒加载**: 菜单数据采用懒加载策略

### 4. 安全考虑
- **权限校验**: 前后端都要进行权限校验
- **会话管理**: 权限变更后及时更新用户会话
- **日志记录**: 记录权限相关的敏感操作
- **异常处理**: 妥善处理权限异常情况

## 扩展功能

### 1. 自定义权限
```sql
-- 添加自定义业务权限
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('${functionName}审核', @parentId, '7',  '#', '', 1, 0, 'F', '0', '0', '${permissionPrefix}:audit', '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('${functionName}导入', @parentId, '8',  '#', '', 1, 0, 'F', '0', '0', '${permissionPrefix}:import', '#', 'admin', sysdate(), '', null, '');
```

### 2. 条件权限
```sql
-- 根据业务需要添加条件权限
#if($table.crud || $table.sub)
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('${functionName}详情', @parentId, '9',  '#', '', 1, 0, 'F', '0', '0', '${permissionPrefix}:detail', '#', 'admin', sysdate(), '', null, '');
#end
```

### 3. 权限清理
```sql
-- 删除模块相关的所有权限（用于模块卸载）
DELETE FROM sys_menu WHERE perms LIKE '${permissionPrefix}:%';

-- 删除指定父菜单下的所有子菜单
DELETE FROM sys_menu WHERE parent_id IN (
    SELECT menu_id FROM sys_menu WHERE perms = '${permissionPrefix}:list'
);
```

### 4. 权限迁移
```sql
-- 权限数据迁移脚本
UPDATE sys_menu SET perms = REPLACE(perms, 'old_prefix', 'new_prefix') 
WHERE perms LIKE 'old_prefix:%';

-- 菜单路径更新
UPDATE sys_menu SET path = 'new_path', component = 'new_module/new_business/index' 
WHERE perms = '${permissionPrefix}:list';
```