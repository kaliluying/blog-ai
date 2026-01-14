<!--
  TagPosts.vue - 标签文章列表页面组件

  本组件用于展示指定标签下的所有文章
-->
<template>
  <div class="tag-posts-page">
    <HandDrawnBackground />

    <div class="posts-container">
      <HandDrawnCard class="posts-card">
        <div class="tag-header">
          <n-button quaternary @click="router.back()">
            ← 返回
          </n-button>
          <div class="tag-title-wrapper">
            <n-tag size="large" round type="info">
              标签：{{ tag }}
            </n-tag>
            <p class="tag-count">共 {{ filteredPosts.length }} 篇文章</p>
          </div>
        </div>

        <div v-if="loading" class="loading-state">
          <n-spin size="large" />
          <p>加载中...</p>
        </div>

        <div v-else-if="filteredPosts.length === 0" class="empty-state">
          <p>暂无该标签的文章</p>
        </div>

        <div v-else class="posts-list">
          <HandDrawnCard v-for="post in filteredPosts" :key="post.id" :title="post.title" class="post-card">
            <div class="post-meta">
              <n-tag v-for="t in (post.tags || [])" :key="t" size="small" round>
                {{ t }}
              </n-tag>
              <span class="post-date">{{ formatDate(post.date) }}</span>
            </div>
            <p class="post-excerpt">{{ post.excerpt }}</p>
            <n-button quaternary @click="readMore(post.id)">
              阅读更多 →
            </n-button>
          </HandDrawnCard>
        </div>
      </HandDrawnCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { NSpin, NButton, NTag } from 'naive-ui'
import HandDrawnCard from '@/components/HandDrawnCard.vue'
import HandDrawnBackground from '@/components/HandDrawnBackground.vue'
import { useBlogStore } from '@/stores/blog'
import { formatDate } from '@/utils/date'

const router = useRouter()
const route = useRoute()
const blogStore = useBlogStore()

const loading = computed(() => blogStore.loading)
const allPosts = computed(() => blogStore.posts)

const tag = computed(() => route.params.tag as string)

const filteredPosts = computed(() => {
  if (!tag.value) return []
  return allPosts.value.filter(post => {
    const tags = post.tags || []
    return tags.some(t => t.toLowerCase() === tag.value.toLowerCase())
  })
})

const readMore = (id: number) => {
  router.push(`/article/${id}`)
}

onMounted(() => {
  if (allPosts.value.length === 0) {
    blogStore.fetchPosts()
  }
})

watch(() => route.params.tag, () => {
  blogStore.fetchPosts()
})
</script>

<style scoped>
.tag-posts-page {
  position: relative;
  min-height: 100vh;
  padding: 40px 20px;
}

.posts-container {
  position: relative;
  z-index: 1;
  max-width: 800px;
  margin: 0 auto;
}

.posts-card {
  width: 100%;
}

.tag-header {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 24px;
}

.tag-title-wrapper {
  flex: 1;
  text-align: center;
}

.tag-title-wrapper .n-tag {
  font-size: 1.1rem;
}

.tag-count {
  color: #7f8c8d;
  margin: 8px 0 0 0;
  font-size: 0.9rem;
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

.posts-list {
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
</style>
