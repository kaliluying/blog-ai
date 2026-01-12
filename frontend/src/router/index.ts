import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'Home', component: Home },
    { path: '/article/:id', name: 'Article', component: () => import('@/views/Article.vue') },
    { path: '/about', name: 'About', component: () => import('@/views/About.vue') },
    { path: '/admin/posts', name: 'AdminPosts', component: () => import('@/views/AdminPosts.vue') },
    { path: '/admin/posts/new', name: 'AdminPostNew', component: () => import('@/views/AdminPostNew.vue') }
  ]
})

export default router
