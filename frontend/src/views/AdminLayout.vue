<!--
  AdminLayout.vue - 管理后台布局组件

  提供统一的侧边栏导航布局，包含：
  1. 可收缩侧边栏导航
  2. Logo 和品牌名称
  3. 菜单项（仪表盘、文章管理、评论管理）
  4. 登出按钮
-->

<template>
  <div class="admin-layout">
    <!-- 侧边栏 -->
    <aside class="sidebar" :class="{ collapsed: isCollapsed }">
      <!-- Logo 区域 -->
      <div class="sidebar-header">
        <div class="logo">
          <HandDrawnIcon type="star" :size="32" />
          <span v-show="!isCollapsed" class="logo-text">Blog AI</span>
        </div>
        <n-button
          quaternary
          circle
          size="small"
          class="collapse-btn"
          @click="isCollapsed = !isCollapsed"
        >
          <template #icon>
            <n-icon>
              <component :is="isCollapsed ? MenuUnfold : MenuFold" />
            </n-icon>
          </template>
        </n-button>
      </div>

      <!-- 导航菜单 -->
      <nav class="sidebar-nav">
        <n-menu
          :collapsed="isCollapsed"
          :collapsed-width="64"
          :collapsed-icon-size="22"
          :options="menuOptions"
          :value="activeKey"
          @update:value="handleMenuClick"
        />
      </nav>

      <!-- 底部用户信息 -->
      <div class="sidebar-footer">
        <div class="user-info" @click="showUserInfo = true">
          <n-avatar round size="small" class="user-avatar">
            <n-icon><UserIcon /></n-icon>
          </n-avatar>
          <span v-show="!isCollapsed" class="user-name">管理员</span>
        </div>
      </div>
    </aside>

    <!-- 主内容区域 -->
    <main class="main-content">
      <div class="content-wrapper">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, h, defineComponent } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { NMenu, NButton, NIcon, NAvatar } from 'naive-ui'
import type { MenuOption } from 'naive-ui'
import HandDrawnIcon from '@/components/HandDrawnIcon.vue'

// 折叠图标
const MenuFold = defineComponent({
  render: () => h('svg', { viewBox: '0 0 24 24', fill: 'currentColor' }, [
    h('path', { d: 'M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z' })
  ])
})

// 展开图标
const MenuUnfold = defineComponent({
  render: () => h('svg', { viewBox: '0 0 24 24', fill: 'currentColor' }, [
    h('path', { d: 'M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z' })
  ])
})

// 用户图标
const UserIcon = defineComponent({
  render: () => h('svg', { viewBox: '0 0 24 24', fill: 'currentColor' }, [
    h('path', { d: 'M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z' })
  ])
})

// ========== 响应式状态 ==========

const router = useRouter()
const route = useRoute()

const isCollapsed = ref(false)
const showUserInfo = ref(false)

// ========== 计算属性 ==========

const activeKey = computed(() => {
  const path = route.path
  if (path === '/admin' || path === '/admin/dashboard') return 'dashboard'
  if (path.startsWith('/admin/posts')) return 'posts'
  if (path.startsWith('/admin/comments')) return 'comments'
  if (path.startsWith('/admin/settings')) return 'settings'
  return 'dashboard'
})

// ========== 菜单配置 ==========

const menuOptions: MenuOption[] = [
  {
    label: '仪表盘',
    key: 'dashboard',
    icon: () => h(NIcon, null, {
      default: () => h('svg', { viewBox: '0 0 24 24', fill: 'currentColor' }, [
        h('path', { d: 'M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z' })
      ])
    })
  },
  {
    label: '文章管理',
    key: 'posts',
    icon: () => h(NIcon, null, {
      default: () => h('svg', { viewBox: '0 0 24 24', fill: 'currentColor' }, [
        h('path', { d: 'M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z' })
      ])
    })
  },
  {
    label: '评论管理',
    key: 'comments',
    icon: () => h(NIcon, null, {
      default: () => h('svg', { viewBox: '0 0 24 24', fill: 'currentColor' }, [
        h('path', { d: 'M21.99 4c0-1.1-.89-2-1.99-2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14l4 4-.01-18zM18 14H6v-2h12v2zm0-3H6V9h12v2zm0-3H6V6h12v2z' })
      ])
    })
  },
  {
    label: '站点设置',
    key: 'settings',
    icon: () => h(NIcon, null, {
      default: () => h('svg', { viewBox: '0 0 24 24', fill: 'currentColor' }, [
        h('path', { d: 'M19.14 12.94c.04-.31.06-.63.06-.94 0-.31-.02-.63-.06-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.04.31-.06.63-.06.94s.02.63.06.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z' })
      ])
    })
  }
]

// ========== 方法 ==========

const handleMenuClick = (key: string) => {
  switch (key) {
    case 'dashboard':
      router.push('/admin')
      break
    case 'posts':
      router.push('/admin/posts')
      break
    case 'comments':
      router.push('/admin/comments')
      break
    case 'settings':
      router.push('/admin/settings')
      break
  }
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: var(--bg-primary, #f8f9fa);
}

.sidebar {
  width: 260px;
  background: var(--card-bg, #ffffff);
  border-right: 1px solid var(--border-color, #e0e0e0);
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  z-index: 100;
}

.sidebar.collapsed {
  width: 64px;
}

.sidebar-header {
  padding: 20px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border-color, #e0e0e0);
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--text-primary, #2c3e50);
}

.logo-text {
  font-family: 'Caveat', cursive;
  font-size: 1.5rem;
  font-weight: 600;
}

.collapse-btn {
  opacity: 0.7;
  transition: opacity 0.2s;
}

.collapse-btn:hover {
  opacity: 1;
}

.sidebar-nav {
  flex: 1;
  padding: 16px 8px;
  overflow-y: auto;
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid var(--border-color, #e0e0e0);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.user-info:hover {
  background: var(--hover-bg, #f5f5f5);
}

.user-name {
  font-size: 0.875rem;
  color: var(--text-secondary, #666);
}

.main-content {
  flex: 1;
  margin-left: 260px;
  transition: margin-left 0.3s ease;
  min-height: 100vh;
}

.sidebar.collapsed + .main-content,
.sidebar.collapsed ~ .main-content {
  margin-left: 64px;
}

.content-wrapper {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

/* 暗黑模式适配 */
:global(.dark) .sidebar {
  background: var(--card-bg, #1a1a2e);
  border-color: var(--border-color, #2d2d44);
}

:global(.dark) .sidebar-header {
  border-color: var(--border-color, #2d2d44);
}

:global(.dark) .sidebar-footer {
  border-color: var(--border-color, #2d2d44);
}

:global(.dark) .user-info:hover {
  background: var(--hover-bg, #2d2d44);
}

:global(.dark) .user-name {
  color: var(--text-secondary, #a0a0a0);
}

/* 响应式 */
@media (max-width: 768px) {
  .sidebar {
    width: 64px;
  }

  .sidebar .logo-text,
  .sidebar .user-name {
    display: none;
  }

  .main-content {
    margin-left: 64px;
  }
}
</style>
