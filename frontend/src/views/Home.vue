<!--
  Home.vue - 首页组件

  本组件是博客的首页，包含：
  1. 手绘风格背景
  2. 左侧文章列表区域
  3. 右侧侧边栏（作者信息、公告、标签云、最新文章、网站统计）
-->

<template>
  <!-- 页面容器 -->
  <div class="blog-home">
    <!-- 手绘风格背景组件 -->
    <HandDrawnBackground />

    <!-- 主内容容器：左右两栏布局 -->
    <div class="main-container">

      <!-- ========== 左侧区域：文章列表 ========== -->
      <section class="left-section">

        <!-- Hero 区域：欢迎语 -->
        <section class="hero-section">
          <HandDrawnCard class="hero-card">
            <h1 class="hero-title">欢迎来到我的手绘博客</h1>
            <p class="hero-subtitle">记录想法，分享技术，热爱生活</p>
          </HandDrawnCard>
        </section>

        <!-- 文章列表区域 -->
        <section class="posts-section">
          <h2 class="section-title">
            <HandDrawnIcon type="star" :size="32" />
            最新文章
          </h2>

          <!-- 加载状态 -->
          <div v-if="loading" class="loading-state">
            <n-spin size="large" />
            <p>加载中...</p>
          </div>

          <!-- 文章列表 -->
          <div v-else class="posts-grid">
            <HandDrawnCard v-for="post in posts" :key="post.id" :title="post.title" class="post-card">
              <!-- 文章元信息：标签和日期 -->
              <div class="post-meta">
                <n-tag v-for="tag in (post.tags || [])" :key="tag" size="small" round>
                  {{ tag }}
                </n-tag>
                <span class="post-views">{{ post.view_count || 0 }} 次阅读</span>
                <span class="post-date">{{ formatDate(post.date) }}</span>
              </div>
              <!-- 文章摘要 -->
              <p class="post-excerpt">{{ post.excerpt }}</p>
              <!-- 阅读更多按钮 -->
              <n-button quaternary @click="readMore(post.id)">
                阅读更多 →
              </n-button>
            </HandDrawnCard>
          </div>

          <!-- 空状态：无文章时显示 -->
          <div v-if="!loading && posts.length === 0" class="empty-state">
            <p>暂无文章</p>
          </div>

          <!-- 分页 -->
          <div v-if="totalCount > pageSize" class="pagination-wrapper">
            <n-pagination v-model:page="currentPage" :page-count="Math.ceil(totalCount / pageSize)"
              :page-sizes="[5, 10, 20]" :page-size="pageSize" show-size-picker @update:page="handlePageChange"
              @update:page-size="handlePageSizeChange" />
          </div>
        </section>
      </section>

      <!-- ========== 右侧区域：侧边栏 ========== -->
      <aside class="right-section">

        <!-- 1. 作者信息卡片 -->
        <HandDrawnCard class="info-card">
          <div class="author-info">
            <div class="author-avatar">
              <HandDrawnIcon type="heart" :size="40" />
            </div>
            <div class="author-detail">
              <h3 class="author-name">博主大大</h3>
              <p class="author-bio">热爱编程，专注于AI全栈开发</p>
              <!-- 社交链接 -->
              <div class="social-links">
                <a href="https://github.com/kaliluying" target="_blank" class="social-link" title="GitHub">
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24"
                    fill="currentColor">
                    <path
                      d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
                  </svg>
                </a>
                <a href="mailto:kaliluying@gmail.com" class="social-link" title="邮箱">
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2">
                    <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
                    <polyline points="22,6 12,13 2,6" />
                  </svg>
                </a>
              </div>
            </div>
          </div>
        </HandDrawnCard>

        <!-- 2. 公告卡片 -->
        <HandDrawnCard class="info-card">
          <h3 class="info-title">
            <HandDrawnIcon type="heart" :size="24" />
            公告
          </h3>
          <p class="notice-text">
            欢迎来到我的手绘博客！这里记录了我的学习笔记和生活感悟。
            如果有任何问题，欢迎留言交流。
          </p>
        </HandDrawnCard>

        <!-- 3. 标签云卡片 -->
        <HandDrawnCard class="info-card">
          <h3 class="info-title">
            <HandDrawnIcon type="star" :size="24" />
            标签云
          </h3>
          <div class="tags-cloud">
            <n-tag v-for="tag in allTags" :key="tag" round size="small" class="tag-item" @click="goToTag(tag)">
              {{ tag }}
            </n-tag>
          </div>
        </HandDrawnCard>

        <!-- 4. 热门文章卡片 -->
        <PopularPosts />

        <!-- 5. 最新文章卡片 -->
        <HandDrawnCard class="info-card">
          <h3 class="info-title">
            <HandDrawnIcon type="star" :size="24" />
            最新文章
          </h3>
          <ul class="recent-posts">
            <li v-for="post in recentPosts" :key="post.id" class="recent-post-item" @click="readMore(post.id)">
              <span class="recent-post-title">{{ post.title }}</span>
              <span class="recent-post-date">{{ formatShortDate(post.date) }}</span>
            </li>
          </ul>
        </HandDrawnCard>

        <!-- 6. 文章归档卡片 -->
        <HandDrawnCard class="info-card">
          <h3 class="info-title">
            <HandDrawnIcon type="star" :size="24" />
            文章归档
          </h3>
          <ul class="archive-list">
            <li class="archive-item" @click="router.push('/archive')">
              <span class="archive-link">查看所有归档</span>
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2">
                <polyline points="9 18 15 12 9 6"></polyline>
              </svg>
            </li>
          </ul>
        </HandDrawnCard>

        <!-- 7. 网站统计卡片 -->
        <HandDrawnCard class="info-card">
          <h3 class="info-title">
            <HandDrawnIcon type="star" :size="24" />
            网站统计
          </h3>
          <div class="stats-list">
            <div class="stat-item">
              <span class="stat-label">文章</span>
              <span class="stat-value">{{ posts.length }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">标签</span>
              <span class="stat-value">{{ allTags.length }}</span>
            </div>
          </div>
        </HandDrawnCard>

      </aside>
    </div>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: 'HomePage'
})

// 从 vue 导入 Composition API 工具
import { computed, onMounted } from 'vue'

// 从 vue-router 导入路由功能
import { useRouter } from 'vue-router'

// 从 stores 导入博客状态管理
import { useBlogStore } from '@/stores/blog'

// 分页配置
const POSTS_PER_PAGE = 10

// 导入自定义手绘风格组件
import HandDrawnCard from '@/components/HandDrawnCard.vue'
import HandDrawnIcon from '@/components/HandDrawnIcon.vue'
import HandDrawnBackground from '@/components/HandDrawnBackground.vue'
import PopularPosts from '@/components/PopularPosts.vue'

// 导入共享工具函数
import { formatDate, formatShortDate } from '@/utils/date'

// ========== 组合式函数 ==========

// 路由实例，用于页面跳转
const router = useRouter()

// 博客 Store 实例，用于获取文章数据
const blogStore = useBlogStore()

// ========== 生命周期 ==========

/**
 * 组件挂载时获取文章列表
 * onMounted 是 Vue 的生命周期钩子，在 DOM 渲染完成后执行
 */
onMounted(() => {
  blogStore.fetchPosts(1, POSTS_PER_PAGE)
})

/**
 * 页码改变
 */
const handlePageChange = (page: number) => {
  blogStore.fetchPosts(page, pageSize.value)
}

/**
 * 每页数量改变
 */
const handlePageSizeChange = (size: number) => {
  blogStore.fetchPosts(1, size)
}

// ========== 计算属性 ==========

// 从 Store 获取文章列表（响应式）
const posts = computed(() => blogStore.posts)

// 从 Store 获取加载状态（响应式）
const loading = computed(() => blogStore.loading)

// 从 Store 获取分页状态
const totalCount = computed(() => blogStore.totalCount)
const currentPage = computed(() => blogStore.currentPage)
const pageSize = computed(() => blogStore.pageSize)

/**
 * 获取所有标签（去重）
 * 使用 Set 数据结构自动去重，然后转为数组
 */
const allTags = computed(() => {
  const tags = new Set<string>()
  posts.value.forEach(post => {
    const postTags = post.tags || []
    postTags.forEach(tag => tags.add(tag))
  })
  return Array.from(tags)
})

/**
 * 获取最新文章（前 5 篇）
 * 按日期降序排序后取前 5 条
 */
const recentPosts = computed(() => {
  return [...posts.value]
    // 按日期降序排序（最新的在前）
    .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
    // 取前 5 篇
    .slice(0, 5)
})

// ========== 方法 ==========

/**
 * 阅读更多：跳转到文章详情页
 * @param id 文章 ID
 */
const readMore = (id: number) => {
  router.push(`/article/${id}`)
}

/**
 * 跳转到标签页面
 * @param tag 标签名称
 */
const goToTag = (tag: string) => {
  router.push(`/tag/${encodeURIComponent(tag)}`)
}
</script>

<style scoped>
.blog-home {
  position: relative;
  min-height: 100vh;
  padding: 20px;
}

.main-container {
  position: relative;
  z-index: 1;
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  gap: 32px;
}

.left-section {
  flex: 3;
}

.right-section {
  flex: 1.3;
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-width: 260px;
}

.hero-section {
  display: flex;
  justify-content: center;
  padding: 40px 0;
}

.hero-card {
  width: 100%;
  text-align: center;
}

.hero-title {
  font-family: 'Caveat', cursive;
  font-size: 2.5rem;
  color: var(--text-primary);
  margin: 0 0 12px 0;
}

.hero-subtitle {
  font-size: 1.1rem;
  color: var(--text-secondary);
  margin: 0;
}

.posts-section {
  padding: 20px 0;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-family: 'Caveat', cursive;
  font-size: 2rem;
  color: var(--text-primary);
  margin-bottom: 24px;
}

.posts-grid {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.post-card {
  width: 100%;
}

.post-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.post-date {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-left: auto;
}

.post-views {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.post-excerpt {
  color: var(--text-primary);
  line-height: 1.6;
  margin-bottom: 16px;
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 40px;
  color: var(--text-secondary);
}

.loading-state p,
.empty-state p {
  margin-top: 16px;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 32px;
  padding: 20px 0;
}

.info-card {
  width: 100%;
}

.info-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-family: 'Caveat', cursive;
  font-size: 1.5rem;
  color: var(--text-primary);
  margin: 0 0 16px 0;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.author-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: var(--code-bg);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #e74c3c;
}

.author-name {
  font-size: 1.1rem;
  color: var(--text-primary);
  margin: 0 0 4px 0;
}

.author-bio {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin: 0 0 12px 0;
  line-height: 1.4;
}

.social-links {
  display: flex;
  gap: 12px;
}

.social-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--code-bg);
  color: var(--text-secondary);
  transition: all 0.2s;
}

.social-link:hover {
  background: var(--border-color);
  color: var(--bg-primary);
  transform: translateY(-2px);
}

.social-link.bilibili:hover {
  background: #00A1D6;
}

.stats-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: 8px;
}

.stat-label {
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.stat-value {
  font-family: 'Caveat', cursive;
  font-size: 1.3rem;
  color: var(--text-primary);
  font-weight: bold;
}

.notice-text {
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
  font-size: 0.9rem;
}

.tags-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-item {
  cursor: pointer;
  transition: transform 0.2s;
}

.tag-item:hover {
  transform: scale(1.1) rotate(-2deg);
}

.recent-posts {
  list-style: none;
  padding: 0;
  margin: 0;
}

.recent-post-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px dashed var(--border-color);
  cursor: pointer;
  transition: all 0.2s;
}

.recent-post-item:last-child {
  border-bottom: none;
}

.recent-post-item:hover {
  padding-left: 8px;
}

.recent-post-title {
  flex: 1;
  font-size: 0.9rem;
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.recent-post-date {
  font-size: 0.8rem;
  color: var(--text-secondary);
  margin-left: 12px;
  flex-shrink: 0;
}

.archive-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.archive-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  cursor: pointer;
  transition: all 0.2s;
}

.archive-item:hover {
  padding-left: 8px;
}

.archive-link {
  font-size: 0.9rem;
  color: var(--text-primary);
}

.archive-item:hover .archive-link {
  color: #3498db;
}

.about-text {
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
  font-size: 0.95rem;
}

/* 响应式：小屏幕隐藏右侧 */
@media (max-width: 768px) {
  .main-container {
    flex-direction: column;
  }

  .right-section {
    display: none;
  }
}
</style>
