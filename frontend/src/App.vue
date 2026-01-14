<!--
  App.vue - 应用根组件

  本组件是整个 Vue 应用的顶层容器，包含：
  1. Naive UI 组件Provider（配置全局主题和弹窗服务）
  2. 顶部导航栏（Logo 和导航链接、用户菜单）
  3. 主内容区（路由视图容器）
  4. 底部版权信息
-->

<template>
  <!--
    n-config-provider: Naive UI 全局配置提供者
    theme-overrides: 自定义主题覆盖色和样式
  -->
  <n-config-provider :theme-overrides="themeOverrides">

    <!-- n-message-provider: 全局消息通知提供者 -->
    <n-message-provider>
      <!-- n-notification-provider: 全局通知提供者 -->
      <n-notification-provider>
        <!-- n-dialog-provider: 全局对话框提供者 -->
        <n-dialog-provider>
          <!-- n-loading-bar-provider: 全局加载进度条提供者 -->
          <n-loading-bar-provider>

            <!-- 页面主布局容器 -->
            <div class="blog-layout">

              <!-- 顶部头部区域 -->
              <header class="header">
                <div class="header-content">
                  <!-- Logo 和站点名称（链接到首页） -->
                  <router-link to="/" class="logo">
                    <HandDrawnIcon type="star" :size="28" />
                    <span>手绘博客</span>
                  </router-link>

                  <!-- 搜索框 -->
                  <div class="search-box">
                    <n-input
                      v-model:value="searchQuery"
                      placeholder="搜索文章..."
                      @keyup.enter="handleSearch"
                      clearable
                    >
                      <template #prefix>
                        <n-icon :component="SearchIcon" />
                      </template>
                    </n-input>
                  </div>

                  <!-- 导航菜单 -->
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
import { ref, h } from 'vue'
import { useRouter } from 'vue-router'
import { NIcon, type GlobalThemeOverrides } from 'naive-ui'

import HandDrawnIcon from '@/components/HandDrawnIcon.vue'
import { useAuthStore } from '@/stores/auth'

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

const UserIcon = {
  render() {
    return h('svg', {
      xmlns: 'http://www.w3.org/2000/svg',
      viewBox: '0 0 24 24',
      width: 16,
      height: 16,
      fill: 'currentColor'
    }, [
      h('path', { d: 'M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z' })
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

const searchQuery = ref('')

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
  // 通用颜色配置
  common: {
    primaryColor: '#34495e',        // 主色调：深蓝灰色
    primaryColorHover: '#5d6d7e',   // 主色悬停状态
    primaryColorPressed: '#2c3e50', // 主色按下状态
    borderRadius: '3px',            // 默认圆角
    // 自定义字体：使用手写风格字体
    fontFamily: '"Caveat", "Comic Sans MS", cursive, sans-serif',
    fontFamilyMono: '"Courier New", monospace'
  },
  // 按钮组件样式覆盖
  Button: {
    borderRadiusMedium: '8px 8px 4px 4px',  // 中号按钮圆角（手绘风格不等边）
    borderRadiusSmall: '6px 6px 3px 3px',  // 小号按钮圆角
    fontWeight: '600'                       // 字体加粗
  },
  // 卡片组件样式覆盖
  Card: {
    borderRadius: '12px 12px 8px 8px',  // 卡片圆角
    boxShadow: '2px 2px 0 #34495e'      // 卡片阴影（手绘风格硬阴影）
  },
  // 输入框组件样式覆盖
  Input: {
    borderRadius: '6px 6px 3px 3px'  // 输入框圆角
  },
  // 标签组件样式覆盖
  Tag: {
    borderRadius: '4px 4px 2px 2px'  // 标签圆角
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400;700&display=swap');

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
}

.blog-layout {
  min-height: 100vh;
  background: linear-gradient(135deg, #fefefe 0%, #f5f5dc 100%);
}

.header {
  background: #fff;
  border-bottom: 2px solid #34495e;
  position: relative;
  z-index: 10;
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
  color: #2c3e50;
  font-family: 'Caveat', cursive;
  font-size: 1.5rem;
  font-weight: 700;
  flex-shrink: 0;
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
  color: #34495e;
  font-size: 1.1rem;
  font-weight: 600;
  transition: color 0.2s;
  font-family: inherit;
}

.nav-link:hover {
  color: #5d6d7e;
}

.nav-link.router-link-active {
  color: #2c3e50;
}

.user-name {
  cursor: pointer;
}

.main-content {
  min-height: calc(100vh - 140px);
}

.footer {
  background: #34495e;
  color: #fff;
  text-align: center;
  padding: 20px;
  position: relative;
  z-index: 10;
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
</style>
