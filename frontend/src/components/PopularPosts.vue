<!--
  PopularPosts.vue - 热门文章组件

  本组件显示阅读量最高的文章列表。
-->

<template>
  <HandDrawnCard class="info-card">
    <SidebarCardTitle icon="star">热门文章</SidebarCardTitle>
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <n-spin size="small" />
    </div>
    <!-- 文章列表 -->
    <ul v-else-if="posts.length > 0" class="popular-posts">
      <li
        v-for="(post, index) in posts"
        :key="post.id"
        class="popular-post-item"
        @click="readMore(post.id)"
      >
        <span class="popular-post-rank">{{ index + 1 }}</span>
        <div class="popular-post-content">
          <span class="popular-post-title">{{ post.title }}</span>
          <span class="popular-post-views">{{ post.view_count || 0 }} 次阅读</span>
        </div>
      </li>
    </ul>
    <!-- 空状态 -->
    <p v-else class="empty-text">暂无热门文章</p>
  </HandDrawnCard>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useBlogStore } from '@/stores/blog'
import HandDrawnCard from '@/components/HandDrawnCard.vue'
import SidebarCardTitle from '@/components/SidebarCardTitle.vue'

// ========== 组合式函数 ==========

const router = useRouter()
const blogStore = useBlogStore()

// 本地加载状态（避免与其他操作共用全局状态）
const localLoading = ref(false)

// ========== 生命周期 ==========

onMounted(async () => {
  localLoading.value = true
  try {
    await blogStore.fetchPopularPosts(5)
  } finally {
    localLoading.value = false
  }
})

// ========== 计算属性 ==========

const posts = computed(() => blogStore.popularPosts)
const loading = computed(() => localLoading.value)

// ========== 方法 ==========

const readMore = (id: number) => {
  router.push(`/article/${id}`)
}
</script>

<style scoped>
.info-card {
  width: 100%;
}

.loading-state {
  text-align: center;
  padding: 20px;
}

.empty-text {
  color: var(--text-secondary);
  text-align: center;
  margin: 0;
  padding: 20px 0;
}

.popular-posts {
  list-style: none;
  padding: 0;
  margin: 0;
}

.popular-post-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px dashed var(--border-color);
  cursor: pointer;
  transition: all 0.2s;
}

.popular-post-item:last-child {
  border-bottom: none;
}

.popular-post-item:hover {
  padding-left: 8px;
}

.popular-post-rank {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--code-bg);
  border-radius: 50%;
  font-size: 0.8rem;
  font-weight: bold;
  color: var(--text-secondary);
  flex-shrink: 0;
}

/* 前三名使用特殊颜色 */
.popular-post-item:nth-child(1) .popular-post-rank {
  background: #f1c40f;
  color: #fff;
}

.popular-post-item:nth-child(2) .popular-post-rank {
  background: #95a5a6;
  color: #fff;
}

.popular-post-item:nth-child(3) .popular-post-rank {
  background: #e67e22;
  color: #fff;
}

.popular-post-content {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}

.popular-post-title {
  flex: 1;
  font-size: 0.85rem;
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.popular-post-views {
  font-size: 0.75rem;
  color: var(--text-secondary);
  flex-shrink: 0;
}
</style>
