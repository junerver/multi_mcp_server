# mapper.xml.vm 模板说明文档

## 模板功能

`mapper.xml.vm` 是一个用于生成MyBatis Mapper XML配置文件的Velocity模板，主要用于创建数据访问层的SQL映射文件。该模板生成的XML文件包含完整的CRUD操作SQL语句、结果映射配置、动态查询条件以及主子表关联查询等功能，是MyBatis持久层框架的核心配置文件。

## 主要特性

### 1. 基础结构
- **标准XML格式**：符合MyBatis Mapper XML规范的标准格式
- **命名空间配置**：自动配置Mapper接口的命名空间
- **结果映射**：定义实体类与数据库字段的映射关系
- **SQL片段复用**：提取公共SQL片段便于复用

### 2. 结果映射配置
- **基础结果映射**：主表实体类的字段映射配置
- **扩展结果映射**：支持主子表关联的复合结果映射
- **集合映射**：支持一对多关系的集合属性映射
- **嵌套查询**：支持延迟加载的嵌套查询配置

### 3. 查询功能
- **列表查询**：支持分页和条件查询的列表查询
- **单条查询**：根据主键查询单条记录
- **动态条件**：支持多种查询条件类型（等于、不等于、大于、小于、模糊查询、范围查询等）
- **逻辑删除**：集成逻辑删除标识的查询过滤

### 4. 增删改操作
- **插入操作**：支持动态字段插入和主键自增
- **更新操作**：支持动态字段更新
- **删除操作**：提供物理删除和逻辑删除两种方式
- **批量操作**：支持批量删除和批量插入

### 5. 主子表支持
- **关联查询**：支持主子表的关联查询
- **子表操作**：提供子表数据的独立操作方法
- **批量处理**：支持子表数据的批量插入和删除
- **级联操作**：支持主子表的级联删除

## 模板变量

### 核心变量
- `$packageName`：包名
- `$ClassName`：类名（首字母大写）
- `$tableName`：主表名
- `$columns`：主表字段列表
- `$pkColumn`：主键字段信息

### 主子表变量
- `$table.sub`：是否包含子表
- `$subClassName`：子表类名（首字母大写）
- `$subclassName`：子表类名（首字母小写）
- `$subTable`：子表信息对象
- `$subTableName`：子表名
- `$subTableFkName`：子表外键字段名
- `$subTableFkClassName`：子表外键类名
- `$subTableFkclassName`：子表外键类名（首字母小写）

### 字段属性
- `$column.javaField`：Java字段名
- `$column.columnName`：数据库字段名
- `$column.javaType`：Java数据类型
- `$column.queryType`：查询类型
- `$column.query`：是否用于查询
- `$column.required`：是否必填

### 主键属性
- `$pkColumn.columnName`：主键字段名
- `$pkColumn.javaField`：主键Java字段名
- `$pkColumn.javaType`：主键Java类型
- `$pkColumn.capJavaField`：主键字段名（首字母大写）
- `$pkColumn.increment`：是否自增

## 生成示例

假设有一个用户管理模块，模板会生成如下Mapper XML：

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.jkr.system.mapper.UserMapper">

    <resultMap type="com.jkr.system.domain.User" id="UserResult">
        <result property="userId"    column="user_id"    />
        <result property="userName"    column="user_name"    />
        <result property="email"    column="email"    />
        <result property="status"    column="status"    />
        <result property="createTime"    column="create_time"    />
    </resultMap>

    <sql id="selectUserVo">
        select user_id, user_name, email, status, create_time from sys_user
    </sql>

    <select id="selectUserList" parameterType="com.jkr.system.domain.User" resultMap="UserResult">
        <include refid="selectUserVo"/>
        <where>
            <if test="userName != null and userName.trim() != ''"> and user_name like concat('%', #{userName}, '%')</if>
            <if test="email != null and email.trim() != ''"> and email = #{email}</if>
            <if test="status != null and status.trim() != ''"> and status = #{status}</if>
            <if test="params.beginCreateTime != null and params.beginCreateTime != '' and params.endCreateTime != null and params.endCreateTime != ''"> and create_time between #{params.beginCreateTime} and #{params.endCreateTime}</if>
            and del_flag = '1'
        </where>
    </select>

    <select id="selectUserByUserId" parameterType="Long" resultMap="UserResult">
        <include refid="selectUserVo"/>
        where user_id = #{userId}
    </select>

    <insert id="insertUser" parameterType="com.jkr.system.domain.User" useGeneratedKeys="true" keyProperty="userId">
        insert into sys_user
        <trim prefix="(" suffix=")" suffixOverrides=",">
            <if test="userName != null and userName != ''">user_name,</if>
            <if test="email != null">email,</if>
            <if test="status != null">status,</if>
            <if test="createTime != null">create_time,</if>
        </trim>
        <trim prefix="values (" suffix=")" suffixOverrides=",">
            <if test="userName != null and userName != ''">#{userName},</if>
            <if test="email != null">#{email},</if>
            <if test="status != null">#{status},</if>
            <if test="createTime != null">#{createTime},</if>
        </trim>
    </insert>

    <update id="updateUser" parameterType="com.jkr.system.domain.User">
        update sys_user
        <trim prefix="SET" suffixOverrides=",">
            <if test="userName != null and userName != ''">user_name = #{userName},</if>
            <if test="email != null">email = #{email},</if>
            <if test="status != null">status = #{status},</if>
            <if test="updateTime != null">update_time = #{updateTime},</if>
        </trim>
        where user_id = #{userId}
    </update>

    <update id="logicRemoveByUserIds" parameterType="String">
        update sys_user set del_flag = REPLACE(unix_timestamp(current_timestamp(3)),'.','') where user_id in
        <foreach item="userId" collection="list" open="(" separator="," close=")">
            #{userId}
        </foreach>
    </update>

    <update id="logicRemoveByUserId" parameterType="Long">
        update sys_user set del_flag = REPLACE(unix_timestamp(current_timestamp(3)),'.','') where user_id = #{userId}
    </update>

    <delete id="deleteUserByUserId" parameterType="Long">
        delete from sys_user where user_id = #{userId}
    </delete>

    <delete id="deleteUserByUserIds" parameterType="String">
        delete from sys_user where user_id in
        <foreach item="userId" collection="array" open="(" separator="," close=")">
            #{userId}
        </foreach>
    </delete>
</mapper>
```

## 查询条件类型

### 1. 等值查询（EQ）
```xml
<if test="status != null and status.trim() != ''"> and status = #{status}</if>
```

### 2. 不等值查询（NE）
```xml
<if test="status != null and status.trim() != ''"> and status != #{status}</if>
```

### 3. 大于查询（GT）
```xml
<if test="createTime != null"> and create_time &gt; #{createTime}</if>
```

### 4. 大于等于查询（GTE）
```xml
<if test="createTime != null"> and create_time &gt;= #{createTime}</if>
```

### 5. 小于查询（LT）
```xml
<if test="createTime != null"> and create_time &lt; #{createTime}</if>
```

### 6. 小于等于查询（LTE）
```xml
<if test="createTime != null"> and create_time &lt;= #{createTime}</if>
```

### 7. 模糊查询（LIKE）
```xml
<if test="userName != null and userName.trim() != ''"> and user_name like concat('%', #{userName}, '%')</if>
```

### 8. 范围查询（BETWEEN）
```xml
<if test="params.beginCreateTime != null and params.beginCreateTime != '' and params.endCreateTime != null and params.endCreateTime != ''"> and create_time between #{params.beginCreateTime} and #{params.endCreateTime}</if>
```

## 使用场景

### 1. 基础数据管理
- **用户管理**：用户信息的数据访问操作
- **角色管理**：系统角色的数据库操作
- **菜单管理**：系统菜单的层级数据处理
- **字典管理**：系统字典数据的维护操作

### 2. 业务数据处理
- **订单管理**：订单信息的复杂查询和更新
- **商品管理**：商品数据的分类和检索
- **客户管理**：客户信息的综合管理

### 3. 主子表业务
- **订单明细**：订单主表和明细子表的关联操作
- **产品配置**：产品主信息和配置明细的联合管理
- **组织架构**：部门和员工的层级关系处理

## 设计特点

### 1. 动态SQL支持
- **条件判断**：使用`<if>`标签进行条件判断
- **动态拼接**：使用`<trim>`标签进行SQL片段的动态拼接
- **循环处理**：使用`<foreach>`标签处理集合参数
- **SQL复用**：使用`<include>`标签复用SQL片段

### 2. 性能优化
- **索引友好**：生成的查询条件支持数据库索引优化
- **分页支持**：配合分页插件实现高效分页查询
- **延迟加载**：支持关联查询的延迟加载策略
- **批量操作**：提供批量插入和删除的高效实现

### 3. 数据安全
- **参数绑定**：使用预编译参数绑定防止SQL注入
- **逻辑删除**：支持逻辑删除保护重要数据
- **字段验证**：对必填字段进行空值检查
- **类型安全**：严格的参数类型定义

## 使用说明

### 1. 模板配置
```velocity
## 设置基本信息
#set($packageName = "com.jkr.system")
#set($ClassName = "User")
#set($tableName = "sys_user")

## 配置字段信息
#set($columns = [...])
#set($pkColumn = {...})
```

### 2. 字段配置示例
```velocity
## 查询字段配置
{
  "javaField": "userName",
  "columnName": "user_name",
  "javaType": "String",
  "queryType": "LIKE",
  "query": true,
  "required": true
}

## 日期范围查询字段
{
  "javaField": "createTime",
  "columnName": "create_time",
  "javaType": "Date",
  "queryType": "BETWEEN",
  "query": true
}
```

### 3. 主子表配置
```velocity
## 主子表关系配置
#set($table.sub = true)
#set($subClassName = "UserRole")
#set($subTableName = "sys_user_role")
#set($subTableFkName = "user_id")
```

## 最佳实践

### 1. SQL优化
- **索引设计**：为常用查询字段创建合适的索引
- **查询优化**：避免使用SELECT *，明确指定需要的字段
- **分页查询**：大数据量查询时使用分页限制结果集
- **条件优化**：将选择性高的条件放在前面

### 2. 参数处理
- **空值检查**：对字符串参数进行空值和空字符串检查
- **类型转换**：确保参数类型与数据库字段类型匹配
- **范围查询**：日期范围查询时验证开始时间和结束时间
- **集合参数**：批量操作时验证集合参数不为空

### 3. 结果映射
- **字段映射**：确保Java字段名与数据库字段名的正确映射
- **类型映射**：注意日期、数字等特殊类型的映射配置
- **关联映射**：主子表关联时配置正确的外键关系
- **性能考虑**：避免不必要的关联查询，按需加载数据

### 4. 维护性
- **命名规范**：遵循统一的命名规范
- **注释完善**：为复杂的SQL语句添加注释
- **版本控制**：SQL变更时做好版本控制和迁移脚本
- **测试覆盖**：为每个SQL语句编写对应的测试用例

## 扩展功能

### 1. 高级查询
- **多表关联**：支持复杂的多表关联查询
- **子查询**：支持嵌套子查询和EXISTS查询
- **聚合函数**：支持COUNT、SUM、AVG等聚合查询
- **分组查询**：支持GROUP BY和HAVING子句

### 2. 缓存集成
- **一级缓存**：MyBatis默认的一级缓存支持
- **二级缓存**：配置二级缓存提高查询性能
- **第三方缓存**：集成Redis等外部缓存系统
- **缓存策略**：合理的缓存更新和失效策略

### 3. 数据库兼容
- **多数据库支持**：支持MySQL、Oracle、PostgreSQL等
- **方言适配**：根据数据库类型生成相应的SQL语法
- **函数映射**：数据库特定函数的抽象和映射
- **类型映射**：不同数据库类型的统一映射

### 4. 监控和调试
- **SQL日志**：详细的SQL执行日志记录
- **性能监控**：SQL执行时间和性能指标监控
- **慢查询分析**：识别和优化慢查询语句
- **错误处理**：完善的异常处理和错误信息

## 逻辑删除机制

### 1. 逻辑删除标识
```sql
-- 使用时间戳作为删除标识
set del_flag = REPLACE(unix_timestamp(current_timestamp(3)),'.','') 
```

### 2. 查询过滤
```xml
<!-- 查询时过滤已删除数据 -->
and del_flag = '1'
```

### 3. 批量逻辑删除
```xml
<update id="logicRemoveByUserIds" parameterType="String">
    update sys_user set del_flag = REPLACE(unix_timestamp(current_timestamp(3)),'.','') where user_id in
    <foreach item="userId" collection="list" open="(" separator="," close=")">
        #{userId}
    </foreach>
</update>
```

## 主子表操作示例

### 1. 主子表关联查询
```xml
<resultMap id="UserRoleResult" type="com.jkr.system.domain.User" extends="UserResult">
    <collection property="roleList" ofType="Role" column="user_id" select="selectRoleList" />
</resultMap>

<select id="selectRoleList" resultMap="RoleResult">
    select role_id, role_name, role_key
    from sys_role r
    left join sys_user_role ur on ur.role_id = r.role_id
    where ur.user_id = #{user_id}
</select>
```

### 2. 子表批量插入
```xml
<insert id="batchRole">
    insert into sys_user_role(user_id, role_id) values
    <foreach item="item" index="index" collection="list" separator=",">
        (#{item.userId}, #{item.roleId})
    </foreach>
</insert>
```

## 原始模板内容

模板文件位置：`d:\dev\framework\jkr-framework-server\jkr-server\src\main\resources\vm\xml\mapper.xml.vm`

该模板使用Velocity模板引擎语法，通过变量替换和条件判断生成完整的MyBatis Mapper XML配置文件。模板包含完整的CRUD操作实现，支持动态查询条件、主子表关联、逻辑删除等高级功能，是MyBatis持久层框架的核心配置模板。