<template>
  <n-config-provider :theme-overrides="themeOverrides">
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
                  <nav class="nav">
                    <router-link to="/" class="nav-link">首页</router-link>
                    <router-link to="/admin/posts" class="nav-link">管理</router-link>
                    <router-link to="/about" class="nav-link">关于</router-link>
                  </nav>
                </div>
              </header>

              <main class="main-content">
                <router-view v-slot="{ Component }">
                  <transition name="fade">
                    <component :is="Component" />
                  </transition>
                </router-view>
              </main>

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
import { type GlobalThemeOverrides } from 'naive-ui'
import HandDrawnIcon from '@/components/HandDrawnIcon.vue'

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
