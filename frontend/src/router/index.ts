/**
 * Vue Router 路由配置
 *
 * 本文件定义了应用的路由规则，将 URL 路径映射到对应的视图组件。
 * 使用 createWebHistory 创建 HTML5 History 模式的路由。
 */

// 从 vue-router 导入创建路由和历史模式的函数
import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useAdminStore } from '@/stores/auth'

// 需要管理员权限的路由
const adminRoutes: RouteRecordRaw[] = [
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: () => import('@/views/AdminLogin.vue')
  },
  {
    path: '/admin/posts',
    name: 'AdminPosts',
    component: () => import('@/views/AdminPosts.vue')
  },
  {
    path: '/admin/posts/new',
    name: 'AdminPostNew',
    component: () => import('@/views/AdminPostNew.vue')
  },
  {
    path: '/admin/posts/:id',
    name: 'AdminPostEdit',
    component: () => import('@/views/AdminPostNew.vue')
  }
]

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
    // 根路径：首页（懒加载）
    {
      path: '/',
      name: 'Home',
      component: () => import('@/views/Home.vue')
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

    // 管理页面：文章列表（需要管理员密码）
    ...adminRoutes,

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

// 路由守卫：检查管理页面访问权限
router.beforeEach((to, from, next) => {
  const adminStore = useAdminStore()

  // 初始化 auth store（从 localStorage 恢复登录状态）
  if (!adminStore.initialized) {
    adminStore.init()
  }

  // 检查是否访问管理页面（排除登录页）
  const isAdminRoute = to.path.startsWith('/admin/')
  const isLoginPage = to.path === '/admin/login'

  if (isAdminRoute && !isLoginPage && !adminStore.isLoggedIn) {
    // 未登录访问管理页面，重定向到登录页
    next({ name: 'AdminLogin', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

// 导出路由实例，供 main.ts 使用
export default router
export { adminRoutes }
