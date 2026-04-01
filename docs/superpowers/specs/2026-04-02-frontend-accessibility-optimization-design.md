# 前端可访问性优化设计方案

## 概述

对博客前端进行完整的可访问性优化，确保所有用户（包括使用键盘、屏幕阅读器等辅助技术的用户）都能良好地使用网站。

## 优化内容

### 1. Skip Link（跳转链接）

**目标**: 让键盘用户快速跳转到主要内容

**实施**: 在 `App.vue` 顶部添加 skip-link

### 2. 焦点样式

**目标**: 确保键盘导航时焦点可见

**实施**: 在 `App.vue` 添加全局 focus-visible 样式

### 3. HandDrawnCard 组件可访问性

**目标**: 卡片组件支持键盘导航

**实施**: 添加 role、tabindex、键盘事件处理

### 4. 按钮 ARIA 属性

**目标**: 屏幕阅读器正确朗读按钮功能

**实施**: back-btn 添加 aria-label

### 5. 文章卡片可访问性

**目标**: 文章卡片支持键盘选择和导航

**实施**: Home.vue 文章卡片添加 aria-label、tabindex

### 6. 评论表单可访问性

**目标**: 表单正确关联标签和错误提示

**实施**: CommentSection.vue 和 ReplyForm.vue 添加 aria 属性

### 7. 图片 alt 属性

**目标**: 屏幕阅读器正确描述图片内容

**实施**: Article.vue 内容区域图片已有占位符，文章内容图片 alt 来自 Markdown

## 涉及文件

| 文件 | 改动类型 |
|------|----------|
| `frontend/src/App.vue` | 修改 |
| `frontend/src/components/HandDrawnCard.vue` | 修改 |
| `frontend/src/views/Article.vue` | 修改 |
| `frontend/src/views/Home.vue` | 修改 |
| `frontend/src/components/CommentSection.vue` | 修改 |
| `frontend/src/components/ReplyForm.vue` | 修改 |

## 预期效果

- 键盘用户可以快速跳转到主要内容
- 所有交互元素可通过 Tab 键导航
- 屏幕阅读器可以正确朗读页面内容
- 表单错误可以被正确 announced

## 优先级

第三批次（后续）
