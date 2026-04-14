import { createRouter, createWebHistory } from 'vue-router'
import Student from '../views/Student.vue'
import Admin from '../views/Admin.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('../views/Index.vue'),
    meta: { requiresAuth: true },
    children: [
      // 学生路由
      {
        path: 'student/papers',
        name: 'StudentPapers',
        component: () => import('../views/student/Papers.vue'),
        meta: { requiresAuth: true, roles: [3] }
      },
      {
        path: 'student/report/:id',
        name: 'StudentReport',
        component: () => import('../views/student/Report.vue'),
        meta: { requiresAuth: true, roles: [3] }
      },
      // 教师路由
      {
        path: 'teacher',
        name: 'Teacher',
        component: () => import('../views/Teacher.vue'),
        meta: { requiresAuth: true, roles: [2] }
      },
      // 管理员路由
      {
        path: 'admin/users',
        name: 'AdminUsers',
        component: () => import('../views/admin/Users.vue'),
        meta: { requiresAuth: true, roles: [1] }
      },
      {
        path: 'admin/settings',
        name: 'AdminSettings',
        component: () => import('../views/admin/Settings.vue'),
        meta: { requiresAuth: true, roles: [1] }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 检查是否需要认证
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 检查是否登录
    const userId = localStorage.getItem('userId')
    if (!userId) {
      // 未登录，重定向到登录页
      next({ path: '/login' })
    } else {
      // 已登录，检查权限
      const userType = parseInt(localStorage.getItem('userType'))
      if (to.meta.roles && !to.meta.roles.includes(userType)) {
        // 无权限，重定向到首页
        next({ path: '/home' })
      } else {
        // 有权限，继续访问
        next()
      }
    }
  } else {
    // 不需要认证，继续访问
    next()
  }
})

export default router
