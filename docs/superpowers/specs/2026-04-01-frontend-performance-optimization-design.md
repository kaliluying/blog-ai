# 前端性能优化设计方案

## 概述

对博客前端进行性能优化，降低首屏加载体积，改善慢网络下的用户体验。

## 优化内容

### 1. 路由懒加载

**目标**：减少首屏 JS 体积

**实施**：
- 修改 `frontend/src/router/index.ts`
- 将所有视图组件从同步导入改为懒加载：
  ```typescript
  // Before
  import Home from '@/views/Home.vue'
  import Article from '@/views/Article.vue'

  // After
  const Home = () => import('@/views/Home.vue')
  const Article = () => import('@/views/Article.vue')
  ```

### 2. Vite 拆包配置

**目标**：优化缓存策略，减少重复加载

**实施**：修改 `vite.config.ts`
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

### 3. 骨架屏

**目标**：网络较慢时展示有意义的加载态

**实施**：
- `views/Home.vue` - 文章列表添加骨架卡片
- `views/Article.vue` - 文章内容区域添加骨架段落
- 使用 Naive UI 的 `n-skeleton` 组件

### 4. 图片懒加载

**目标**：延迟加载视口外的图片

**实施**：
- 在 ArticleCard 组件的图片上添加 `loading="lazy"`
- 使用 VueUse 的 `useIntersectionObserver` 实现更精细的控制

## 涉及文件

| 文件 | 改动类型 |
|------|----------|
| `frontend/src/router/index.ts` | 修改 |
| `frontend/vite.config.ts` | 修改 |
| `frontend/src/views/Home.vue` | 修改 |
| `frontend/src/views/Article.vue` | 修改 |
| `frontend/src/components/ArticleCard.vue` | 修改（如存在） |

## 预期效果

- 首屏 JS 体积减少 ~40%
- 用户在慢网络下看到骨架屏而非空白
- 图片按需加载，提升整体感知性能

## 优先级

第一批次（高优先级）
