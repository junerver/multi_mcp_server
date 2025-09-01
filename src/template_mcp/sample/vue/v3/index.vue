<template>
    <div class="app-container">
        <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
                        <el-form-item label="是否启用" prop="enabled">
                            <el-input
                                    v-model="queryParams.enabled"
                                    placeholder="请输入是否启用"
                                    clearable
                                    @keyup.enter="handleQuery"
                            />
                        </el-form-item>
            <el-form-item>
                <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
                <el-button icon="Refresh" @click="resetQuery">重置</el-button>
            </el-form-item>
        </el-form>

        <el-row :gutter="10" class="mb8">
            <el-col :span="1.5">
                <el-button
                        type="primary"
                        plain
                        icon="Plus"
                        @click="handleAdd"
                        v-hasPermi="['system:prompt:add']"
                >新增</el-button>
            </el-col>
            <el-col :span="1.5">
                <el-button
                        type="danger"
                        plain
                        icon="Delete"
                        :disabled="multiple"
                        @click="handleDelete"
                        v-hasPermi="['system:prompt:remove']"
                >删除</el-button>
            </el-col>
            <el-col :span="1.5">
                <el-button
                        type="warning"
                        plain
                        icon="Download"
                        @click="handleExport"
                        v-hasPermi="['system:prompt:export']"
                >导出</el-button>
            </el-col>
            <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
        </el-row>

        <el-table v-loading="tableObject.loading" :data="tableObject.tableList" @selection-change="handleSelectionChange">
            <el-table-column type="selection" width="55" align="center" />
            <el-table-column label="序号" width="50" type="index" align="center">
                <template #default="scope">
                    <span>{{ (tableObject.currentPage - 1) * tableObject.pageSize + scope.$index + 1 }}</span>
                </template>
            </el-table-column>
                    <el-table-column label="主键id" align="center" prop="id" />
                    <el-table-column label="prompt内容" align="center" prop="content" />
                    <el-table-column label="是否启用" align="center" prop="enabled" />
                    <el-table-column label="备注" align="center" prop="remark" />
            <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
                <template #default="scope">
                    <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['system:prompt:edit']">修改</el-button>
                    <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['system:prompt:remove']">删除</el-button>
                </template>
            </el-table-column>
        </el-table>

        <pagination
          v-show="tableObject.total > 0"
          :total="tableObject.total"
          v-model:page="tableObject.currentPage"
          v-model:limit="tableObject.pageSize"
          @pagination="getList"
        />

      <!-- 添加或修改参数配置对话框 -->
      <Form ref="formRef" @success="submitSuccess"></Form>
    </div>
</template>

<script setup name="Prompt">
    import { listPrompt, batchDelPrompt } from "@/api/system/prompt";
    import { useTable } from '@/hook/useTable.js';
    import Form from './Form.vue';

    const { proxy } = getCurrentInstance();
    const showSearch = ref(true);
    const ids = ref([]);
    const single = ref(true);
    const multiple = ref(true);
    const formRef = ref()
    const queryParams=ref({
        content: null,
        enabled: null,
    })

    const { tableObject,tableMethods } = useTable({
        defaultParams:
            queryParams.value,
        getListApi:listPrompt,
        delListApi:batchDelPrompt
        })

    const { getList,setSearchParams } = tableMethods

    /** 搜索按钮操作 */
    function handleQuery() {
      setSearchParams(queryParams.value)
    }

    /** 删除按钮操作 */
    function handleDelete(row) {
      const _ids = row?.id?[row.id]: Object.values(ids.value);
        const form={
            ids:_ids
        }
      tableMethods.delList(form, false)
    }

    /** 重置按钮操作 */
    function resetQuery() {
      proxy.resetForm("queryRef");
      handleQuery();
    }

    /** 新增按钮操作 */
    function handleAdd() {
      formRef.value.open('添加')
    }

    /** 多选框选中数据 */
    function handleSelectionChange(selection) {
      ids.value = selection.map(item => item.id);
      single.value = selection.length != 1;
      multiple.value = !selection.length;
    }

    /** 修改按钮操作 */
    function handleUpdate(row) {
      formRef.value.open('编辑',row.id)
    }

    /** 提交按钮 */
    const submitSuccess = ()=>{
      getList()
    }

    /** 导出按钮操作 */
    function handleExport() {
      proxy.download('system/prompt/export', {
        ...queryParams.value
      }, `prompt_${new Date().getTime()}.xlsx`)
    }

    getList();
</script>
