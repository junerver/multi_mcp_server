# index.vue.vm 模板说明文档

## 模板功能

`index.vue.vm` 是一个用于生成Vue.js前端页面的Velocity模板，主要用于创建完整的CRUD（增删改查）管理页面。该模板生成的页面包含数据列表展示、搜索过滤、新增/编辑表单、删除操作、分页功能以及数据导出等完整的业务管理功能。

## 主要特性

### 1. 基础结构
- **Vue单文件组件**：采用标准的Vue.js单文件组件结构（template + script）
- **Element UI集成**：使用Element UI组件库构建用户界面
- **响应式设计**：支持不同屏幕尺寸的自适应布局
- **模块化设计**：清晰的组件结构和方法组织

### 2. 搜索功能
- **动态搜索表单**：根据字段配置自动生成搜索条件
- **多种输入类型**：支持文本输入、下拉选择、单选按钮、日期时间选择等
- **日期范围查询**：支持开始时间和结束时间的范围查询
- **字典数据支持**：集成系统字典数据进行选项展示

### 3. 数据列表
- **动态表格列**：根据字段配置自动生成表格列
- **数据类型处理**：支持日期时间格式化、图片显示、字典值转换等
- **操作按钮**：提供编辑、删除等行级操作
- **批量操作**：支持多选和批量删除功能
- **分页控制**：集成分页组件进行数据分页展示

### 4. 表单操作
- **新增/编辑表单**：统一的弹窗表单用于数据新增和编辑
- **动态表单项**：根据字段类型自动生成相应的表单控件
- **表单验证**：集成表单验证规则，确保数据完整性
- **文件上传**：支持图片和文件上传功能
- **富文本编辑**：支持富文本编辑器集成

### 5. 主子表支持
- **主子表关联**：支持一对多的主子表数据管理
- **子表操作**：提供子表数据的增删改查功能
- **数据联动**：主表和子表数据的联动更新

## 模板变量

### 核心变量
- `$functionName`：功能名称（中文）
- `$BusinessName`：业务名称（首字母大写）
- `$businessName`：业务名称（首字母小写）
- `$moduleName`：模块名称
- `$pkColumn`：主键字段信息
- `$columns`：字段列表
- `$table`：表信息对象

### 字段属性
- `$column.javaField`：Java字段名
- `$column.columnComment`：字段注释
- `$column.htmlType`：HTML控件类型
- `$column.queryType`：查询类型
- `$column.required`：是否必填
- `$column.list`：是否在列表显示
- `$column.query`：是否用于查询
- `$column.insert`：是否用于新增
- `$column.edit`：是否用于编辑
- `$column.dictType`：字典类型

### 主子表变量
- `$subTable`：子表信息
- `$subclassName`：子表类名（首字母小写）
- `$subClassName`：子表类名（首字母大写）
- `$subTableFkclassName`：子表外键字段名

## 生成示例

假设有一个用户管理模块，模板会生成如下Vue组件：

```vue
<template>
  <div class="app-container">
    <!-- 搜索表单 -->
    <el-form :model="queryParams" ref="queryForm" size="small" :inline="true">
      <el-form-item label="用户名" prop="userName">
        <el-input v-model="queryParams.userName" placeholder="请输入用户名" clearable />
      </el-form-item>
      <el-form-item label="状态" prop="status">
        <el-select v-model="queryParams.status" placeholder="请选择状态" clearable>
          <el-option label="正常" value="0" />
          <el-option label="停用" value="1" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" @click="handleQuery">搜索</el-button>
        <el-button icon="el-icon-refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- 操作按钮 -->
    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button type="primary" @click="handleAdd">新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="danger" @click="handleDelete">删除</el-button>
      </el-col>
    </el-row>

    <!-- 数据表格 -->
    <el-table v-loading="loading" :data="userList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="用户名" prop="userName" />
      <el-table-column label="状态" prop="status">
        <template slot-scope="scope">
          <dict-tag :options="sys_normal_disable" :value="scope.row.status"/>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center">
        <template slot-scope="scope">
          <el-button size="mini" type="text" @click="handleUpdate(scope.row)">修改</el-button>
          <el-button size="mini" type="text" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <pagination v-show="total>0" :total="total" :page.sync="queryParams.pageNum" :limit.sync="queryParams.pageSize" @pagination="getList" />

    <!-- 添加或修改对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="500px">
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="用户名" prop="userName">
          <el-input v-model="form.userName" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio label="0">正常</el-radio>
            <el-radio label="1">停用</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { listUser, getUser, delUser, addUser, updateUser } from "@/api/system/user";

export default {
  name: "User",
  dicts: ['sys_normal_disable'],
  data() {
    return {
      loading: true,
      userList: [],
      total: 0,
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        userName: null,
        status: null
      },
      form: {},
      rules: {
        userName: [
          { required: true, message: "用户名不能为空", trigger: "blur" }
        ]
      }
    };
  },
  created() {
    this.getList();
  },
  methods: {
    getList() {
      this.loading = true;
      listUser(this.queryParams).then(response => {
        this.userList = response.data.rows;
        this.total = response.data.total;
        this.loading = false;
      });
    },
    handleAdd() {
      this.reset();
      this.open = true;
      this.title = "添加用户";
    },
    handleUpdate(row) {
      this.reset();
      const userId = row.userId || this.ids;
      getUser(userId).then(response => {
        this.form = response.data;
        this.open = true;
        this.title = "修改用户";
      });
    },
    submitForm() {
      this.$refs["form"].validate(valid => {
        if (valid) {
          if (this.form.userId != null) {
            updateUser(this.form).then(response => {
              this.$modal.msgSuccess("修改成功");
              this.open = false;
              this.getList();
            });
          } else {
            addUser(this.form).then(response => {
              this.$modal.msgSuccess("新增成功");
              this.open = false;
              this.getList();
            });
          }
        }
      });
    }
  }
};
</script>
```

## 使用场景

### 1. 业务管理页面
- **用户管理**：用户信息的增删改查
- **角色管理**：系统角色的配置管理
- **菜单管理**：系统菜单的层级管理
- **字典管理**：系统字典数据维护

### 2. 数据维护页面
- **基础数据**：各类基础数据的维护
- **配置管理**：系统配置参数管理
- **日志查询**：系统日志的查询展示

### 3. 业务流程页面
- **订单管理**：订单信息的处理流程
- **审批流程**：各类审批业务的处理
- **工作流管理**：业务流程的配置和执行

## 设计特点

### 1. 高度可配置
- **字段驱动**：通过字段配置自动生成页面结构
- **类型适配**：根据字段类型自动选择合适的UI组件
- **权限控制**：集成权限验证，控制功能访问

### 2. 用户体验优化
- **加载状态**：提供数据加载的视觉反馈
- **操作反馈**：操作成功/失败的消息提示
- **表单验证**：实时的表单验证和错误提示
- **响应式布局**：适配不同设备的屏幕尺寸

### 3. 开发效率
- **代码复用**：统一的页面结构和交互模式
- **快速生成**：通过模板快速生成标准化页面
- **易于维护**：清晰的代码结构和注释

## 使用说明

### 1. 模板配置
```velocity
## 设置基本信息
#set($functionName = "用户管理")
#set($BusinessName = "User")
#set($businessName = "user")
#set($moduleName = "system")

## 配置字段信息
#set($columns = [...])
#set($pkColumn = {...})
```

### 2. 字段配置示例
```velocity
## 文本输入字段
{
  "javaField": "userName",
  "columnComment": "用户名",
  "htmlType": "input",
  "required": true,
  "list": true,
  "query": true,
  "insert": true,
  "edit": true
}

## 下拉选择字段
{
  "javaField": "status",
  "columnComment": "状态",
  "htmlType": "select",
  "dictType": "sys_normal_disable",
  "required": true,
  "list": true,
  "query": true,
  "insert": true,
  "edit": true
}
```

### 3. API集成
```javascript
// 导入API方法
import { listUser, getUser, delUser, addUser, updateUser } from "@/api/system/user";

// 在methods中调用
listUser(this.queryParams).then(response => {
  this.userList = response.data.rows;
  this.total = response.data.total;
});
```

## 最佳实践

### 1. 字段设计
- **合理分组**：将相关字段进行逻辑分组
- **类型选择**：根据数据特点选择合适的HTML类型
- **验证规则**：设置必要的字段验证规则
- **显示控制**：合理配置字段的显示和操作权限

### 2. 性能优化
- **分页加载**：大数据量时使用分页减少加载时间
- **懒加载**：对于复杂组件使用懒加载策略
- **缓存策略**：合理使用缓存减少重复请求
- **防抖处理**：搜索输入使用防抖避免频繁请求

### 3. 用户体验
- **加载提示**：提供明确的加载状态提示
- **操作确认**：重要操作提供确认对话框
- **错误处理**：友好的错误信息展示
- **快捷操作**：提供键盘快捷键支持

### 4. 代码维护
- **组件拆分**：复杂页面进行组件拆分
- **方法复用**：提取公共方法避免代码重复
- **注释完善**：添加必要的代码注释
- **规范统一**：遵循项目的编码规范

## 扩展功能

### 1. 高级搜索
- **多条件组合**：支持复杂的搜索条件组合
- **保存搜索**：保存常用的搜索条件
- **搜索历史**：记录搜索历史便于重复使用

### 2. 数据导入导出
- **Excel导入**：支持Excel文件的数据导入
- **模板下载**：提供导入模板下载
- **批量操作**：支持批量数据处理

### 3. 个性化设置
- **列显示控制**：用户可自定义显示的列
- **排序设置**：支持多列排序
- **页面布局**：可调整的页面布局

### 4. 数据可视化
- **图表展示**：集成图表组件展示数据
- **统计信息**：显示数据统计信息
- **趋势分析**：数据趋势的可视化分析

## 原始模板内容

模板文件位置：`d:\dev\framework\jkr-framework-server\jkr-server\src\main\resources\vm\vue\index.vue.vm`

该模板使用Velocity模板引擎语法，通过变量替换和条件判断生成完整的Vue.js页面代码。模板包含完整的CRUD功能实现，支持多种字段类型和主子表关联，是一个功能完善的前端页面生成模板。