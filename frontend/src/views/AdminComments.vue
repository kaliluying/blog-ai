<!--
  AdminComments.vue - 评论管理页面组件

  提供后台评论管理功能：
  1. 评论列表展示（支持分页）
  2. 搜索筛选功能
  3. 删除评论操作
  4. 查看评论所在文章
-->

<template>
  <div class="admin-comments-page">
    <div class="page-header">
      <h1 class="page-title">评论管理</h1>
      <div class="header-actions">
        <n-input
          v-model:value="searchKeyword"
          placeholder="搜索评论..."
          clearable
          style="width: 240px"
        >
          <template #prefix>
            <HandDrawnIcon type="star" :size="16" />
          </template>
        </n-input>
        <n-button type="primary" @click="handleSearch">
          搜索
        </n-button>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <n-spin size="large" />
      <p>加载中...</p>
    </div>

    <!-- 空状态 -->
    <div v-else-if="comments.length === 0" class="empty-state">
      <HandDrawnIcon type="star" :size="48" />
      <p>暂无评论</p>
    </div>

    <!-- 评论列表 -->
    <div v-else class="comments-list">
      <HandDrawnCard
        v-for="comment in comments"
        :key="comment.id"
        class="comment-card"
      >
        <div class="comment-header">
          <div class="comment-meta">
            <span class="comment-author">{{ comment.nickname }}</span>
            <span class="comment-time">{{ formatDate(comment.created_at) }}</span>
          </div>
          <div class="comment-article">
            来自文章：
            <span
              class="article-link"
              @click="router.push(`/article/${comment.post_id}`)"
            >
              {{ comment.post_title }}
            </span>
          </div>
        </div>
        <div class="comment-content">
          {{ comment.content }}
        </div>
        <div class="comment-actions">
          <n-button
            quaternary
            type="error"
            size="small"
            @click="handleDelete(comment.id)"
          >
            删除
          </n-button>
        </div>
      </HandDrawnCard>
    </div>

    <!-- 分页 -->
    <div v-if="total > 0" class="pagination-wrapper">
      <n-pagination
        v-model:page="page"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50]"
        :total="total"
        show-size-picker
        @update:page="handlePageChange"
        @update:page-size="handlePageSizeChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage, NInput, NButton, NSpin, NPagination } from 'naive-ui'
import HandDrawnCard from '@/components/HandDrawnCard.vue'
import HandDrawnIcon from '@/components/HandDrawnIcon.vue'
import { adminApi } from '@/api'
import { useAdminStore } from '@/stores/auth'
import type { AdminComment } from '@/types'
import { formatDate } from '@/utils/date'

// ========== 响应式状态 ==========

const router = useRouter()
const message = useMessage()
const adminStore = useAdminStore()

const comments = ref<AdminComment[]>([])
const loading = ref(true)
const searchKeyword = ref('')
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)

// ========== 方法 ==========

const fetchComments = async () => {
  try {
    loading.value = true
    const response = await adminApi.getComments(
      (page.value - 1) * pageSize.value,
      pageSize.value,
      undefined,
      searchKeyword.value || undefined
    )
    comments.value = response.comments
    total.value = response.total
  } catch (error) {
    message.error('获取评论失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  page.value = 1
  fetchComments()
}

const handleDelete = async (commentId: number) => {
  try {
    await adminApi.deleteComment(commentId)
    message.success('删除成功')
    fetchComments()
  } catch (error) {
    message.error('删除失败')
    console.error(error)
  }
}

const handlePageChange = (newPage: number) => {
  page.value = newPage
  fetchComments()
}

const handlePageSizeChange = (newSize: number) => {
  pageSize.value = newSize
  page.value = 1
  fetchComments()
}

// ========== 生命周期 ==========

onMounted(async () => {
  if (!adminStore.initialized) {
    await adminStore.init()
  }

  if (!adminStore.isLoggedIn) {
    router.replace({ name: 'AdminLogin', query: { redirect: '/admin/comments' } })
    return
  }

  fetchComments()
})

// 搜索关键词变化时重新获取
let searchTimeout: ReturnType<typeof setTimeout> | null = null
watch(searchKeyword, () => {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    handleSearch()
  }, 300)
})
</script>

<style scoped>
.admin-comments-page {
  padding: 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-title {
  font-family: 'Caveat', cursive;
  font-size: 2rem;
  color: var(--text-primary, #2c3e50);
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-secondary, #666);
}

.empty-state p {
  margin-top: 16px;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.comment-card {
  padding: 20px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
  flex-wrap: wrap;
  gap: 8px;
}

.comment-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.comment-author {
  font-weight: 600;
  color: var(--text-primary, #2c3e50);
}

.comment-time {
  font-size: 0.875rem;
  color: var(--text-secondary, #666);
}

.comment-article {
  font-size: 0.875rem;
  color: var(--text-secondary, #666);
}

.article-link {
  color: #3498db;
  cursor: pointer;
  transition: color 0.2s;
}

.article-link:hover {
  color: #2980b9;
  text-decoration: underline;
}

.comment-content {
  color: var(--text-primary, #2c3e50);
  line-height: 1.6;
  padding: 12px 0;
  border-top: 1px dashed var(--border-color, #e0e0e0);
  border-bottom: 1px dashed var(--border-color, #e0e0e0);
  margin: 12px 0;
}

.comment-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}

/* 暗黑模式适配 */
:global(.dark) .page-title {
  color: var(--text-primary, #e0e0e0);
}

:global(.dark) .comment-author {
  color: var(--text-primary, #e0e0e0);
}

:global(.dark) .comment-time {
  color: var(--text-secondary, #a0a0a0);
}

:global(.dark) .comment-article {
  color: var(--text-secondary, #a0a0a0);
}

:global(.dark) .comment-content {
  color: var(--text-primary, #e0e0e0);
}

:global(.dark) .loading-state,
:global(.dark) .empty-state {
  color: var(--text-secondary, #a0a0a0);
}

/* 响应式 */
@media (max-width: 640px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .header-actions {
    width: 100%;
  }

  .header-actions .n-input {
    flex: 1;
  }

  .comment-header {
    flex-direction: column;
  }
}
</style>
