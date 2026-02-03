<!--
  App.vue - 应用根组件

  本组件是整个 Vue 应用的顶层容器，包含：
  1. Naive UI 组件Provider（配置全局主题和弹窗服务）
  2. 顶部导航栏（Logo 和导航链接、用户菜单）
  3. 主内容区（路由视图容器）
  4. 底部版权信息
-->

<template>
  <n-config-provider :theme-overrides="themeOverrides" :theme="naiveTheme">

    <n-message-provider>
      <n-notification-provider>
        <n-dialog-provider>
          <n-loading-bar-provider>

            <div class="blog-layout">

              <header class="header">
                <div class="header-content">
                  <router-link to="/" class="logo">
                    <HandDrawnIcon type="star" :size="28" />
                    <span>手绘博客</span>
                  </router-link>

                  <div class="search-box">
                    <n-input v-model:value="searchQuery" placeholder="搜索文章..." @keyup.enter="handleSearch" clearable>
                      <template #prefix>
                        <n-icon :component="SearchIcon" />
                      </template>
                    </n-input>
                  </div>

                  <nav class="nav">
                    <router-link to="/" class="nav-link">首页</router-link>
                    <template v-if="authStore.isLoggedIn">
                      <router-link to="/admin/posts" class="nav-link">管理</router-link>
                      <n-dropdown :options="adminMenuOptions" @select="handleAdminMenuSelect">
                        <span class="nav-link user-name">博主</span>
                      </n-dropdown>
                    </template>
                    <template v-else>
                      <router-link to="/admin/posts" class="nav-link">管理</router-link>
                    </template>
                    <router-link to="/about" class="nav-link">关于</router-link>
                    <n-button quaternary circle @click="handleThemeToggle" class="theme-toggle">
                      <template #icon>
                        <n-icon :component="themeIcon" />
                      </template>
                    </n-button>
                  </nav>
                </div>
              </header>

              <!-- 主内容区域 -->
              <main class="main-content">
                <!-- 路由视图：使用 transition 实现页面切换过渡动画 -->
                <router-view v-slot="{ Component }">
                  <transition name="fade">
                    <component :is="Component" />
                  </transition>
                </router-view>
              </main>

              <!-- 底部区域 -->
              <footer class="footer">
                <p>手绘风格博客 - Built with Vue 3 + Naive UI + Rough.js</p>
              </footer>

              <!-- 回到顶部按钮 -->
              <transition name="slide-up">
                <n-button v-if="showBackToTop" circle class="back-to-top" @click="scrollToTop">
                  <template #icon>
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                      stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M12 19V5M5 12l7-7 7 7" />
                    </svg>
                  </template>
                </n-button>
              </transition>

            </div>
          </n-loading-bar-provider>
        </n-dialog-provider>
      </n-notification-provider>
    </n-message-provider>
  </n-config-provider>
</template>

<script setup lang="ts">
import { ref, computed, h, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { NIcon, type GlobalThemeOverrides, darkTheme } from 'naive-ui'

import HandDrawnIcon from '@/components/HandDrawnIcon.vue'
import { SearchIcon, WriteIcon, LogoutIcon, SunIcon, MoonIcon } from '@/components/icons'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'

const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()

const searchQuery = ref('')
const showBackToTop = ref(false)

// 监听滚动事件
const handleScroll = () => {
  showBackToTop.value = window.scrollY > 300
}

// 回到顶部
const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

const themeIcon = computed(() => {
  return themeStore.isDark ? MoonIcon : SunIcon
})

const handleThemeToggle = () => {
  themeStore.toggleTheme()
}

// 博主管理菜单选项
const adminMenuOptions = [
  {
    label: '写文章',
    key: 'write',
    icon: () => h(NIcon, null, { default: () => h(WriteIcon) })
  },
  { type: 'divider', key: 'd1' },
  {
    label: '退出登录',
    key: 'logout',
    icon: () => h(NIcon, null, { default: () => h(LogoutIcon) })
  }
]

// 处理博主菜单选择
const handleAdminMenuSelect = (key: string) => {
  switch (key) {
    case 'write':
      router.push('/admin/posts/new')
      break
    case 'logout':
      authStore.logout()
      break
  }
}

// 搜索处理
const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({ path: '/search', query: { q: searchQuery.value } })
  }
}

/**
 * 全局主题配置
 * 自定义 Naive UI 的默认主题色、字体和圆角等样式
 */
const themeOverrides: GlobalThemeOverrides = {
  common: {
    primaryColor: '#34495e',
    primaryColorHover: '#5d6d7e',
    primaryColorPressed: '#2c3e50',
    borderRadius: '3px',
    fontFamily: '"Caveat", "Comic Sans MS", cursive, sans-serif',
    fontFamilyMono: '"Courier New", monospace'
  },
  Button: {
    borderRadiusMedium: '8px 8px 4px 4px',
    borderRadiusSmall: '6px 6px 3px 3px',
    fontWeight: '600'
  },
  Card: {
    borderRadius: '12px 12px 8px 8px',
    boxShadow: '2px 2px 0 #34495e'
  },
  Input: {
    borderRadius: '6px 6px 3px 3px'
  },
  Tag: {
    borderRadius: '4px 4px 2px 2px'
  }
}

const naiveTheme = computed(() => themeStore.isDark ? darkTheme : null)
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400;700&display=swap');

:root {
  --bg-primary: #fefefe;
  --bg-secondary: #f5f5dc;
  --text-primary: #2c3e50;
  --text-secondary: #7f8c8d;
  --border-color: #34495e;
  --card-bg: #ffffff;
  --shadow-color: #34495e;
  --code-bg: #f5f5f5;
  --blockquote-bg: #f8f8f8;
}

html.dark {
  --bg-primary: #1a1a2e;
  --bg-secondary: #16213e;
  --text-primary: #e4e4e7;
  --text-secondary: #a1a1aa;
  --border-color: #4a5568;
  --card-bg: #1e293b;
  --shadow-color: #0f172a;
  --code-bg: #0d1117;
  --blockquote-bg: #1e293b;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.blog-layout {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
  transition: background 0.3s ease;
}

.header {
  background: var(--card-bg);
  border-bottom: 2px solid var(--border-color);
  position: sticky;
  top: 0;
  z-index: 100;
  transition: background 0.3s ease, border-color 0.3s ease;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 16px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: var(--text-primary);
  font-family: 'Caveat', cursive;
  font-size: 1.5rem;
  font-weight: 700;
  flex-shrink: 0;
  transition: color 0.3s ease;
}

.search-box {
  flex: 1;
  max-width: 400px;
}

.nav {
  display: flex;
  gap: 24px;
  align-items: center;
}

.nav-link {
  text-decoration: none;
  color: var(--text-primary);
  font-size: 1.1rem;
  font-weight: 600;
  transition: color 0.2s;
  font-family: inherit;
}

.nav-link:hover {
  color: #5d6d7e;
}

.nav-link.router-link-active {
  color: var(--text-primary);
}

.user-name {
  cursor: pointer;
}

.theme-toggle {
  margin-left: 8px;
}

.main-content {
  min-height: calc(100vh - 140px);
}

.footer {
  background: var(--border-color);
  color: var(--bg-primary);
  text-align: center;
  padding: 20px;
  position: relative;
  z-index: 10;
  transition: background 0.3s ease, color 0.3s ease;
}

.footer p {
  margin: 0;
  font-family: 'Caveat', cursive;
  font-size: 1.1rem;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

html.dark .footer {
  background: var(--shadow-color);
}

html.dark .nav-link:hover {
  color: #94a3b8;
}

html.dark .article-content :deep(pre .copy-btn) {
  background: rgba(255, 255, 255, 0.1);
  color: #a1a1aa;
}

html.dark .article-content :deep(pre .copy-btn:hover) {
  background: rgba(255, 255, 255, 0.2);
  color: #e4e4e7;
}

.back-to-top {
  position: fixed;
  bottom: 40px;
  right: 40px;
  z-index: 100;
  box-shadow: 2px 2px 0 var(--border-color);
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>
