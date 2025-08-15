# Vue 3 列表页面模板 (index.vue.vm)

## 功能概述

`v3/index.vue.vm` 是一个基于 Vue 3 Composition API 的代码生成模板，用于生成标准的数据列表管理页面。该模板生成的页面包含完整的 CRUD（增删改查）功能，支持搜索、分页、批量操作和数据导出等特性。

## 主要特性

### 1. Vue 3 Composition API
- 使用 `<script setup>` 语法
- 基于 Composition API 的响应式数据管理
- 现代化的 Vue 3 开发模式

### 2. 动态搜索表单
- 根据字段配置自动生成搜索条件
- 支持多种输入类型（文本、选择器、日期等）
- 支持日期范围查询
- 字典数据自动绑定

### 3. 数据表格展示
- 动态生成表格列
- 支持序号、选择框、操作列
- 特殊字段类型处理（日期、图片、字典）
- 分页功能集成

### 4. CRUD 操作
- 新增数据（调用 Form 组件）
- 编辑数据（调用 Form 组件）
- 单个/批量删除
- 数据导出功能

### 5. 权限控制
- 基于 `v-hasPermi` 指令的按钮权限控制
- 细粒度的操作权限管理

## 模板变量

### 核心变量
- `${BusinessName}`: 业务实体名称（首字母大写）
- `${businessName}`: 业务实体名称（首字母小写）
- `${moduleName}`: 模块名称
- `${pkColumn}`: 主键列信息
- `${columns}`: 字段列表
- `${dicts}`: 字典类型列表
- `${datetimeQueryFlag}`: 是否包含日期范围查询标志

### 字段属性
- `column.javaField`: Java 字段名
- `column.columnComment`: 字段注释
- `column.htmlType`: HTML 控件类型
- `column.dictType`: 字典类型
- `column.query`: 是否用于查询
- `column.list`: 是否在列表中显示
- `column.queryType`: 查询类型（如 BETWEEN）
- `column.pk`: 是否为主键
- `column.required`: 是否必填

## 支持的控件类型

### 搜索表单控件
- **input**: 文本输入框
- **select**: 下拉选择器（支持字典绑定）
- **radio**: 单选框（支持字典绑定）
- **datetime**: 日期选择器（支持单日期和日期范围）

### 表格列类型
- **普通文本**: 直接显示字段值
- **日期时间**: 格式化显示（YYYY-MM-DD）
- **图片**: 使用 `image-preview` 组件显示缩略图
- **字典**: 使用 `dict-tag` 组件显示字典标签
- **复选框**: 支持多选值的逗号分隔显示

## 生成示例

假设有一个用户管理模块，模板变量如下：
```
${BusinessName} = "User"
${businessName} = "user"
${moduleName} = "system"
${pkColumn.javaField} = "userId"
```

生成的组件将包含：
- 用户列表查询和展示
- 用户信息的增删改操作
- 用户数据导出功能
- 基于角色的权限控制

## 使用场景

### 1. 系统管理
- 用户管理、角色管理、菜单管理
- 字典管理、参数配置
- 操作日志、系统监控

### 2. 业务数据管理
- 订单管理、商品管理
- 客户信息、供应商管理
- 财务数据、报表管理

### 3. 内容管理
- 文章管理、分类管理
- 标签管理、评论管理
- 媒体文件管理

## 设计特点

### 1. 组件化设计
- 表单操作独立为 Form 组件
- 分页组件复用
- 工具栏组件集成

### 2. Hook 集成
- 使用 `useTable` Hook 简化表格操作
- 统一的数据加载和状态管理
- 简化的 API 调用逻辑

### 3. 用户体验优化
- 加载状态显示
- 搜索条件可折叠
- 批量操作支持
- 导出功能集成

### 4. 高度可配置
- 基于字段配置自动生成界面
- 支持多种数据类型和控件
- 灵活的权限控制

## 使用说明

### 1. 模板配置
```velocity
## 在代码生成器中配置
- 设置模块名称和业务名称
- 配置字段属性（查询、列表、HTML类型等）
- 设置字典类型和权限标识
```

### 2. 字段配置
```velocity
## 查询字段配置
$column.query = true          # 是否用于查询
$column.htmlType = "input"    # 控件类型
$column.queryType = "BETWEEN" # 查询类型

## 列表字段配置
$column.list = true           # 是否在列表显示
$column.dictType = "sys_yes_no" # 字典类型
```

### 3. API 集成
```javascript
// 需要提供的 API 方法
import { 
  listUser,      // 查询列表
  batchDelUser   // 批量删除
} from "@/api/system/user";
```

## Vue 3 特性应用

### 1. Composition API
```javascript
// 响应式数据
const showSearch = ref(true);
const queryParams = ref({});

// 组合式函数
const { tableObject, tableMethods } = useTable({});
```

### 2. 模板语法
```vue
<!-- 插槽语法 -->
<template #default="scope">
  <span>{{ scope.row.fieldName }}</span>
</template>

<!-- v-model 语法糖 -->
<pagination v-model:page="tableObject.currentPage" />
```

### 3. 组件通信
```javascript
// 子组件事件监听
<Form ref="formRef" @success="submitSuccess"></Form>

// 方法调用
formRef.value.open('添加');
```

## 最佳实践

### 1. 性能优化
- 合理使用 `v-show` 控制搜索表单显示
- 表格数据懒加载和分页
- 避免不必要的响应式数据

### 2. 用户体验
- 提供清晰的加载状态
- 合理的默认值设置
- 友好的错误提示

### 3. 代码维护
- 保持组件职责单一
- 合理抽取公共逻辑
- 统一的命名规范

### 4. 数据安全
- 严格的权限控制
- 输入数据验证
- 安全的 API 调用

## 扩展功能

### 1. 高级搜索
- 多条件组合查询
- 自定义查询条件
- 查询条件保存

### 2. 表格增强
- 列排序和筛选
- 列宽调整
- 表格数据导入

### 3. 批量操作
- 批量编辑
- 批量状态更新
- 批量数据处理

### 4. 数据可视化
- 图表展示
- 统计信息
- 数据分析

## 注意事项

### 1. 依赖要求
- Vue 3.x
- Element Plus
- 项目中的 Hook 和工具函数

### 2. API 接口要求
- 列表查询接口：支持分页和条件查询
- 删除接口：支持单个和批量删除
- 导出接口：支持条件导出

### 3. 权限配置
- 确保权限标识与后端一致
- 合理设置按钮权限
- 考虑数据权限控制

### 4. 字典数据
- 确保字典类型正确配置
- 字典数据及时更新
- 处理字典加载异常

## 依赖组件

- **Form**: 表单组件（同目录下的 Form.vue）
- **pagination**: 分页组件
- **right-toolbar**: 右侧工具栏组件
- **image-preview**: 图片预览组件
- **dict-tag**: 字典标签组件
- **useTable**: 表格操作 Hook
- **useDict**: 字典数据 Hook

该模板为 Vue 3 项目提供了标准化的列表页面解决方案，通过配置化的方式大大提高了开发效率，同时保持了良好的可维护性和扩展性。