<template>
  <div class="blog-home">
    <HandDrawnBackground />

    <div class="main-container">
      <!-- 左侧：文章列表 -->
      <section class="left-section">
        <section class="hero-section">
          <HandDrawnCard class="hero-card">
            <h1 class="hero-title">欢迎来到我的手绘博客</h1>
            <p class="hero-subtitle">记录想法，分享技术，热爱生活</p>
          </HandDrawnCard>
        </section>

        <section class="posts-section">
          <h2 class="section-title">
            <HandDrawnIcon type="star" :size="32" />
            最新文章
          </h2>

          <div v-if="loading" class="loading-state">
            <n-spin size="large" />
            <p>加载中...</p>
          </div>

          <div v-else class="posts-grid">
            <HandDrawnCard
              v-for="post in posts"
              :key="post.id"
              :title="post.title"
              class="post-card"
            >
              <div class="post-meta">
                <n-tag v-for="tag in post.tags" :key="tag" size="small" round>
                  {{ tag }}
                </n-tag>
                <span class="post-date">{{ formatDate(post.date) }}</span>
              </div>
              <p class="post-excerpt">{{ post.excerpt }}</p>
              <n-button quaternary @click="readMore(post.id)">
                阅读更多 →
              </n-button>
            </HandDrawnCard>
          </div>

          <div v-if="!loading && posts.length === 0" class="empty-state">
            <p>暂无文章</p>
          </div>
        </section>
      </section>

      <!-- 右侧：信息栏 -->
      <aside class="right-section">
        <!-- 作者信息 -->
        <HandDrawnCard class="info-card">
          <div class="author-info">
            <div class="author-avatar">
              <HandDrawnIcon type="heart" :size="40" />
            </div>
            <div class="author-detail">
              <h3 class="author-name">博主大大</h3>
              <p class="author-bio">热爱编程与绘画，专注于全栈开发</p>
              <div class="social-links">
                <a href="https://github.com/kaliluying" target="_blank" class="social-link" title="GitHub">
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                  </svg>
                </a>
                <a href="https://space.bilibili.com/671157361" target="_blank" class="social-link bilibili" title="B站">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="#00A1D6">
                    <path d="M17.813 4.653h.854c1.51.054 2.769.578 3.773 1.574 1.004.996 1.524 2.249 1.574 3.758v6.844c-.05 1.511-.57 2.771-1.574 3.773-.996 1.004-2.264 1.53-3.773 1.582H5.133c-1.51-.052-2.77-.578-3.773-1.574-1.004-.996-1.524-2.262-1.574-3.773V9.987c.05-1.509.57-2.761 1.574-3.758 1.004-.996 2.264-1.52 3.773-1.574h.903l-.903-2.326h-.427c-.904.052-1.606.356-2.107.914-.5.557-.75 1.317-.75 2.277v7.665c0 .96.25 1.72.75 2.278.5.558 1.203.862 2.107.914h.427l.903-2.327h-.903c-1.51-.052-2.77-.578-3.773-1.574-1.004-.996-1.524-2.262-1.574-3.773V9.987c.05-1.509.57-2.761 1.574-3.758 1.004-.996 2.264-1.52 3.773-1.574h.854v2.326h.427c.904.052 1.606.356 2.107.914.5.557.75 1.317.75 2.277v7.665c0 .96-.25 1.72-.75 2.278-.5.558-1.203.862-2.107.914h-.427v2.326h.903c1.51.054 2.769.578 3.773 1.574 1.004.996 1.524 2.249 1.574 3.758v1.82H2.133v-1.82c-.05-1.511-.57-2.771-1.574-3.773-.996-1.004-2.264-1.53-3.773-1.582H1.787c-.904.052-1.606.356-2.107.914-.5.557-.75 1.317-.75 2.277V19.5c0 .96.25 1.72.75 2.278.5.558 1.203.862 2.107.914h14.712c1.51-.052 2.77-.578 3.773-1.574 1.004-.996 1.524-2.262 1.574-3.773V9.987c-.05-1.509-.57-2.761-1.574-3.758-1.004-.996-2.264-1.52-3.773-1.574z"/>
                    <path d="M6 8.5h4v7H6v-7zm7.5-1.5h3v1.5h-3V7z" fill="#fff"/>
                  </svg>
                </a>
                <a href="mailto:kaliluying@gmail.com" class="social-link" title="邮箱">
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                    <polyline points="22,6 12,13 2,6"/>
                  </svg>
                </a>
              </div>
            </div>
          </div>
        </HandDrawnCard>

        <!-- 公告 -->
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

        <!-- 标签云 -->
        <HandDrawnCard class="info-card">
          <h3 class="info-title">
            <HandDrawnIcon type="star" :size="24" />
            标签云
          </h3>
          <div class="tags-cloud">
            <n-tag
              v-for="tag in allTags"
              :key="tag"
              round
              size="small"
              class="tag-item"
            >
              {{ tag }}
            </n-tag>
          </div>
        </HandDrawnCard>

        <!-- 最新文章 -->
        <HandDrawnCard class="info-card">
          <h3 class="info-title">
            <HandDrawnIcon type="star" :size="24" />
            最新文章
          </h3>
          <ul class="recent-posts">
            <li
              v-for="post in recentPosts"
              :key="post.id"
              class="recent-post-item"
              @click="readMore(post.id)"
            >
              <span class="recent-post-title">{{ post.title }}</span>
              <span class="recent-post-date">{{ formatShortDate(post.date) }}</span>
            </li>
          </ul>
        </HandDrawnCard>

        <!-- 网站统计 -->
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
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useBlogStore } from '@/stores/blog'
import HandDrawnCard from '@/components/HandDrawnCard.vue'
import HandDrawnIcon from '@/components/HandDrawnIcon.vue'
import HandDrawnBackground from '@/components/HandDrawnBackground.vue'

const router = useRouter()
const blogStore = useBlogStore()

onMounted(() => {
  blogStore.fetchPosts()
})

const posts = computed(() => blogStore.posts)
const loading = computed(() => blogStore.loading)

const allTags = computed(() => {
  const tags = new Set<string>()
  posts.value.forEach(post => post.tags.forEach(tag => tags.add(tag)))
  return Array.from(tags)
})

const recentPosts = computed(() => {
  return [...posts.value]
    .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
    .slice(0, 5)
})

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const formatShortDate = (date: string) => {
  return new Date(date).toLocaleDateString('zh-CN', {
    month: 'short',
    day: 'numeric'
  })
}

const readMore = (id: number) => {
  router.push(`/article/${id}`)
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
  color: #2c3e50;
  margin: 0 0 12px 0;
}

.hero-subtitle {
  font-size: 1.1rem;
  color: #7f8c8d;
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
  color: #2c3e50;
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
  color: #7f8c8d;
  margin-left: auto;
}

.post-excerpt {
  color: #5d6d7e;
  line-height: 1.6;
  margin-bottom: 16px;
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 40px;
  color: #7f8c8d;
}

.loading-state p,
.empty-state p {
  margin-top: 16px;
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
  color: #2c3e50;
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
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #e74c3c;
}

.author-name {
  font-size: 1.1rem;
  color: #2c3e50;
  margin: 0 0 4px 0;
}

.author-bio {
  font-size: 0.85rem;
  color: #7f8c8d;
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
  background: #f5f5f5;
  color: #666;
  transition: all 0.2s;
}

.social-link:hover {
  background: #34495e;
  color: #fff;
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
  background: #f8f8f8;
  border-radius: 8px;
}

.stat-label {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.stat-value {
  font-family: 'Caveat', cursive;
  font-size: 1.3rem;
  color: #2c3e50;
  font-weight: bold;
}

.notice-text {
  color: #5d6d7e;
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
  border-bottom: 1px dashed #e0e0e0;
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
  color: #34495e;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.recent-post-date {
  font-size: 0.8rem;
  color: #95a5a6;
  margin-left: 12px;
  flex-shrink: 0;
}

.about-text {
  color: #5d6d7e;
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
