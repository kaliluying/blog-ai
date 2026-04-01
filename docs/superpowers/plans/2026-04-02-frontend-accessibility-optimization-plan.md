# 前端可访问性优化实现计划

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development

**Goal:** 完整可访问性优化 - Skip link、焦点样式、ARIA、表单标签

**Tech Stack:** Vue 3, Naive UI

---

## Chunk 1: Skip Link 和焦点样式

**Files:**
- Modify: `frontend/src/App.vue`

- [ ] **Step 1: 添加 skip-link**

在 App.vue 的 `<template>` 开头（在 `<n-config-provider>` 之前）添加：

```vue
<!-- Skip Link - 键盘导航跳转链接 -->
<a href="#main-content" class="skip-link">跳转到主要内容</a>
```

- [ ] **Step 2: 添加 skip-link CSS**

在 `<style>` 中添加：

```css
.skip-link {
  position: absolute;
  top: -100px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--primary-color, #34495e);
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  z-index: 10000;
  text-decoration: none;
  font-weight: 600;
  transition: top 0.3s;
}

.skip-link:focus {
  top: 10px;
  outline: 3px solid var(--primary-color, #34495e);
  outline-offset: 2px;
}
```

- [ ] **Step 3: 添加全局焦点样式**

在 `<style>` 中添加：

```css
/* 全局焦点样式 - 确保键盘导航可见 */
:focus-visible {
  outline: 3px solid var(--primary-color, #34495e);
  outline-offset: 2px;
}

/* 移除按钮和链接的默认轮廓，使用自定义样式 */
button:focus-visible,
a:focus-visible {
  outline: 3px solid var(--primary-color, #34495e);
  outline-offset: 2px;
}
```

- [ ] **Step 4: 在 main-content 上添加 id**

在 `<main class="main-content">` 添加 id：

```vue
<main id="main-content" class="main-content">
```

---

## Chunk 2: HandDrawnCard 组件可访问性

**Files:**
- Modify: `frontend/src/components/HandDrawnCard.vue`

- [ ] **Step 1: 添加 tabindex 和 role**

修改模板中的 HandDrawnBorder：

```vue
<HandDrawnBorder
  :roughness="2"
  stroke="#34495e"
  class="hand-drawn-card"
  :class="{ 'no-hover': hoverEffect === false }"
  role="article"
  :tabindex="hoverEffect !== false ? 0 : -1"
>
```

- [ ] **Step 2: 添加键盘事件**

```vue
<HandDrawnBorder
  ...
  @keydown.enter="$emit('click')"
  @keydown.space.prevent="$emit('click')"
>
```

---

## Chunk 3: Article.vue back-btn ARIA

**Files:**
- Modify: `frontend/src/views/Article.vue`

- [ ] **Step 1: 添加 aria-label**

将：
```vue
<n-button quaternary @click="router.back()" class="back-btn">
  ← 返回
</n-button>
```

替换为：
```vue
<n-button quaternary @click="router.back()" class="back-btn" aria-label="返回上一页">
  ← 返回
</n-button>
```

---

## Chunk 4: Home.vue 文章卡片 ARIA

**Files:**
- Modify: `frontend/src/views/Home.vue`

- [ ] **Step 1: 添加 aria-label**

将：
```vue
<HandDrawnCard :title="post.title" class="post-card" hover-effect>
```

替换为：
```vue
<HandDrawnCard :title="post.title" class="post-card" hover-effect
  :aria-label="`阅读文章: ${post.title}`"
>
```

---

## Chunk 5: CommentSection.vue 表单 ARIA

**Files:**
- Modify: `frontend/src/components/CommentSection.vue`

- [ ] **Step 1: 添加 aria-label 到表单元素**

需要查看 CommentSection.vue 的具体结构后添加适当的 aria 属性。

---

## Chunk 6: ReplyForm.vue 表单 ARIA

**Files:**
- Modify: `frontend/src/components/ReplyForm.vue`

- [ ] **Step 1: 添加 aria-label 到表单元素**

需要查看 ReplyForm.vue 的具体结构后添加适当的 aria 属性。

---

## 执行顺序

1. Chunk 1: Skip Link 和焦点样式
2. Chunk 2: HandDrawnCard 组件可访问性
3. Chunk 3: Article.vue back-btn ARIA
4. Chunk 4: Home.vue 文章卡片 ARIA
5. Chunk 5: CommentSection.vue 表单 ARIA
6. Chunk 6: ReplyForm.vue 表单 ARIA

---

## 验证命令

```bash
cd frontend
npm run dev
# 使用 Tab 键导航检查焦点是否可见
# 检查 skip-link 是否正常工作
```
