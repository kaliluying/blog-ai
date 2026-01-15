<template>
  <aside class="article-sidebar">
    <!-- 1. 博主信息卡片 -->
    <HandDrawnCard class="sidebar-card">
      <div class="author-info">
        <div class="author-avatar">
          <HandDrawnIcon type="heart" :size="36" />
        </div>
        <div class="author-detail">
          <h3 class="author-name">博主大大</h3>
          <p class="author-bio">热爱编程与绘画，专注于全栈开发</p>
          <div class="social-links">
            <a href="https://github.com/kaliluying" target="_blank" class="social-link" title="GitHub">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path
                  d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
              </svg>
            </a>
            <a href="mailto:kaliluying@gmail.com" class="social-link" title="邮箱">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
                <polyline points="22,6 12,13 2,6" />
              </svg>
            </a>
          </div>
        </div>
      </div>
    </HandDrawnCard>

    <!-- 2. 文章标签卡片 -->
    <HandDrawnCard class="sidebar-card" v-if="tags && tags.length > 0">
      <h3 class="sidebar-title">
        <HandDrawnIcon type="tag" :size="20" />
        文章标签
      </h3>
      <div class="tags-list">
        <n-tag v-for="tag in tags" :key="tag" round size="small" class="tag-item" @click="goToTag(tag)">
          {{ tag }}
        </n-tag>
      </div>
    </HandDrawnCard>

    <!-- 3. 热门文章卡片 -->
    <PopularPosts />
  </aside>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import HandDrawnCard from '@/components/HandDrawnCard.vue'
import HandDrawnIcon from '@/components/HandDrawnIcon.vue'
import PopularPosts from '@/components/PopularPosts.vue'

defineOptions({
  name: 'ArticleSidebar'
})

defineProps<{
  tags: string[]
}>()

const router = useRouter()

const goToTag = (tag: string) => {
  router.push(`/tag/${encodeURIComponent(tag)}`)
}
</script>

<style scoped>
.article-sidebar {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
}

.sidebar-card {
  width: 100%;
  padding: 16px;
}

.sidebar-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-family: 'Caveat', cursive;
  font-size: 1.3rem;
  color: var(--text-primary);
  margin: 0 0 12px 0;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.author-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: var(--code-bg);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #e74c3c;
  flex-shrink: 0;
}

.author-detail {
  flex: 1;
  min-width: 0;
}

.author-name {
  font-size: 1rem;
  color: var(--text-primary);
  margin: 0 0 4px 0;
}

.author-bio {
  font-size: 0.8rem;
  color: var(--text-secondary);
  margin: 0 0 8px 0;
  line-height: 1.4;
}

.social-links {
  display: flex;
  gap: 8px;
}

.social-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
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

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-item {
  cursor: pointer;
  transition: transform 0.2s;
}

.tag-item:hover {
  transform: scale(1.05);
}

@media (max-width: 1024px) {
  .article-sidebar {
    display: none;
  }
}
</style>
