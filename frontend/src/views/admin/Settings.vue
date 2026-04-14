<template>
  <div class="settings-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>系统配置</span>
        </div>
      </template>
      
      <el-form :model="settings" :rules="rules" ref="settingsRef">
        <el-form-item label="系统名称" prop="systemName">
          <el-input v-model="settings.systemName" placeholder="请输入系统名称" />
        </el-form-item>
        <el-form-item label="系统版本" prop="systemVersion">
          <el-input v-model="settings.systemVersion" placeholder="请输入系统版本" />
        </el-form-item>
        <el-form-item label="最大上传文件大小" prop="maxFileSize">
          <el-input v-model="settings.maxFileSize" type="number" placeholder="请输入最大上传文件大小（MB）" />
        </el-form-item>
        <el-form-item label="允许上传的文件类型" prop="allowedFileTypes">
          <el-input v-model="settings.allowedFileTypes" placeholder="请输入允许上传的文件类型，用逗号分隔" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitSettings">保存配置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'

const settings = reactive({
  systemName: '论文管理系统',
  systemVersion: '1.0.0',
  maxFileSize: 50,
  allowedFileTypes: '.doc,.docx,.pdf'
})

const rules = {
  systemName: [
    { required: true, message: '请输入系统名称', trigger: 'blur' }
  ],
  systemVersion: [
    { required: true, message: '请输入系统版本', trigger: 'blur' }
  ],
  maxFileSize: [
    { required: true, message: '请输入最大上传文件大小', trigger: 'blur' },
    { type: 'number', min: 1, message: '最大上传文件大小至少为1MB', trigger: 'blur' }
  ],
  allowedFileTypes: [
    { required: true, message: '请输入允许上传的文件类型', trigger: 'blur' }
  ]
}

const submitSettings = () => {
  // 这里可以实现保存配置的逻辑
  alert('配置保存成功')
}
</script>

<style scoped>
.settings-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
