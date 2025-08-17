# Form.vue.vm 模板说明文档

## 模板功能

`Form.vue.vm` 是一个 Vue 3 模板文件，专门用于生成表单组件。该模板采用 Vue 3 的 Composition API 和 `<script setup>` 语法，生成可复用的表单对话框组件，用于数据的新增和修改操作。

## 主要特性

### 1. Vue 3 Composition API
- 使用 `<script setup>` 语法
- 采用 Composition API 编程模式
- 支持 TypeScript（可选）
- 现代化的 Vue 3 开发方式

### 2. 对话框表单
- 封装为独立的表单组件
- 支持新增和修改两种模式
- 模态对话框展示
- 可通过 `open` 方法调用

### 3. 动态表单生成
- 根据字段配置动态生成表单项
- 支持多种输入控件类型
- 自动处理表单验证
- 支持字典数据绑定

### 4. 主子表支持
- 支持主表和子表的联合编辑
- 子表数据的增删操作
- 表格形式的子表数据展示
- 子表数据的批量选择

### 5. 表单验证
- 动态生成验证规则
- 支持必填字段验证
- 不同控件类型的验证触发
- 实时表单校验

## 模板变量

### 核心变量
- `${BusinessName}`: 业务实体名称（首字母大写）
- `${businessName}`: 业务实体名称（首字母小写）
- `${moduleName}`: 模块名称
- `${functionName}`: 功能名称
- `${dicts}`: 字典类型列表
- `${dictsNoSymbol}`: 去除符号的字典列表

### 字段属性
- `${columns}`: 所有字段列表
- `${column.javaField}`: Java字段名
- `${column.columnComment}`: 字段注释
- `${column.htmlType}`: HTML控件类型
- `${column.required}`: 是否必填
- `${column.insert}`: 是否插入字段
- `${column.pk}`: 是否主键
- `${column.usableColumn}`: 是否可用字段
- `${column.superColumn}`: 是否超级字段
- `${column.dictType}`: 字典类型
- `${column.javaType}`: Java数据类型

### 子表变量
- `${table.sub}`: 是否有子表
- `${subTable}`: 子表信息
- `${subClassName}`: 子表类名
- `${subclassName}`: 子表类名（首字母小写）
- `${subTableFkclassName}`: 子表外键字段名

## 支持的控件类型

### 1. 基础输入控件
- **input**: 文本输入框
- **textarea**: 多行文本输入
- **datetime**: 日期选择器

### 2. 选择控件
- **select**: 下拉选择框
- **radio**: 单选按钮组
- **checkbox**: 复选框组

### 3. 文件上传控件
- **imageUpload**: 图片上传
- **fileUpload**: 文件上传

### 4. 富文本控件
- **editor**: 富文本编辑器

## 生成示例

假设配置如下：
- BusinessName: "SysUser"
- businessName: "sysUser"
- functionName: "用户管理"
- 字段包含：用户名、邮箱、手机号、状态等

生成的组件将包含：
```vue
<template>
  <Dialog :title="dialogTitle" v-model="dialogVisible">
    <el-form ref="formRef" :model="form" :rules="formRules">
      <el-form-item label="用户名" prop="userName">
        <el-input v-model="form.userName" placeholder="请输入用户名" />
      </el-form-item>
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="form.email" placeholder="请输入邮箱" />
      </el-form-item>
      <!-- 更多表单项 -->
    </el-form>
  </Dialog>
</template>
```

## 使用场景

### 1. 数据管理页面
- 用户管理的新增/编辑
- 角色管理的配置
- 权限设置的修改

### 2. 业务数据录入
- 订单信息录入
- 商品信息管理
- 客户资料维护

### 3. 系统配置
- 参数配置管理
- 字典数据维护
- 菜单配置编辑

### 4. 主子表数据
- 订单及订单明细
- 用户及用户角色
- 文章及文章标签

## 设计特点

### 1. 组件化设计
- 独立的表单组件
- 可复用的设计模式
- 清晰的组件接口
- 事件驱动的交互

### 2. 现代化开发
- Vue 3 Composition API
- `<script setup>` 语法
- 响应式数据管理
- 更好的 TypeScript 支持

### 3. 用户体验优化
- 加载状态提示
- 表单验证反馈
- 操作成功提示
- 错误处理机制

### 4. 高度可配置
- 灵活的字段配置
- 多样的控件类型
- 可定制的验证规则
- 支持字典数据

## 使用说明

### 1. 组件调用
```javascript
// 在父组件中使用
const formRef = ref()

// 新增操作
const handleAdd = () => {
  formRef.value.open('新增')
}

// 编辑操作
const handleEdit = (id) => {
  formRef.value.open('编辑', id)
}
```

### 2. 事件监听
```vue
<template>
  <UserForm ref="formRef" @success="handleSuccess" />
</template>

<script setup>
const handleSuccess = () => {
  // 表单提交成功后的处理
  getList() // 刷新列表
}
</script>
```

### 3. 字段配置
```velocity
## 配置字段属性
#foreach($column in $columns)
  #if($column.insert && !$column.pk)
    ## 生成对应的表单项
  #end
#end
```

## 最佳实践

### 1. 表单设计
- 合理安排表单字段顺序
- 使用适当的控件类型
- 设置清晰的字段标签
- 提供有用的占位符文本

### 2. 验证规则
- 设置必要的必填验证
- 添加格式验证（邮箱、手机号等）
- 使用合适的验证触发时机
- 提供清晰的错误提示

### 3. 性能优化
- 合理使用 v-model
- 避免不必要的响应式数据
- 优化大表单的渲染性能
- 使用懒加载处理大量选项

### 4. 用户体验
- 提供加载状态反馈
- 实现表单数据的自动保存
- 支持键盘快捷键操作
- 优化移动端的表单体验

## 扩展功能

### 1. 表单步骤
```vue
<template>
  <el-steps :active="currentStep">
    <el-step title="基本信息" />
    <el-step title="详细信息" />
    <el-step title="确认提交" />
  </el-steps>
</template>
```

### 2. 动态表单
```javascript
// 根据条件动态显示字段
const showAdvanced = ref(false)
const toggleAdvanced = () => {
  showAdvanced.value = !showAdvanced.value
}
```

### 3. 表单联动
```javascript
// 字段联动逻辑
watch(() => form.value.type, (newType) => {
  // 根据类型改变其他字段的选项
  updateRelatedFields(newType)
})
```

### 4. 自定义验证
```javascript
const customValidator = (rule, value, callback) => {
  // 自定义验证逻辑
  if (!value) {
    callback(new Error('请输入内容'))
  } else {
    callback()
  }
}
```

## 主子表操作

### 1. 子表数据管理
```javascript
// 添加子表行
const handleAddSubRow = () => {
  subTableList.value.push({
    // 默认数据
  })
}

// 删除子表行
const handleDeleteSubRow = () => {
  const selections = subTableRef.value.getSelectionRows()
  // 删除选中行
}
```

### 2. 子表验证
```javascript
// 子表数据验证
const validateSubTable = () => {
  return subTableList.value.every(row => {
    // 验证每行数据
    return row.required_field && row.required_field.trim()
  })
}
```

## 注意事项

1. **Vue 3 兼容性**：确保项目使用 Vue 3 版本
2. **组件依赖**：确保引入了必要的 UI 组件库
3. **API 接口**：确保后端提供对应的增删改查接口
4. **字典数据**：确保字典数据的正确加载和使用
5. **表单验证**：合理设置验证规则，避免过度验证
6. **性能考虑**：大表单时注意性能优化

## 依赖组件

- **Element Plus**: Vue 3 版本的 UI 组件库
- **Dialog**: 自定义对话框组件
- **image-upload**: 图片上传组件
- **file-upload**: 文件上传组件
- **editor**: 富文本编辑器组件

该模板为 Vue 3 项目提供了现代化的表单解决方案，支持复杂的表单操作和数据管理，是企业级应用中处理表单数据的理想选择。