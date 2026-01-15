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

            </div>
          </n-loading-bar-provider>
        </n-dialog-provider>
      </n-notification-provider>
    </n-message-provider>
  </n-config-provider>
</template>

<script setup lang="ts">
import { ref, h, computed } from 'vue'
import { useRouter } from 'vue-router'
import { NIcon, type GlobalThemeOverrides, darkTheme } from 'naive-ui'

import HandDrawnIcon from '@/components/HandDrawnIcon.vue'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'

// SVG 图标组件
const SearchIcon = {
  render() {
    return h('svg', {
      xmlns: 'http://www.w3.org/2000/svg',
      viewBox: '0 0 512 512',
      width: 16,
      height: 16,
      fill: 'currentColor'
    }, [
      h('path', {
        fill: 'none',
        stroke: 'currentColor',
        'stroke-linecap': 'round',
        'stroke-linejoin': 'round',
        'stroke-width': '32',
        d: 'M221.09 64a157.09 157.09 0 1 0 157.09 157.09A157.1 157.1 0 0 0 221.09 64z'
      }),
      h('path', {
        fill: 'none',
        stroke: 'currentColor',
        'stroke-linecap': 'round',
        'stroke-linejoin': 'round',
        'stroke-width': '32',
        d: 'M338.29 338.29L448 448'
      })
    ])
  }
}

const WriteIcon = {
  render() {
    return h('svg', {
      xmlns: 'http://www.w3.org/2000/svg',
      viewBox: '0 0 24 24',
      width: 16,
      height: 16,
      fill: 'currentColor'
    }, [
      h('path', { d: 'M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z' })
    ])
  }
}

const LogoutIcon = {
  render() {
    return h('svg', {
      xmlns: 'http://www.w3.org/2000/svg',
      viewBox: '0 0 24 24',
      width: 16,
      height: 16,
      fill: 'currentColor'
    }, [
      h('path', { d: 'M17 7l-1.41 1.41L18.17 11H8v2h10.17l-2.58 2.58L17 17l5-5zM4 5h8V3H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h8v-2H4V5z' })
    ])
  }
}

const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()

const searchQuery = ref('')

const themeIcon = computed(() => {
  switch (themeStore.theme) {
    case 'light':
      return {
        render() {
          return h('svg', { xmlns: 'http://www.w3.org/2000/svg', viewBox: '0 0 24 24', width: 18, height: 18, fill: 'currentColor' }, [
            h('circle', { cx: '12', cy: '12', r: '5' }),
            h('line', { x1: '12', y1: '1', x2: '12', y2: '3', stroke: 'currentColor', 'stroke-width': '2' }),
            h('line', { x1: '12', y1: '21', x2: '12', y2: '23', stroke: 'currentColor', 'stroke-width': '2' }),
            h('line', { x1: '4.22', y1: '4.22', x2: '5.64', y2: '5.64', stroke: 'currentColor', 'stroke-width': '2' }),
            h('line', { x1: '18.36', y1: '18.36', x2: '19.78', y2: '19.78', stroke: 'currentColor', 'stroke-width': '2' }),
            h('line', { x1: '1', y1: '12', x2: '3', y2: '12', stroke: 'currentColor', 'stroke-width': '2' }),
            h('line', { x1: '21', y1: '12', x2: '23', y2: '12', stroke: 'currentColor', 'stroke-width': '2' }),
            h('line', { x1: '4.22', y1: '19.78', x2: '5.64', y2: '18.36', stroke: 'currentColor', 'stroke-width': '2' }),
            h('line', { x1: '18.36', y1: '5.64', x2: '19.78', y2: '4.22', stroke: 'currentColor', 'stroke-width': '2' })
          ])
        }
      }
    case 'dark':
      return {
        render() {
          return h('svg', { xmlns: 'http://www.w3.org/2000/svg', viewBox: '0 0 24 24', width: 18, height: 18, fill: 'currentColor' }, [
            h('path', { d: 'M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z' })
          ])
        }
      }
    default:
      return {
        render() {
          return h('svg', { xmlns: 'http://www.w3.org/2000/svg', viewBox: '0 0 24 24', width: 18, height: 18, fill: 'currentColor' }, [
            h('rect', { x: '2', y: '3', width: '20', height: '14', rx: '2', ry: '2' }),
            h('line', { x1: '8', y1: '21', x2: '16', y2: '21', stroke: 'currentColor', 'stroke-width': '2' }),
            h('line', { x1: '12', y1: '17', x2: '12', y2: '21', stroke: 'currentColor', 'stroke-width': '2' })
          ])
        }
      }
  }
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
  position: relative;
  z-index: 10;
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
</style>
