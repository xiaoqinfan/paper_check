<template>
  <div class="student-page">
    <h2>学生论文格式检测</h2>

    <div class="card">
      <h3>1. 上传论文（.docx）</h3>
      <el-upload :auto-upload="false" @change="handleFileChange">
        <el-button type="primary">选择文件</el-button>
        <el-button
          style="margin-left: 10px"
          type="success"
          :loading="uploadLoading"
          @click="uploadPaper"
        >
          确认上传
        </el-button>
      </el-upload>
      <div v-if="paperId" class="tip">
        上传成功，论文 ID：{{ paperId }}
      </div>
    </div>

    <div class="card">
      <h3>2. 选择检测模板</h3>
      <el-select v-model="templateId" placeholder="请选择模板" style="width: 300px">
        <el-option
          v-for="t in templateList"
          :key="t.id"
          :label="t.template_name"
          :value="t.id"
        />
      </el-select>
      <el-button
        type="primary"
        style="margin-left: 10px"
        :disabled="!paperId || !templateId"
        :loading="checkLoading"
        @click="startCheck"
      >
        开始检测
      </el-button>
    </div>

    <div class="card" v-if="resultVisible">
      <h3>3. 检测报告</h3>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="格式得分">
          <span :style="{ color: score < 60 ? 'red' : 'green' }">
            {{ score }}
          </span>
        </el-descriptions-item>
        <el-descriptions-item label="错误总数">{{ errorCount }}</el-descriptions-item>
      </el-descriptions>

      <el-table :data="errors" border style="width: 100%; margin-top: 20px">
        <el-table-column prop="position" label="位置" />
        <el-table-column prop="error_type" label="错误类型" />
        <el-table-column prop="error_message" label="问题说明" />
        <el-table-column prop="expect_value" label="要求" />
        <el-table-column prop="actual_value" label="实际" />
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const user = JSON.parse(localStorage.getItem('user'))
const file = ref(null)
const paperId = ref(null)
const templateId = ref(null)
const templateList = ref([])

const uploadLoading = ref(false)
const checkLoading = ref(false)
const resultVisible = ref(false)
const score = ref(0)
const errorCount = ref(0)
const errors = ref([])

onMounted(() => {
  loadTemplates()
})

const loadTemplates = async () => {
  const res = await axios.get('/teacher/template/list')
  templateList.value = res.data
}

const handleFileChange = (uploadFile) => {
  file.value = uploadFile.raw
}

const uploadPaper = async () => {
  if (!file.value) return ElMessage.warning('请选择文件')
  uploadLoading.value = true
  const form = new FormData()
  form.append('file', file.value)
  try {
    const res = await axios.post(
      `/student/paper/upload?student_id=${user.id}&class_id=1`,
      form
    )
    paperId.value = res.data.paper_id
    ElMessage.success('上传成功')
  } finally {
    uploadLoading.value = false
  }
}

const startCheck = async () => {
  checkLoading.value = true
  try {
    const res = await axios.post(`/paper/check/${paperId.value}?template_id=${templateId.value}`)
    score.value = res.data.score
    errorCount.value = res.data.count
    errors.value = res.data.errors
    resultVisible.value = true
    ElMessage.success('检测完成')
  } finally {
    checkLoading.value = false
  }
}
</script>

<style scoped>
.student-page {
  max-width: 1100px;
  margin: 40px auto;
  padding: 0 20px;
}
.card {
  background: #fff;
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}
.tip {
  margin-top: 10px;
  color: #333;
}
</style>