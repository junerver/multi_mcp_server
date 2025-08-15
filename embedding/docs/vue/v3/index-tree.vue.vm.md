# index-tree.vue.vm 模板说明文档（Vue 3 版本）

## 模板功能

`index-tree.vue.vm` 是一个 Vue 3 模板文件，用于生成具有树形结构的完整管理页面。该模板采用 Vue 3 的 Composition API 和 `<script setup>` 语法，专门用于处理具有层级关系的数据管理，如组织架构、菜单管理、分类管理等场景。

## 主要特性

### 1. Vue 3 Composition API
- 使用 `<script setup>` 语法
- 采用 Composition API 编程模式
- 响应式数据管理（ref、reactive）
- 现代化的 Vue 3 开发方式

### 2. 树形数据管理
- 支持树形表格展示
- 可展开/折叠树节点
- 支持全部展开/折叠操作
- 树形数据结构转换
- 父子节点关系管理

### 3. 完整的 CRUD 功能
- 查询：支持条件查询和树形展示
- 新增：支持指定父节点的新增操作
- 修改：支持树节点的修改
- 删除：支持树节点的删除
- 权限控制：集成权限验证

### 4. 动态搜索表单
- 根据字段配置动态生成搜索条件
- 支持多种输入类型：输入框、选择器、单选框、日期选择器
- 支持日期范围查询
- 搜索和重置功能

### 5. 树形选择器
- 集成 Element Plus 的 el-tree-select 组件
- 支持父子节点选择
- 用于新增/修改时选择父节点
- 支持严格模式选择

### 6. 表单验证
- 动态生成表单验证规则
- 支持必填字段验证
- 不同控件类型的验证触发方式

## 模板变量

### 核心变量
- `${BusinessName}`: 业务实体名称（首字母大写）
- `${businessName}`: 业务实体名称（首字母小写）
- `${moduleName}`: 模块名称
- `${functionName}`: 功能名称
- `${treeCode}`: 树节点ID字段
- `${treeParentCode}`: 树父节点ID字段
- `${treeName}`: 树节点名称字段
- `${pkColumn}`: 主键列信息

### 字段属性
- `${columns}`: 所有字段列表
- `${column.javaField}`: Java字段名
- `${column.columnComment}`: 字段注释
- `${column.htmlType}`: HTML控件类型
- `${column.required}`: 是否必填
- `${column.query}`: 是否查询字段
- `${column.queryType}`: 查询类型
- `${column.list}`: 是否列表显示
- `${column.insert}`: 是否插入字段
- `${column.pk}`: 是否主键
- `${column.usableColumn}`: 是否可用字段
- `${column.superColumn}`: 是否超级字段
- `${column.dictType}`: 字典类型
- `${column.javaType}`: Java数据类型

### 字典变量
- `${dicts}`: 字典类型列表
- `${dictsNoSymbol}`: 去除符号的字典列表
- `${dictType}`: 具体字典类型

## 支持的控件类型

### 1. 查询表单控件
- **input**: 文本输入框
- **select**: 下拉选择框
- **radio**: 单选按钮组
- **datetime**: 日期选择器（支持范围查询）

### 2. 表格显示控件
- **datetime**: 日期格式化显示
- **imageUpload**: 图片预览
- **dictType**: 字典标签显示
- **checkbox**: 复选框标签显示

### 3. 表单编辑控件
- **input**: 文本输入框
- **textarea**: 多行文本输入
- **select**: 下拉选择框
- **radio**: 单选按钮组
- **checkbox**: 复选框组
- **datetime**: 日期选择器
- **imageUpload**: 图片上传
- **fileUpload**: 文件上传
- **editor**: 富文本编辑器
- **tree-select**: 树形选择器（用于父节点选择）

## 生成示例

假设配置如下：
- BusinessName: "SysMenu"
- businessName: "sysMenu"
- functionName: "菜单管理"
- treeCode: "menuId"
- treeParentCode: "parentId"
- treeName: "menuName"

生成的页面将包含：
1. 菜单搜索表单
2. 新增、展开/折叠操作按钮
3. 菜单树形表格展示
4. 菜单的增删改查功能
5. 新增/修改菜单对话框
6. 父菜单选择器

## 使用场景

### 1. 系统管理
- 菜单管理系统
- 权限管理系统
- 角色层级管理
- 用户组织架构

### 2. 内容管理
- 文章分类管理
- 商品分类管理
- 资源分类管理
- 标签层级管理

### 3. 地理信息
- 行政区划管理
- 地区层级管理
- 位置分类管理

### 4. 业务分类
- 部门层级管理
- 业务分类管理
- 流程节点管理

## 设计特点

### 1. 现代化架构
- Vue 3 Composition API
- `<script setup>` 语法
- 响应式数据管理
- 更好的 TypeScript 支持

### 2. 树形结构优化
- 高效的树形数据处理
- 支持大量节点的展示
- 优化的展开/折叠性能
- 智能的父子关系处理

### 3. 用户体验优化
- 直观的树形展示
- 便捷的节点操作
- 友好的交互反馈
- 响应式设计

### 4. 开发效率
- 模板化生成
- 标准化的代码结构
- 易于维护和扩展
- 高度可配置

## 使用说明

### 1. 模板配置
```velocity
## 配置树形字段
#set($treeCode = "id")
#set($treeParentCode = "parentId")
#set($treeName = "name")

## 配置业务信息
#set($BusinessName = "SysMenu")
#set($businessName = "sysMenu")
#set($functionName = "菜单管理")
```

### 2. 字段配置
- 设置字段的 htmlType（input、select、radio、datetime等）
- 配置查询字段和查询类型
- 设置列表显示字段
- 配置字典类型和验证规则

### 3. API 集成
- 确保后端提供对应的 API 接口
- 接口需要支持树形数据返回
- 支持父子关系的数据操作

### 4. 权限配置
```javascript
// 权限验证指令
v-hasPermi="['${moduleName}:${businessName}:add']"
v-hasPermi="['${moduleName}:${businessName}:edit']"
v-hasPermi="['${moduleName}:${businessName}:remove']"
```

## Vue 3 特性应用

### 1. Composition API
```javascript
// 响应式数据
const ${businessName}List = ref([])
const loading = ref(true)
const open = ref(false)

// 响应式对象
const data = reactive({
  form: {},
  queryParams: {},
  rules: {}
})

// 解构响应式对象
const { queryParams, form, rules } = toRefs(data)
```

### 2. 生命周期
```javascript
// 组件挂载后执行
getList()
```

### 3. 计算属性和监听器
```javascript
// 可以添加计算属性
const computedProperty = computed(() => {
  // 计算逻辑
})

// 可以添加监听器
watch(someRef, (newValue, oldValue) => {
  // 监听逻辑
})
```

## 最佳实践

### 1. 树形设计
- 合理设计树的深度，避免过深的层级
- 考虑节点数量，大量节点时使用懒加载
- 设计清晰的父子关系字段
- 避免循环引用

### 2. 性能优化
- 使用虚拟滚动处理大量节点
- 实现节点的懒加载
- 优化树形数据的查询和更新
- 合理使用 ref 和 reactive

### 3. 用户体验
- 提供节点搜索功能
- 支持拖拽排序（如需要）
- 清晰的节点状态标识
- 加载状态提示

### 4. 数据安全
- 验证节点的父子关系
- 防止循环引用
- 权限控制节点操作
- 数据验证和清理

## 扩展功能

### 1. 拖拽排序
```javascript
// 添加拖拽功能
const handleDragEnd = (draggingNode, dropNode, dropType) => {
  // 处理节点拖拽逻辑
}
```

### 2. 批量操作
```javascript
// 批量删除节点
const handleBatchDelete = () => {
  // 批量删除选中节点
}
```

### 3. 节点图标
```vue
<template>
  <!-- 添加节点图标 -->
  <el-table-column label="名称" prop="name">
    <template #default="scope">
      <i :class="scope.row.icon"></i>
      <span>{{ scope.row.name }}</span>
    </template>
  </el-table-column>
</template>
```

### 4. 右键菜单
```javascript
// 添加右键菜单
const handleNodeContextmenu = (event, data) => {
  // 显示右键菜单
}
```

### 5. 节点搜索
```javascript
// 树节点搜索
const searchText = ref('')
const filterNode = (value, data) => {
  if (!value) return true
  return data.name.indexOf(value) !== -1
}
```

## 注意事项

1. **Vue 3 兼容性**：确保项目使用 Vue 3 版本
2. **Element Plus**：确保使用 Element Plus 而不是 Element UI
3. **数据结构**：确保后端返回的数据包含正确的父子关系字段
4. **性能考虑**：大量节点时考虑分页或懒加载
5. **循环引用**：防止父子关系形成循环
6. **权限控制**：根据用户权限控制节点的操作权限
7. **数据一致性**：确保树形结构的数据一致性
8. **响应式数据**：正确使用 ref 和 reactive

## 依赖组件

- **Element Plus**: Vue 3 版本的 UI 组件库
- **el-tree-select**: 树形选择器组件
- **image-preview**: 图片预览组件
- **dict-tag**: 字典标签组件
- **image-upload**: 图片上传组件
- **file-upload**: 文件上传组件
- **editor**: 富文本编辑器组件
- **right-toolbar**: 右侧工具栏组件

## API 接口要求

```javascript
// 必需的 API 接口
list${BusinessName}(params)    // 查询列表
get${BusinessName}(id)         // 获取详情
add${BusinessName}(data)       // 新增数据
update${BusinessName}(data)    // 更新数据
del${BusinessName}(id)         // 删除数据
```

该模板为 Vue 3 项目提供了完整的树形数据管理解决方案，结合了现代化的开发模式和优秀的用户体验，是企业级应用中处理树形结构数据的理想选择。