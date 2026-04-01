# 前端性能优化实现计划

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 降低首屏 JS 体积，改善慢网络下的用户体验

**Architecture:** 路由懒加载已实现，本次优化聚焦于：Vite 拆包、骨架屏、图片懒加载

**Tech Stack:** Vue 3, Vite, Naive UI, VueUse

---

## 已知情况

- 路由懒加载已在 `router/index.ts` 中实现（使用 `() => import()`）
- 无独立 ArticleCard 组件，文章卡片直接在 Home.vue 中用 HandDrawnCard 实现
- 文章内容中的图片在 `Article.vue` 的 `.article-content` 区域内

---

## Chunk 1: Vite 拆包配置

**Files:**
- Modify: `frontend/vite.config.ts`

- [ ] **Step 1: 添加 manualChunks 配置**

修改 `vite.config.ts`，在 `build.rollupOptions.output` 中添加：

```typescript
build: {
  rollupOptions: {
    output: {
      manualChunks: {
        'naive-ui': ['naive-ui'],
        'vue-vendor': ['vue', 'vue-router', 'pinia'],
        'markdown': ['dompurify', 'roughjs'],
      }
    }
  }
}
```

完整配置：
```typescript
import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'naive-ui': ['naive-ui'],
          'vue-vendor': ['vue', 'vue-router', 'pinia'],
          'markdown': ['dompurify', 'roughjs'],
        }
      }
    }
  }
})
```

- [ ] **Step 2: 验证构建**

Run: `cd frontend && npm run build`
Expected: 生成多个 chunk 文件（naive-ui-xxx.js, vue-vendor-xxx.js 等）

---

## Chunk 2: Home.vue 骨架屏

**Files:**
- Modify: `frontend/src/views/Home.vue:41-44`（加载状态部分）

- [ ] **Step 1: 替换 n-spin 为骨架屏**

将第 41-44 行的加载状态：
```vue
<div v-if="loading" class="loading-state">
  <n-spin size="large" />
  <p>加载中...</p>
</div>
```

替换为：
```vue
<div v-if="loading" class="skeleton-container">
  <HandDrawnCard class="skeleton-card">
    <n-skeleton :height="200" :width="'100%'" class="skeleton-img" />
    <div class="skeleton-meta">
      <n-skeleton :width="60" height="20" />
      <n-skeleton :width="80" height="20" />
      <n-skeleton :width="100" height="20" />
    </div>
    <n-skeleton :width="'60%'" height="20" />
    <n-skeleton :width="'80%'" height="16" />
    <n-skeleton :width="'40%'" height="16" />
  </HandDrawnCard>
</div>
```

- [ ] **Step 2: 添加骨架屏样式**

在 `<style scoped>` 中添加：
```css
.skeleton-container {
  margin-bottom: 24px;
}

.skeleton-card {
  width: 100%;
}

.skeleton-img {
  margin-bottom: 16px;
  border-radius: 8px;
}

.skeleton-meta {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}
```

- [ ] **Step 3: 验证**

Run: `cd frontend && npm run dev`
检查加载时是否显示骨架屏而非 spinner

---

## Chunk 3: Article.vue 骨架屏

**Files:**
- Modify: `frontend/src/views/Article.vue:25-32`（加载状态部分）

- [ ] **Step 1: 替换 n-spin 为骨架屏**

将第 25-32 行的加载状态：
```vue
<div v-if="loading" class="loading-state">
  <HandDrawnCard>
    <div class="loading-content">
      <n-spin size="large" />
      <p>加载中...</p>
    </div>
  </HandDrawnCard>
</div>
```

替换为：
```vue
<div v-if="loading" class="skeleton-container">
  <HandDrawnCard>
    <div class="skeleton-content">
      <n-skeleton :width="150" height="40" class="skeleton-title" />
      <div class="skeleton-meta">
        <n-skeleton :width="60" height="24" />
        <n-skeleton :width="80" height="24" />
        <n-skeleton :width="100" height="24" />
      </div>
      <div class="skeleton-body">
        <n-skeleton :width="'100%'" height="20" />
        <n-skeleton :width="'95%'" height="20" />
        <n-skeleton :width="'90%'" height="20" />
        <n-skeleton :width="'60%'" height="20" />
        <n-skeleton :width="'100%'" height="20" />
        <n-skeleton :width="'85%'" height="20" />
      </div>
    </div>
  </HandDrawnCard>
</div>
```

- [ ] **Step 2: 添加骨架屏样式**

在 `<style scoped>` 中添加：
```css
.skeleton-container {
  max-width: 800px;
  margin: 0 auto;
}

.skeleton-content {
  padding: 20px 0;
}

.skeleton-title {
  margin: 0 auto 20px;
}

.skeleton-meta {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-bottom: 32px;
}

.skeleton-body {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
```

- [ ] **Step 3: 验证**

Run: `cd frontend && npm run dev`
导航到文章详情页，检查加载时是否显示骨架屏

---

## Chunk 4: 文章图片懒加载

**Files:**
- Modify: `frontend/src/utils/markdown.ts`（已在 Chunk 1 修复中添加 `data-src` 到白名单）
- Modify: `frontend/src/views/Article.vue`

- [ ] **Step 1: 在 Article.vue 中添加懒加载逻辑**

在 `<script setup>` 中导入并添加：
```typescript
import { useIntersectionObserver } from '@vueuse/core'

// 图片懒加载
const setupLazyImages = () => {
  if (!contentRef.value) return

  const images = contentRef.value.querySelectorAll('img')
  images.forEach((img) => {
    const { stop } = useIntersectionObserver(
      img,
      ([{ isIntersecting }]) => {
        if (isIntersecting) {
          const dataSrc = img.getAttribute('data-src')
          if (dataSrc) {
            img.src = dataSrc
            img.removeAttribute('data-src')
          }
          stop()
        }
      },
      { threshold: 0.1 }
    )
  })
}
```

- [ ] **Step 2: 修改 safeContent，将 src 转为 data-src**

在 `safeContent` computed 中添加正则替换：
```typescript
const safeContent = computed(() => {
  const html = renderMarkdownWithCodeSafe(post.value?.content || '')
  // 将外部图片的 src 转为 data-src（保留 base64 图片的 src）
  return html.replace(/<img([^>]+)src="(https?:\/\/[^"]+)"/g, '<img$1data-src="$2"')
})
```

- [ ] **Step 3: 调用懒加载设置**

在 `fetchPost` 函数中调用：
```typescript
requestAnimationFrame(() => {
  if (contentRef.value) {
    setupCopyButtons(contentRef.value)
    extractHeadings()
    setupScrollObserver()
    setupLazyImages()
  }
})
```

- [ ] **Step 4: 添加 CSS 样式**

```css
.article-content :deep(img) {
  max-width: 100%;
  border-radius: 8px;
  opacity: 0;
  transition: opacity 0.3s ease-in;
}

.article-content :deep(img[src]) {
  opacity: 1;
}
```

- [ ] **Step 5: 验证**

Run: `cd frontend && npm run dev`
检查文章中的图片是否在进入视口后才加载

---

## Chunk 5: 全局进度条（已实现）

**Files:**
- `frontend/src/App.vue` (已有)

**状态**: 已实现。`App.vue` 已使用 `n-loading-bar-provider`，它会监听路由变化自动显示加载进度条。无需额外工作。

---

## 执行顺序

1. Chunk 1: Vite 拆包配置
2. Chunk 2: Home.vue 骨架屏
3. Chunk 3: Article.vue 骨架屏
4. Chunk 4: 文章图片懒加载
5. Chunk 5: 全局进度条（可选）

---

## 验证命令

```bash
cd frontend
npm run build        # 验证构建产物
npm run dev          # 验证开发环境
npm run type-check   # 验证类型
```
