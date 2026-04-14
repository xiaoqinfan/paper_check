<template>
  <div class="users-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户管理</span>
          <el-button type="primary" @click="dialogVisible = true">创建用户</el-button>
        </div>
      </template>
      
      <el-table :data="users" style="width: 100%">
        <el-table-column prop="id" label="用户ID" width="80" />
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="real_name" label="真实姓名" />
        <el-table-column prop="user_type" label="用户类型" width="120">
          <template #default="scope">
            <span v-if="scope.row.user_type === 1">管理员</span>
            <span v-else-if="scope.row.user_type === 2">教师</span>
            <span v-else-if="scope.row.user_type === 3">学生</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button type="primary" size="small" @click="editUser(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="deleteUser(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 创建/编辑用户对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑用户' : '创建用户'"
      width="500px"
    >
      <el-form :model="userForm" :rules="userRules" ref="userFormRef">
        <el-form-item label="用户名" prop="username" :disabled="isEdit">
          <el-input v-model="userForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="真实姓名" prop="realName">
          <el-input v-model="userForm.realName" placeholder="请输入真实姓名" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="!isEdit">
          <el-input v-model="userForm.password" type="password" placeholder="请输入密码" />
        </el-form-item>
        <el-form-item label="用户类型" prop="userType">
          <el-select v-model="userForm.userType" placeholder="请选择用户类型">
            <el-option label="管理员" value="1" />
            <el-option label="教师" value="2" />
            <el-option label="学生" value="3" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitUser">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'

const users = ref([])
const dialogVisible = ref(false)
const userFormRef = ref(null)
const isEdit = ref(false)
const currentUserId = ref(0)

const userForm = reactive({
  username: '',
  realName: '',
  password: '',
  userType: ''
})

const userRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  realName: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ],
  userType: [
    { required: true, message: '请选择用户类型', trigger: 'change' }
  ]
}

onMounted(() => {
  fetchUsers()
})

const fetchUsers = async () => {
  try {
    const response = await axios.get('/users')
    users.value = response.data
  } catch (error) {
    console.error('获取用户列表失败:', error)
  }
}

const submitUser = async () => {
  try {
    if (isEdit.value) {
      // 编辑用户
      await axios.put(`/users/${currentUserId.value}`, {
        real_name: userForm.realName,
        user_type: userForm.userType
      })
    } else {
      // 创建用户
      await axios.post('/users', {
        username: userForm.username,
        password: userForm.password,
        real_name: userForm.realName,
        user_type: userForm.userType
      })
    }
    dialogVisible.value = false
    fetchUsers()
    alert('操作成功')
  } catch (error) {
    console.error('操作失败:', error)
    alert('操作失败')
  }
}

const editUser = (user) => {
  isEdit.value = true
  currentUserId.value = user.id
  userForm.username = user.username
  userForm.realName = user.real_name
  userForm.userType = user.user_type
  dialogVisible.value = true
}

const deleteUser = async (userId) => {
  if (confirm('确定要删除该用户吗？')) {
    try {
      await axios.delete(`/users/${userId}`)
      fetchUsers()
      alert('删除成功')
    } catch (error) {
      console.error('删除失败:', error)
      alert('删除失败')
    }
  }
}
</script>

<style scoped>
.users-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
