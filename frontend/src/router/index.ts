/**
 * Vue Router 路由配置
 *
 * 本文件定义了应用的路由规则，将 URL 路径映射到对应的视图组件。
 * 使用 createWebHistory 创建 HTML5 History 模式的路由。
 */

// 从 vue-router 导入创建路由和历史模式的函数
import { createRouter, createWebHistory } from 'vue-router'

// 导入首页组件（同步加载，因为首页是主要入口）
import Home from '@/views/Home.vue'

// 导入 auth store（用于路由守卫）
import { useAuthStore } from '@/stores/auth'

/**
 * 创建路由实例
 *
 * history: 使用 HTML5 History 模式（URL 不带 # 号）
 * routes: 路由配置数组，定义路径与组件的映射关系
 */
const router = createRouter({
  // 创建基于浏览器 History API 的路由历史
  history: createWebHistory(),

  // 路由配置列表
  routes: [
    // 根路径：首页
    {
      path: '/',
      name: 'Home',
      component: Home
    },

    // 登录页面
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/Login.vue')
    },

    // 注册页面
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/views/Register.vue')
    },

    // 搜索结果页面
    {
      path: '/search',
      name: 'Search',
      component: () => import('@/views/Search.vue')
    },

    // 文章详情页：动态路由参数 :id 表示文章 ID
    {
      path: '/article/:id',
      name: 'Article',
      // 使用动态导入实现路由懒加载（按需加载）
      component: () => import('@/views/Article.vue')
    },

    // 关于页面
    {
      path: '/about',
      name: 'About',
      component: () => import('@/views/About.vue')
    },

    // 管理页面：文章列表
    {
      path: '/admin/posts',
      name: 'AdminPosts',
      component: () => import('@/views/AdminPosts.vue')
    },

    // 管理页面：新建文章
    {
      path: '/admin/posts/new',
      name: 'AdminPostNew',
      component: () => import('@/views/AdminPostNew.vue')
    },

    // 管理页面：编辑文章
    {
      path: '/admin/posts/:id',
      name: 'AdminPostEdit',
      component: () => import('@/views/AdminPostNew.vue')
    },

    // 归档页面：文章归档列表
    {
      path: '/archive',
      name: 'Archive',
      component: () => import('@/views/Archive.vue')
    },

    // 归档页面：指定年月的文章
    {
      path: '/archive/:year/:month',
      name: 'ArchiveMonth',
      component: () => import('@/views/ArchiveMonth.vue')
    },

    // 标签页面：按标签筛选文章
    {
      path: '/tag/:tag',
      name: 'TagPosts',
      component: () => import('@/views/TagPosts.vue')
    }
  ]
})

// ========== 导航守卫 ==========

/**
 * 全局前置守卫
 * 等待 auth 初始化完成后再允许导航
 */
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // 等待 auth 初始化完成
  if (!authStore.initialized) {
    await authStore.init()
  }

  next()
})

// 导出路由实例，供 main.ts 使用
export default router
