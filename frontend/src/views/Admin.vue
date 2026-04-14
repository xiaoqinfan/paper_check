<template>
  <div class="admin-page">
    <h2>管理员后台</h2>

    <el-tabs v-model="tab">
      <el-tab-pane label="用户管理" name="user">
        <el-table :data="userList" border>
          <el-table-column label="ID" prop="id" />
          <el-table-column label="账号" prop="username" />
          <el-table-column label="姓名" prop="real_name" />
          <el-table-column label="角色">
            <template #default="scope">
              <el-tag :type="scope.row.user_type === 1 ? 'danger' : scope.row.user_type === 2 ? 'primary' : 'success'">
                {{ scope.row.user_type === 1 ? '管理员' : scope.row.user_type === 2 ? '教师' : '学生' }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <el-tab-pane label="班级管理" name="class">
        <el-table :data="classList" border>
          <el-table-column label="班级" prop="class_name" />
          <el-table-column label="学院" prop="college" />
          <el-table-column label="专业" prop="major" />
        </el-table>
      </el-tab-pane>

      <el-tab-pane label="论文管理" name="paper">
        <el-table :data="paperList" border>
          <el-table-column label="论文名" prop="paper_name" />
          <el-table-column label="上传时间" prop="upload_time" />
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
const tab = ref('user')
const userList = ref([])
const classList = ref([])
const paperList = ref([])

onMounted(() => {
  loadUsers()
  loadClasses()
  loadPapers()
})

const loadUsers = async () => {
  const res = await axios.get('/admin/user/list')
  userList.value = res.data
}
const loadClasses = async () => {
  const res = await axios.get('/teacher/class/list')
  classList.value = res.data
}
const loadPapers = async () => {
  const res = await axios.get('/admin/paper/list')
  paperList.value = res.data
}
</script>

<style scoped>
.admin-page { padding: 20px; }
</style>