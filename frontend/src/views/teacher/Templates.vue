<template>
  <div class="templates-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>格式模板配置</span>
          <el-button type="primary" @click="dialogVisible = true">创建模板</el-button>
        </div>
      </template>
      
      <el-table :data="templates" style="width: 100%">
        <el-table-column prop="id" label="模板ID" width="80" />
        <el-table-column prop="template_name" label="模板名称" />
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button type="primary" size="small" @click="viewRules(scope.row.id)">查看规则</el-button>
            <el-button type="success" size="small" @click="addRule(scope.row.id)">添加规则</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 创建模板对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="创建模板"
      width="500px"
    >
      <el-form :model="templateForm" :rules="templateRules" ref="templateFormRef">
        <el-form-item label="模板名称" prop="templateName">
          <el-input v-model="templateForm.templateName" placeholder="请输入模板名称" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitTemplate">创建</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 规则列表对话框 -->
    <el-dialog
      v-model="rulesDialogVisible"
      title="规则列表"
      width="800px"
    >
      <el-table :data="rules" style="width: 100%">
        <el-table-column prop="id" label="规则ID" width="80" />
        <el-table-column prop="target_part" label="目标部分" />
        <el-table-column prop="rule_key" label="规则键" />
        <el-table-column prop="rule_value" label="规则值" />
        <el-table-column prop="error_tip" label="错误提示" />
      </el-table>
    </el-dialog>
    
    <!-- 添加规则对话框 -->
    <el-dialog
      v-model="addRuleDialogVisible"
      title="添加规则"
      width="500px"
    >
      <el-form :model="ruleForm" :rules="ruleRules" ref="ruleFormRef">
        <el-form-item label="目标部分" prop="targetPart">
          <el-select v-model="ruleForm.targetPart" placeholder="请选择目标部分">
            <el-option label="标题" value="标题" />
            <el-option label="正文" value="正文" />
            <el-option label="摘要" value="摘要" />
            <el-option label="参考文献" value="参考文献" />
          </el-select>
        </el-form-item>
        <el-form-item label="规则键" prop="ruleKey">
          <el-select v-model="ruleForm.ruleKey" placeholder="请选择规则项">
            <el-option label="字体" value="font_name" />
            <el-option label="字号" value="font_size" />
            <el-option label="行距" value="line_height" />
            <el-option label="缩进" value="indent" />
            <el-option label="对齐方式" value="alignment" />
          </el-select>
        </el-form-item>
        <el-form-item label="规则值" prop="ruleValue">
          <el-input v-model="ruleForm.ruleValue" placeholder="请输入规则值" />
        </el-form-item>
        <el-form-item label="错误提示" prop="errorTip">
          <el-input v-model="ruleForm.errorTip" placeholder="请输入错误提示" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="addRuleDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitRule">添加</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'

const templates = ref([])
const rules = ref([])
const dialogVisible = ref(false)
const rulesDialogVisible = ref(false)
const addRuleDialogVisible = ref(false)
const templateFormRef = ref(null)
const ruleFormRef = ref(null)
const currentTemplateId = ref(0)

const templateForm = reactive({
  templateName: ''
})

const templateRules = {
  templateName: [
    { required: true, message: '请输入模板名称', trigger: 'blur' }
  ]
}

const ruleForm = reactive({
  targetPart: '',
  ruleKey: '',
  ruleValue: '',
  errorTip: ''
})

const ruleRules = {
  targetPart: [
    { required: true, message: '请输入目标部分', trigger: 'blur' }
  ],
  ruleKey: [
    { required: true, message: '请输入规则键', trigger: 'blur' }
  ],
  ruleValue: [
    { required: true, message: '请输入规则值', trigger: 'blur' }
  ],
  errorTip: [
    { required: true, message: '请输入错误提示', trigger: 'blur' }
  ]
}

onMounted(() => {
  fetchTemplates()
})

const fetchTemplates = async () => {
  try {
    const response = await axios.get('/templates')
    templates.value = response.data
  } catch (error) {
    console.error('获取模板列表失败:', error)
  }
}

const submitTemplate = async () => {
  try {
    await axios.post('/templates', {
      template_name: templateForm.templateName
    })
    dialogVisible.value = false
    templateForm.templateName = ''
    fetchTemplates()
    alert('模板创建成功')
  } catch (error) {
    console.error('创建模板失败:', error)
    alert('创建模板失败')
  }
}

const viewRules = async (templateId) => {
  currentTemplateId.value = templateId
  try {
    const response = await axios.get(`/templates/${templateId}/rules`)
    rules.value = response.data
    rulesDialogVisible.value = true
  } catch (error) {
    console.error('获取规则列表失败:', error)
    alert('获取规则列表失败')
  }
}

const addRule = (templateId) => {
  currentTemplateId.value = templateId
  ruleForm.targetPart = ''
  ruleForm.ruleKey = ''
  ruleForm.ruleValue = ''
  ruleForm.errorTip = ''
  addRuleDialogVisible.value = true
}

const submitRule = async () => {
  try {
    await axios.post(`/templates/${currentTemplateId.value}/rules`, {
      target_part: ruleForm.targetPart,
      rule_key: ruleForm.ruleKey,
      rule_value: ruleForm.ruleValue,
      error_tip: ruleForm.errorTip
    })
    addRuleDialogVisible.value = false
    alert('规则添加成功')
  } catch (error) {
    console.error('添加规则失败:', error)
    alert('添加规则失败')
  }
}
</script>

<style scoped>
.templates-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
