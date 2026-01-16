<!--
  Archive.vue - 文章归档页面组件

  本组件用于展示文章归档，按年份和月份分组展示所有文章
-->
<template>
  <div class="archive-page">
    <HandDrawnBackground />

    <div class="archive-container">
      <HandDrawnCard class="archive-card">
        <div class="archive-header">
          <n-button quaternary @click="router.push('/')">
            ← 返回首页
          </n-button>
          <h1 class="archive-title">文章归档</h1>
          <p class="archive-subtitle">共 {{ totalPostCount }} 篇文章</p>
        </div>

        <div v-if="loading" class="loading-state">
          <n-spin size="large" />
          <p>加载中...</p>
        </div>

        <div v-else-if="error" class="error-state">
          <p>{{ error }}</p>
          <n-button type="primary" @click="fetchArchive">重试</n-button>
        </div>

        <div v-else class="archive-content">
          <n-collapse accordion>
            <n-collapse-item
              v-for="yearData in archiveData"
              :key="yearData.year"
              :title="`${yearData.year} 年`"
              :name="yearData.year"
            >
              <template #header-extra>
                <span class="year-count">{{ yearData.post_count }} 篇</span>
              </template>

              <div class="months-list">
                <div
                  v-for="monthData in yearData.months"
                  :key="monthData.month"
                  class="month-item"
                  @click="goToMonth(yearData.year, monthData.month)"
                >
                  <div class="month-info">
                    <span class="month-name">{{ monthData.month_name }}</span>
                    <span class="month-count">{{ monthData.post_count }} 篇</span>
                  </div>
                  <div class="month-posts">
                    <div
                      v-for="post in monthData.posts.slice(0, 3)"
                      :key="post.id"
                      class="post-item"
                      @click.stop="readMore(post.id)"
                    >
                      <span class="post-title">{{ post.title }}</span>
                    </div>
                    <div
                      v-if="monthData.posts.length > 3"
                      class="more-posts"
                      @click.stop="goToMonth(yearData.year, monthData.month)"
                    >
                      还有 {{ monthData.posts.length - 3 }} 篇...
                    </div>
                  </div>
                </div>
              </div>
            </n-collapse-item>
          </n-collapse>

          <div v-if="archiveData.length === 0" class="empty-state">
            <p>暂无文章</p>
          </div>
        </div>
      </HandDrawnCard>
    </div>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: 'ArchivePage'
})

import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { NSpin, NButton, NCollapse, NCollapseItem } from 'naive-ui'
import HandDrawnCard from '@/components/HandDrawnCard.vue'
import HandDrawnBackground from '@/components/HandDrawnBackground.vue'
import { archiveApi } from '@/api'
import type { ArchiveYear } from '@/types'

const router = useRouter()

const archiveData = ref<ArchiveYear[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

const totalPostCount = computed(() => {
  return archiveData.value.reduce((sum: number, year: ArchiveYear) => sum + year.post_count, 0)
})

const fetchArchive = async () => {
  loading.value = true
  error.value = null

  try {
    archiveData.value = await archiveApi.getArchive()
  } catch (e: unknown) {
    error.value = '加载归档失败'
    console.error(e)
  } finally {
    loading.value = false
  }
}

const readMore = (id: number) => {
  router.push(`/article/${id}`)
}

const goToMonth = (year: number, month: number) => {
  router.push(`/archive/${year}/${month}`)
}

onMounted(() => {
  fetchArchive()
})
</script>

<style scoped>
.archive-page {
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
}

.archive-header .n-button {
  position: absolute;
  left: 16px;
  top: 16px;
}

.archive-title {
  font-family: 'Caveat', cursive;
  font-size: 2.5rem;
  color: #2c3e50;
  margin: 0 0 8px 0;
}

.archive-subtitle {
  color: #7f8c8d;
  margin: 0;
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

.archive-content {
  padding: 16px 0;
}

.year-count {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.months-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.month-item {
  cursor: pointer;
  padding: 12px 16px;
  background: #f8f8f8;
  border-radius: 8px;
  transition: all 0.2s;
}

.month-item:hover {
  background: #f0f0f0;
  transform: translateX(4px);
}

.month-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.month-name {
  font-weight: 500;
  color: #2c3e50;
}

.month-count {
  color: #7f8c8d;
  font-size: 0.85rem;
}

.month-posts {
  padding-left: 8px;
}

.post-item {
  padding: 6px 0;
  cursor: pointer;
  transition: all 0.2s;
}

.post-item:hover {
  color: #3498db;
}

.post-title {
  font-size: 0.9rem;
  color: #34495e;
}

.more-posts {
  padding: 6px 0;
  font-size: 0.85rem;
  color: #95a5a6;
  cursor: pointer;
}

.more-posts:hover {
  color: #3498db;
}

:deep(.n-collapse-item__header) {
  font-size: 1.1rem;
}

:deep(.n-collapse-item__content-inner) {
  padding-top: 12px;
}
</style>
