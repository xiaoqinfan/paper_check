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
        
        <div v-if="paperContent" class="paper-content">
          <h3>论文内容（带错误标注）</h3>
          <div class="paper-body">
            <div 
              v-for="para in paperContent.paragraphs" 
              :key="para.id" 
              class="paper-paragraph"
              :class="{ 'has-error': hasErrorInParagraph(para.text) }"
              :style="{
                textAlign: getAlignment(para.format?.alignment),
                marginBottom: para.format?.space_after ? para.format.space_after + 'pt' : '15px',
                marginTop: para.format?.space_before ? para.format.space_before + 'pt' : '0px',
                lineHeight: para.format?.line_spacing ? para.format.line_spacing : 1.8,
                padding: '10px 0'
              }"
            >
              <template v-if="para.runs && para.runs.length > 0">
                <span 
                  v-for="(run, runIndex) in para.runs" 
                  :key="runIndex"
                  :style="{
                    fontFamily: run.font_name || 'SimSun, Times New Roman',
                    fontSize: run.font_size + 'pt',
                    fontWeight: run.bold ? 'bold' : 'normal',
                    fontStyle: run.italic ? 'italic' : 'normal',
                    textDecoration: run.underline ? 'underline' : 'none'
                  }"
                >
                  {{ run.text }}
                </span>
              </template>
              <template v-else>
                {{ para.text }}
              </template>
              <div v-if="getErrorsInParagraph(para.text).length > 0" class="error-comments">
                <el-popover 
                  v-for="(error, index) in getErrorsInParagraph(para.text)" 
                  :key="index"
                  placement="top"
                  trigger="hover"
                >
                  <template #reference>
                    <span class="error-marker" :title="error.error_message">{{ index + 1 }}</span>
                  </template>
                  <div class="error-detail">
                    <p><strong>错误类型:</strong> {{ error.error_type }}</p>
                    <p><strong>错误信息:</strong> {{ error.error_message }}</p>
                    <p><strong>期望:</strong> {{ error.expect_value }}</p>
                    <p><strong>实际:</strong> {{ error.actual_value }}</p>
                  </div>
                </el-popover>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="no-content">
          <p>无法加载论文内容</p>
        </div>
        
        <div class="error-details">
          <h3>错误详情</h3>
          <el-table :data="report.errors" style="width: 100%">
            <el-table-column prop="position" label="位置" />
            <el-table-column prop="error_message" label="错误信息" />
            <el-table-column prop="expect_value" label="期望" />
            <el-table-column prop="actual_value" label="实际" />
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
import service from '../../utils/request'

const route = useRoute()
const report = ref(null)
const paperContent = ref(null)
const loading = ref(true)

onMounted(() => {
  fetchData()
})

const fetchData = async () => {
  const paperId = route.params.id
  try {
    // 尝试获取论文内容
    try {
      const contentResponse = await service.get(`/paper/content/${paperId}`)
      paperContent.value = contentResponse
    } catch (error) {
      console.error('获取论文内容失败:', error)
    }
    
    // 首先获取最新的检测任务
    const tasksResponse = await service.get(`/paper/tasks/${paperId}`)
    if (tasksResponse && tasksResponse.length > 0) {
      const latestTask = tasksResponse[tasksResponse.length - 1]
      // 然后获取任务结果
      const response = await service.get(`/paper/result/${latestTask.id}`)
      report.value = response
    } else {
      alert('该论文还没有检测记录')
    }
  } catch (error) {
    console.error('获取报告失败:', error)
    const errorMsg = error.response?.data?.detail || '获取报告失败'
    alert(errorMsg)
  } finally {
    loading.value = false
  }
}

const hasErrorInParagraph = (text) => {
  if (!report.value || !report.value.errors) return false
  return report.value.errors.some(error => text.includes(error.position))
}

const getErrorsInParagraph = (text) => {
  if (!report.value || !report.value.errors) return []
  return report.value.errors.filter(error => text.includes(error.position))
}

const getAlignment = (alignment) => {
  if (!alignment) return 'left'
  const alignmentMap = {
    'LEFT': 'left',
    'CENTER': 'center',
    'RIGHT': 'right',
    'JUSTIFY': 'justify',
    'center': 'center',
    'left': 'left',
    'right': 'right',
    'justify': 'justify'
  }
  return alignmentMap[alignment] || 'left'
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

.paper-content {
  margin: 30px 0;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.paper-body {
  margin-top: 15px;
  line-height: 1.8;
}

.paper-paragraph {
  margin-bottom: 15px;
  padding: 10px;
  border-radius: 4px;
  position: relative;
}

.paper-paragraph.has-error {
  background-color: #fff3f3;
  border-left: 4px solid #f56c6c;
}

.error-comments {
  display: inline-block;
  margin-left: 10px;
  vertical-align: top;
}

.error-marker {
  display: inline-block;
  width: 20px;
  height: 20px;
  background-color: #f56c6c;
  color: white;
  border-radius: 50%;
  text-align: center;
  line-height: 20px;
  font-size: 12px;
  margin-left: 5px;
  cursor: pointer;
}

.error-detail {
  padding: 10px;
  background-color: #fff;
  border: 1px solid #f56c6c;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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
