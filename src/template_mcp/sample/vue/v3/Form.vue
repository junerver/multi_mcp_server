<template>
    <!-- 添加或修改AI提示词内容管理对话框 -->
    <Dialog :title="dialogTitle" v-model="dialogVisible">
        <el-form ref="formRef" :model="form" :rules="formRules" label-width="80px">
                            <el-form-item label="prompt内容">
                                <editor v-model="form.content" :min-height="192"/>
                            </el-form-item>
                            <el-form-item label="是否启用" prop="enabled">
                                <el-input v-model="form.enabled" placeholder="请输入是否启用" />
                            </el-form-item>
                            <el-form-item label="备注" prop="remark">
                                <el-input v-model="form.remark" type="textarea" placeholder="请输入内容" />
                            </el-form-item>
        </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button type="primary" :disabled="formLoading" @click="submitForm">确 定</el-button>
                <el-button @click="dialogVisible=false">取 消</el-button>
            </div>
        </template>
    </Dialog>
</template>

<script setup name="Prompt">
    import Dialog from "@/components/Dialog/index.vue";
    import { getPrompt, addPrompt, updatePrompt } from "@/api/system/prompt";

    const { proxy } = getCurrentInstance();

    const emit = defineEmits(['success'])
    const form = ref({})
    const dialogTitle = ref('')
    const dialogVisible = ref(false)
    const formLoading = ref(false)
    const formType = ref('')
    const formRef = ref()
    const open = async (type,id)=>{
      resetForm()
      dialogVisible.value = true
      dialogTitle.value = formType
      formType.value = type
      if(id){
        formLoading.value = true
        try {
          const data = await getPrompt(id)
          form.value = data.data
        }finally
        {
          formLoading.value = false
        }
      }
    }
    defineExpose({ open })
    const formRules = reactive({
                    enabled: [
                { required: true, message: "是否启用不能为空", trigger: "blur" }
              ],
                    createTime: [
                { required: true, message: "创建时间不能为空", trigger: "blur" }
              ],
                    updateTime: [
                { required: true, message: "更新时间不能为空", trigger: "blur" }
              ],
                    delFlag: [
                { required: true, message: "删除标志不能为空", trigger: "blur" }
              ],
    })


    /** 提交表单 */
    const submitForm = async () => {
      // 校验表单
      if (!formRef) return
      const valid = await formRef.value.validate()
      if (!valid) return

      try {
        if (formType.value == '编辑') {
          await updatePrompt(form.value)
          proxy.$modal.msgSuccess("修改成功");
        } else {
          await addPrompt(form.value)
          proxy.$modal.msgSuccess("添加成功");
        }
        dialogVisible.value = false
        emit('success')
      } finally {
        formLoading.value = false
      }
    }

    /** 表单重置 */
    function resetForm() {
      form.value = {
                      id: null,
                      content: null,
                      enabled: null,
                      createBy: null,
                      createTime: null,
                      updateBy: null,
                      updateTime: null,
                      delFlag: null,
                      remark: null
      };
      proxy.resetForm("formRef");
    }
</script>
<style scoped lang="scss">

</style>