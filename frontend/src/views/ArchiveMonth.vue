<!--
  ArchiveMonth.vue - 月度归档页面组件

  本组件用于展示指定年月的文章列表
-->
<template>
  <div class="archive-month-page">
    <HandDrawnBackground />

    <div class="archive-container">
      <HandDrawnCard class="archive-card">
        <div class="archive-header">
          <n-button quaternary @click="router.push('/archive')">
            ← 返回归档
          </n-button>
          <h1 class="archive-title">{{ monthTitle }}</h1>
          <p class="archive-subtitle">共 {{ monthData?.post_count || 0 }} 篇文章</p>
        </div>

        <div v-if="loading" class="loading-state">
          <n-spin size="large" />
          <p>加载中...</p>
        </div>

        <div v-else-if="error" class="error-state">
          <p>{{ error }}</p>
          <n-button type="primary" @click="fetchArchive">重试</n-button>
        </div>

        <div v-else-if="monthData" class="posts-list">
          <HandDrawnCard v-for="post in monthData.posts" :key="post.id" :title="post.title" class="post-card">
            <div class="post-meta">
              <n-tag v-for="tag in (post.tags || [])" :key="tag" size="small" round>
                {{ tag }}
              </n-tag>
              <span class="post-date">{{ formatDate(post.date) }}</span>
            </div>
            <p class="post-excerpt">{{ post.excerpt }}</p>
            <n-button quaternary @click="readMore(post.id)">
              阅读更多 →
            </n-button>
          </HandDrawnCard>

          <div v-if="monthData.posts.length === 0" class="empty-state">
            <p>该月份暂无文章</p>
          </div>
        </div>
      </HandDrawnCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { NSpin, NButton, NTag } from 'naive-ui'
import HandDrawnCard from '@/components/HandDrawnCard.vue'
import HandDrawnBackground from '@/components/HandDrawnBackground.vue'
import { archiveApi, type ArchiveGroup } from '@/api'

const router = useRouter()
const route = useRoute()

const monthData = ref<ArchiveGroup | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

const year = computed(() => Number(route.params.year))
const month = computed(() => Number(route.params.month))

const monthTitle = computed(() => {
  const monthNames: Record<number, string> = {
    1: '一月', 2: '二月', 3: '三月', 4: '四月',
    5: '五月', 6: '六月', 7: '七月', 8: '八月',
    9: '九月', 10: '十月', 11: '十一月', 12: '十二月'
  }
  return `${year.value}年 ${monthNames[month.value] || month.value}`
})

const fetchArchive = async () => {
  loading.value = true
  error.value = null

  try {
    monthData.value = await archiveApi.getArchiveByYearMonth(year.value, month.value)
  } catch (e: unknown) {
    error.value = '加载归档失败'
    console.error(e)
  } finally {
    loading.value = false
  }
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const readMore = (id: number) => {
  router.push(`/article/${id}`)
}

onMounted(() => {
  fetchArchive()
})
</script>

<style scoped>
.archive-month-page {
  position: relative;
  min-height: 100vh;
  padding: 40px 20px;
}

.archive-container {
  position: relative;
  z-index: 1;
  max-width: 800px;
  margin: 0 auto;
}

.archive-card {
  width: 100%;
}

.archive-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  margin-bottom: 24px;
  position: relative;
}

.archive-header .n-button {
  position: absolute;
  left: 0;
  top: 8px;
}

.archive-title {
  font-family: 'Caveat', cursive;
  font-size: 2.5rem;
  color: #2c3e50;
  margin: 16px 0 8px 0;
  text-align: center;
}

.archive-subtitle {
  color: #7f8c8d;
  margin: 0;
  text-align: center;
}

.loading-state,
.error-state,
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
