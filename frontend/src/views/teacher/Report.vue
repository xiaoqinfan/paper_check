<template>
  <div class="report-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>格式检测报告</span>
        </div>
      </template>
      
      <div v-if="report" class="report-content">
        <div class="report-summary">
          <h3>检测结果</h3>
          <el-descriptions :column="2">
            <el-descriptions-item label="格式得分">
              <span class="score">{{ report.task.format_score }}</span>
            </el-descriptions-item>
            <el-descriptions-item label="错误数量">
              <span class="error-count">{{ report.task.total_error }}</span>
            </el-descriptions-item>
          </el-descriptions>
        </div>
        
        <div class="error-details">
          <h3>错误详情</h3>
          <el-table :data="report.error_details" style="width: 100%">
            <el-table-column prop="position" label="位置" />
            <el-table-column prop="error_message" label="错误信息" />
            <el-table-column prop="expect" label="期望" />
            <el-table-column prop="actual" label="实际" />
          </el-table>
        </div>
      </div>
      <div v-else class="loading">
        <el-loading v-model="loading" text="加载中..." />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const report = ref(null)
const loading = ref(true)

onMounted(() => {
  fetchReport()
})

const fetchReport = async () => {
  const paperId = route.params.id
  try {
    const response = await axios.get(`/papers/${paperId}/report`)
    report.value = response.data
  } catch (error) {
    console.error('获取报告失败:', error)
    alert('获取报告失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.report-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.report-content {
  margin-top: 20px;
}

.report-summary {
  margin-bottom: 30px;
}

.score {
  font-size: 24px;
  font-weight: bold;
  color: #67c23a;
}

.error-count {
  font-size: 24px;
  font-weight: bold;
  color: #f56c6c;
}

.error-details {
  margin-top: 30px;
}

.loading {
  height: 300px;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
