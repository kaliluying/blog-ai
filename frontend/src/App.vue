<!--
  App.vue - 应用根组件

  本组件是整个 Vue 应用的顶层容器，包含：
  1. Naive UI 组件Provider（配置全局主题和弹窗服务）
  2. 顶部导航栏（Logo 和导航链接）
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

                  <!-- 导航菜单 -->
                  <nav class="nav">
                    <router-link to="/" class="nav-link">首页</router-link>
                    <router-link to="/admin/posts" class="nav-link">管理</router-link>
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
// 导入 Naive UI 的全局主题类型
import { type GlobalThemeOverrides } from 'naive-ui'

// 导入自定义的手绘风格图标组件
import HandDrawnIcon from '@/components/HandDrawnIcon.vue'

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
}

.nav {
  display: flex;
  gap: 24px;
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
