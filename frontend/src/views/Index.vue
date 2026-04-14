<template>
  <div class="home-container">
    <!-- 顶部导航栏 -->
    <el-header height="60px" class="header">
      <div class="header-left">
        <h1>论文格式检测系统</h1>
      </div>
      <div class="header-right">
        <span>{{ realName }}</span>
        <el-button type="text" @click="handleLogout">退出登录</el-button>
      </div>
    </el-header>
    
    <!-- 主体内容 -->
    <el-container style="height: calc(100vh - 60px);">
      <!-- 侧边栏 -->
      <el-aside width="200px" class="aside">
        <el-menu
          :default-active="activeMenu"
          class="el-menu-vertical-demo"
          router
        >
          <!-- 学生菜单 -->
          <template v-if="userType === 3">
            <el-menu-item index="/home/student/papers">
              <el-icon><Document /></el-icon>
              <span>论文管理</span>
            </el-menu-item>
          </template>
          
          <!-- 教师菜单 -->
          <template v-else-if="userType === 2">
            <el-menu-item index="/home/teacher">
              <el-icon><School /></el-icon>
              <span>教师后台</span>
            </el-menu-item>
          </template>
          
          <!-- 管理员菜单 -->
          <template v-else-if="userType === 1">
            <el-menu-item index="/home/admin/users">
              <el-icon><User /></el-icon>
              <span>用户管理</span>
            </el-menu-item>
            <el-menu-item index="/home/admin/settings">
              <el-icon><Setting /></el-icon>
              <span>系统配置</span>
            </el-menu-item>
          </template>
        </el-menu>
      </el-aside>
      
      <!-- 内容区域 -->
      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Document, School, Collection, User, Setting } from '@element-plus/icons-vue'

const router = useRouter()
const realName = ref('')
const userType = ref(0)
const activeMenu = ref('')

onMounted(() => {
  // 从localStorage获取用户信息
  realName.value = localStorage.getItem('realName') || ''
  userType.value = parseInt(localStorage.getItem('userType')) || 0
  
  // 设置默认激活的菜单
  setActiveMenu()
})

const setActiveMenu = () => {
  const path = window.location.pathname
  if (userType.value === 3) {
    activeMenu.value = '/home/student/papers'
  } else if (userType.value === 2) {
    activeMenu.value = '/home/teacher'
  } else if (userType.value === 1) {
    activeMenu.value = '/home/admin/users'
  }
}

const handleLogout = () => {
  // 清除登录信息
  localStorage.removeItem('token')
  localStorage.removeItem('userId')
  localStorage.removeItem('username')
  localStorage.removeItem('realName')
  localStorage.removeItem('userType')
  
  // 跳转到登录页
  router.push('/login')
}
</script>

<style scoped>
.home-container {
  height: 100vh;
  overflow: hidden;
}

.header {
  background-color: #409eff;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.header-left h1 {
  font-size: 20px;
  font-weight: bold;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.aside {
  background-color: #f0f2f5;
}

.main {
  padding: 20px;
  background-color: #f5f7fa;
  overflow-y: auto;
}
</style>
