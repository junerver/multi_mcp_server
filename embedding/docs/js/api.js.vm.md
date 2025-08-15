# 前端API接口模板 (api.js.vm)

## 模板功能说明

这个模板用于生成前端JavaScript API接口文件，为Vue.js应用提供与后端REST API通信的标准化接口方法。生成的API文件包含完整的CRUD操作方法，使用axios进行HTTP请求，遵循RESTful API设计规范。

## 主要特性

### 1. 基础结构
- **模块导入**: 导入统一的request工具模块
- **函数导出**: 导出标准的API接口函数
- **命名规范**: 遵循驼峰命名和业务语义化命名
- **注释完整**: 每个函数都有清晰的中文注释说明

### 2. 标准CRUD操作
- **列表查询**: `list${BusinessName}` - 支持条件查询和分页
- **详情查询**: `get${BusinessName}` - 根据主键获取单条记录
- **新增数据**: `add${BusinessName}` - 创建新记录
- **修改数据**: `update${BusinessName}` - 更新现有记录
- **单条删除**: `del${BusinessName}` - 删除单条记录
- **批量删除**: `batchDel${BusinessName}` - 批量删除多条记录

### 3. HTTP方法映射
- **GET请求**: 用于查询操作（列表、详情）
- **POST请求**: 用于数据变更操作（增删改）
- **参数传递**: 查询参数使用params，数据提交使用data
- **URL构建**: 支持路径参数和查询参数

### 4. 请求配置
- **统一基础URL**: 使用模块名和业务名构建API路径
- **标准化响应**: 统一的响应数据格式处理
- **错误处理**: 依赖request工具的统一错误处理
- **拦截器支持**: 支持请求和响应拦截器

## 模板变量说明

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `${functionName}` | 功能名称（中文） | `用户信息` |
| `${BusinessName}` | 业务名称（首字母大写） | `SysUser` |
| `${moduleName}` | 模块名称（小写） | `system` |
| `${businessName}` | 业务名称（小写） | `user` |
| `${pkColumn.javaField}` | 主键字段名 | `userId` |

## API接口设计规范

### 1. URL路径规范
```javascript
// 基础路径格式
/${moduleName}/${businessName}/action

// 具体示例
/system/user/list          // 列表查询
/system/user/info/{id}     // 详情查询
/system/user/add           // 新增数据
/system/user/edit          // 修改数据
/system/user/remove/{id}   // 单条删除
/system/user/batchRemove   // 批量删除
```

### 2. 请求方法规范
- **查询操作**: 使用GET方法，参数通过query string传递
- **数据操作**: 使用POST方法，数据通过request body传递
- **路径参数**: 直接拼接在URL路径中
- **批量操作**: 数据通过request body以数组形式传递

### 3. 参数传递规范
```javascript
// 查询参数（GET请求）
params: {
    pageNum: 1,
    pageSize: 10,
    userName: 'admin'
}

// 数据参数（POST请求）
data: {
    userName: 'newuser',
    email: 'user@example.com',
    status: '0'
}

// 批量删除参数
data: [1, 2, 3, 4, 5]  // 主键ID数组
```

## 生成示例

```javascript
import request from '@/utils/request'

// 查询用户信息列表
export function listSysUser(query) {
    return request({
        url: '/system/user/list',
        method: 'get',
        params: query
    })
}

// 查询用户信息详细
export function getSysUser(userId) {
    return request({
        url: '/system/user/info/' + userId,
        method: 'get'
    })
}

// 新增用户信息
export function addSysUser(data) {
    return request({
        url: '/system/user/add',
        method: 'post',
        data: data
    })
}

// 修改用户信息
export function updateSysUser(data) {
    return request({
        url: '/system/user/edit',
        method: 'post',
        data: data
    })
}

// 删除用户信息
export function delSysUser(userId) {
    return request({
        url: '/system/user/remove/' + userId,
        method: 'post'
    })
}

// 批量删除用户信息
export function batchDelSysUser(data) {
    return request({
        url: '/system/user/batchRemove',
        method: 'post',
        data: data
    })
}
```

## 原始模板内容

```velocity
import request from '@/utils/request'

// 查询${functionName}列表
export function list${BusinessName}(query) {
    return request({
        url: '/${moduleName}/${businessName}/list',
        method: 'get',
        params: query
    })
}

// 查询${functionName}详细
export function get${BusinessName}(${pkColumn.javaField}) {
    return request({
        url: '/${moduleName}/${businessName}/info/' + ${pkColumn.javaField},
        method: 'get'
    })
}

// 新增${functionName}
export function add${BusinessName}(data) {
    return request({
        url: '/${moduleName}/${businessName}/add',
        method: 'post',
        data: data
    })
}

// 修改${functionName}
export function update${BusinessName}(data) {
    return request({
        url: '/${moduleName}/${businessName}/edit',
        method: 'post',
        data: data
    })
}

// 删除${functionName}
export function del${BusinessName}(${pkColumn.javaField}) {
    return request({
        url: '/${moduleName}/${businessName}/remove/' + ${pkColumn.javaField},
        method: 'post'
    })
}

// 批量删除${functionName}
export function batchDel${BusinessName}(data) {
    return request({
        url: '/${moduleName}/${businessName}/batchRemove',
        method: 'post',
        data: data
    })
}
```

## 使用场景

### 1. 前后端分离架构
- **API层抽象**: 为前端提供统一的API调用接口
- **数据交互**: 处理前端与后端的数据通信
- **状态管理**: 配合Vuex等状态管理工具使用
- **组件解耦**: 将API调用逻辑从组件中分离

### 2. 业务场景示例
- **用户管理**: 用户的增删改查操作
- **权限管理**: 角色、菜单的管理操作
- **系统配置**: 参数配置的管理操作
- **业务数据**: 各种业务实体的CRUD操作

### 3. 开发流程集成
- **代码生成**: 配合后端代码生成，自动生成对应的前端API
- **接口联调**: 前后端开发人员的接口联调基础
- **文档同步**: API接口与后端接口文档保持同步
- **版本管理**: 支持API版本化管理

## 设计特点

### 1. 标准化设计
- **统一规范**: 所有API接口遵循统一的命名和调用规范
- **RESTful风格**: 符合RESTful API设计原则
- **语义化命名**: 函数名称具有明确的业务语义
- **注释完整**: 每个接口都有清晰的中文注释

### 2. 可维护性
- **模块化设计**: 每个业务模块独立的API文件
- **统一入口**: 通过统一的request工具处理所有请求
- **配置集中**: 基础配置在request工具中统一管理
- **错误统一**: 统一的错误处理和响应格式

### 3. 扩展性
- **功能扩展**: 可以轻松添加新的API接口方法
- **参数扩展**: 支持添加更多的请求参数和配置
- **拦截器**: 支持请求和响应拦截器的扩展
- **中间件**: 可以集成各种HTTP中间件

## 使用说明

### 1. 导入使用
```javascript
// 在Vue组件中导入API方法
import { listSysUser, getSysUser, addSysUser } from '@/api/system/user'

// 在方法中调用API
export default {
    methods: {
        async loadUserList() {
            try {
                const response = await listSysUser(this.queryParams)
                this.userList = response.data.rows
                this.total = response.data.total
            } catch (error) {
                console.error('加载用户列表失败:', error)
            }
        }
    }
}
```

### 2. 参数配置
```javascript
// 查询参数示例
const queryParams = {
    pageNum: 1,
    pageSize: 10,
    userName: '',
    status: '',
    beginTime: '',
    endTime: ''
}

// 表单数据示例
const formData = {
    userName: 'admin',
    nickName: '管理员',
    email: 'admin@example.com',
    phonenumber: '13800138000',
    sex: '1',
    status: '0'
}
```

### 3. 错误处理
```javascript
// 统一错误处理
try {
    const response = await addSysUser(formData)
    if (response.code === 200) {
        this.$message.success('添加成功')
        this.loadUserList()
    }
} catch (error) {
    this.$message.error('添加失败: ' + error.message)
}
```

## 最佳实践

### 1. API组织
- **按模块分组**: 将相关的API接口放在同一个文件中
- **命名一致**: 保持API方法名与后端接口的一致性
- **文档同步**: 及时更新API接口文档
- **版本管理**: 对API接口进行版本化管理

### 2. 性能优化
- **请求缓存**: 对不经常变化的数据进行缓存
- **并发控制**: 避免重复请求和并发冲突
- **分页加载**: 大数据量使用分页加载
- **懒加载**: 按需加载API模块

### 3. 安全考虑
- **参数验证**: 在前端进行基础的参数验证
- **敏感数据**: 避免在URL中传递敏感信息
- **CSRF防护**: 配合后端的CSRF防护机制
- **权限控制**: 结合前端路由权限控制

### 4. 开发规范
- **代码风格**: 遵循团队的JavaScript代码规范
- **注释规范**: 为每个API方法添加清晰的注释
- **测试覆盖**: 为关键API接口编写单元测试
- **文档维护**: 及时更新API接口文档和使用说明

## 扩展功能

### 1. 高级查询
```javascript
// 导出功能
export function exportSysUser(query) {
    return request({
        url: '/system/user/export',
        method: 'get',
        params: query,
        responseType: 'blob'
    })
}

// 导入功能
export function importSysUser(data) {
    return request({
        url: '/system/user/import',
        method: 'post',
        data: data,
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
}
```

### 2. 状态管理集成
```javascript
// 与Vuex集成
export function fetchUserList(context, params) {
    return listSysUser(params).then(response => {
        context.commit('SET_USER_LIST', response.data)
        return response
    })
}
```

### 3. 缓存策略
```javascript
// 带缓存的API调用
const cache = new Map()

export function getCachedSysUser(userId) {
    const cacheKey = `user_${userId}`
    if (cache.has(cacheKey)) {
        return Promise.resolve(cache.get(cacheKey))
    }
    
    return getSysUser(userId).then(response => {
        cache.set(cacheKey, response)
        return response
    })
}
```