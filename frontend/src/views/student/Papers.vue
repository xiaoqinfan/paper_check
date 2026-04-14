<template>
  <div class="papers-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>论文管理</span>
          <div>
            <el-button type="danger" size="small" @click="batchDelete" :disabled="selectedPapers.length === 0">批量删除</el-button>
            <el-button type="primary" @click="dialogVisible = true">上传论文</el-button>
          </div>
        </div>
      </template>
      
      <el-table 
        :data="papers" 
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="论文ID" width="80" />
        <el-table-column prop="paper_name" label="论文名称" />
        <el-table-column prop="class_id" label="班级ID" width="100" />
        <el-table-column label="操作" width="250">
          <template #default="scope">
            <el-button type="primary" size="small" @click="checkFormat(scope.row.id)">格式检测</el-button>
            <el-button type="success" size="small" @click="viewReport(scope.row.id)">查看报告</el-button>
            <el-button type="danger" size="small" @click="deletePaper(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 上传论文对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="上传论文"
      width="500px"
    >
      <el-form :model="uploadForm" :rules="uploadRules" ref="uploadFormRef">
        <el-form-item label="班级" prop="classId">
          <el-select v-model="uploadForm.classId" placeholder="请选择班级">
            <el-option
              v-for="cls in classes"
              :key="cls.id"
              :label="cls.class_name"
              :value="cls.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="论文名称" prop="paperName">
          <el-input v-model="uploadForm.paperName" placeholder="请输入论文名称" />
        </el-form-item>
        <el-form-item label="论文文件" prop="file">
          <el-upload
            class="upload-demo"
            :action="''"
            :auto-upload="false"
            :on-change="handleFileChange"
            :file-list="fileList"
            accept=".docx"
          >
            <el-button type="primary">选择文件</el-button>
            <template #tip>
              <div class="el-upload__tip">
                只能上传docx文件
              </div>
            </template>
          </el-upload>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitUpload">上传</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import service from '../../utils/request.js'

const router = useRouter()
const papers = ref([])
const classes = ref([])
const dialogVisible = ref(false)
const uploadFormRef = ref(null)
const fileList = ref([])
const selectedPapers = ref([])

const uploadForm = reactive({
  classId: '',
  paperName: ''
})

const uploadRules = {
  classId: [
    { required: true, message: '请选择班级', trigger: 'change' }
  ],
  paperName: [
    { required: true, message: '请输入论文名称', trigger: 'blur' }
  ]
}

onMounted(() => {
  fetchPapers()
  fetchClasses()
})

const fetchPapers = async () => {
  try {
    const studentId = localStorage.getItem('userId')
    const response = await service.get(`/student/papers/list/${studentId}`)
    papers.value = response
  } catch (error) {
    console.error('获取论文列表失败:', error)
  }
}

const fetchClasses = async () => {
  try {
    const response = await service.get('/teacher/class/list')
    classes.value = response
  } catch (error) {
    console.error('获取班级列表失败:', error)
  }
}

const handleFileChange = (file) => {
  fileList.value = [file]
}

const submitUpload = async () => {
  if (!fileList.value.length) {
    alert('请选择文件')
    return
  }
  
  const formData = new FormData()
  formData.append('student_id', localStorage.getItem('userId'))
  formData.append('class_id', uploadForm.classId)
  formData.append('file', fileList.value[0].raw)
  
  try {
    await service.post('/student/paper/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    dialogVisible.value = false
    fileList.value = []
    uploadForm.classId = ''
    uploadForm.paperName = ''
    fetchPapers()
    alert('上传成功')
  } catch (error) {
    console.error('上传失败:', error)
    alert('上传失败')
  }
}

const checkFormat = async (paperId) => {
  try {
    const response = await service.post(`/paper/check/${paperId}`, {
      template_id: 1
    })
    alert(`格式检测完成！得分：${response.score}，错误数：${response.count}`)
  } catch (error) {
    console.error('格式检测失败:', error)
    const errorMsg = error.response?.data?.detail || '格式检测失败'
    alert(errorMsg)
  }
}

const viewReport = (paperId) => {
  router.push(`/home/student/report/${paperId}`)
}

const handleSelectionChange = (val) => {
  selectedPapers.value = val
}

const deletePaper = async (paperId) => {
  if (confirm('确定要删除这篇论文吗？')) {
    try {
      await service.delete(`/paper/delete/${paperId}`)
      fetchPapers()
      alert('删除成功')
    } catch (error) {
      console.error('删除失败:', error)
      alert('删除失败')
    }
  }
}

const batchDelete = async () => {
  if (selectedPapers.value.length === 0) {
    alert('请选择要删除的论文')
    return
  }
  
  if (confirm('确定要批量删除选中的论文吗？')) {
    try {
      const paperIds = selectedPapers.value.map(paper => paper.id)
      await service.post('/paper/batch-delete', { paper_ids: paperIds })
      fetchPapers()
      selectedPapers.value = []
      alert('批量删除成功')
    } catch (error) {
      console.error('批量删除失败:', error)
      alert('批量删除失败')
    }
  }
}
</script>

<style scoped>
.papers-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header div {
  display: flex;
  gap: 10px;
}
</style>
