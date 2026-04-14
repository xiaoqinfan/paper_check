<template>
  <div class="papers-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>班级论文管理</span>
        </div>
      </template>
      
      <el-table :data="papers" style="width: 100%">
        <el-table-column prop="id" label="论文ID" width="80" />
        <el-table-column prop="paper_name" label="论文名称" />
        <el-table-column prop="student_id" label="学生ID" width="100" />
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button type="primary" size="small" @click="checkFormat(scope.row.id)">格式检测</el-button>
            <el-button type="success" size="small" @click="viewReport(scope.row.id)">查看报告</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const papers = ref([])

onMounted(() => {
  fetchPapers()
})

const fetchPapers = async () => {
  const classId = route.params.classId
  try {
    const response = await axios.get(`/papers/class/${classId}/list`)
    papers.value = response.data
  } catch (error) {
    console.error('获取论文列表失败:', error)
  }
}

const checkFormat = async (paperId) => {
  try {
    await axios.post(`/papers/${paperId}/check`)
    alert('格式检测完成')
  } catch (error) {
    console.error('格式检测失败:', error)
    alert('格式检测失败')
  }
}

const viewReport = (paperId) => {
  // 跳转到报告查看页面
  router.push(`/home/teacher/report/${paperId}`)
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
</style>
