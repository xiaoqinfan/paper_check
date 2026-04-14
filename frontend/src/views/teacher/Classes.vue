<template>
  <div class="classes-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>班级管理</span>
          <el-button type="primary" @click="dialogVisible = true">创建班级</el-button>
        </div>
      </template>
      
      <el-table :data="classes" style="width: 100%">
        <el-table-column prop="id" label="班级ID" width="80" />
        <el-table-column prop="class_name" label="班级名称" />
        <el-table-column prop="college" label="学院" />
        <el-table-column prop="major" label="专业" />
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button type="primary" size="small" @click="viewStudents(scope.row.id)">查看学生</el-button>
            <el-button type="success" size="small" @click="viewPapers(scope.row.id)">查看论文</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 创建班级对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="创建班级"
      width="500px"
    >
      <el-form :model="classForm" :rules="classRules" ref="classFormRef">
        <el-form-item label="班级名称" prop="className">
          <el-input v-model="classForm.className" placeholder="请输入班级名称" />
        </el-form-item>
        <el-form-item label="学院" prop="college">
          <el-input v-model="classForm.college" placeholder="请输入学院" />
        </el-form-item>
        <el-form-item label="专业" prop="major">
          <el-input v-model="classForm.major" placeholder="请输入专业" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitClass">创建</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 学生列表对话框 -->
    <el-dialog
      v-model="studentsDialogVisible"
      title="班级学生"
      width="600px"
    >
      <el-table :data="students" style="width: 100%">
        <el-table-column prop="id" label="学生ID" width="80" />
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="real_name" label="真实姓名" />
      </el-table>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import service from '../../utils/request.js'

const router = useRouter()
const classes = ref([])
const students = ref([])
const dialogVisible = ref(false)
const studentsDialogVisible = ref(false)
const classFormRef = ref(null)
const currentClassId = ref(0)

const classForm = reactive({
  className: '',
  college: '',
  major: ''
})

const classRules = {
  className: [
    { required: true, message: '请输入班级名称', trigger: 'blur' }
  ],
  college: [
    { required: true, message: '请输入学院', trigger: 'blur' }
  ],
  major: [
    { required: true, message: '请输入专业', trigger: 'blur' }
  ]
}

onMounted(() => {
  fetchClasses()
})

const fetchClasses = async () => {
  try {
    const response = await service.get('/teacher/class/list')
    classes.value = response
  } catch (error) {
    console.error('获取班级列表失败:', error)
  }
}

const submitClass = async () => {
  try {
    await service.post('/teacher/class/create', {
      name: classForm.className,
      college: classForm.college,
      major: classForm.major
    })
    dialogVisible.value = false
    classForm.className = ''
    classForm.college = ''
    classForm.major = ''
    fetchClasses()
    alert('班级创建成功')
  } catch (error) {
    console.error('创建班级失败:', error)
    alert('创建班级失败')
  }
}

const viewStudents = async (classId) => {
  currentClassId.value = classId
  try {
    // 暂时模拟学生数据
    students.value = [
      { id: 1, username: 'student1', real_name: '学生1' },
      { id: 2, username: 'student2', real_name: '学生2' }
    ]
    studentsDialogVisible.value = true
  } catch (error) {
    console.error('获取学生列表失败:', error)
    alert('获取学生列表失败')
  }
}

const viewPapers = (classId) => {
  router.push({ path: '/home/teacher', query: { classId } })
}
</script>

<style scoped>
.classes-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
