<template>
  <div class="admin-posts-page">
    <HandDrawnBackground />

    <div class="admin-container">
      <HandDrawnCard class="admin-card">
        <div class="admin-header">
          <h1 class="admin-title">文章管理</h1>
          <div class="header-actions">
            <n-input
              v-model:value="searchKeyword"
              placeholder="搜索文章..."
              clearable
              style="width: 200px"
            >
              <template #prefix>
                <HandDrawnIcon type="star" :size="16" />
              </template>
            </n-input>
            <n-button type="primary" @click="router.push('/admin/posts/new')">
              <HandDrawnIcon type="star" :size="18" />
              新建文章
            </n-button>
          </div>
        </div>

        <div v-if="loading" class="loading-state">
          <n-spin size="large" />
          <p>加载中...</p>
        </div>

        <div v-else-if="posts.length === 0" class="empty-state">
          <HandDrawnIcon type="star" :size="48" />
          <p>暂无文章，点击新建文章开始创作</p>
        </div>

        <n-data-table
          v-else
          :columns="columns"
          :data="filteredPosts"
          :bordered="false"
          :row-key="(row: BlogPost) => row.id"
        />

        <div v-if="filteredPosts.length === 0 && posts.length > 0" class="empty-state">
          <HandDrawnIcon type="star" :size="32" />
          <p>没有找到匹配的文章</p>
        </div>
      </HandDrawnCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, h } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage, NButton, NTag, NSpace, NInput } from 'naive-ui'
import type { DataTableColumns } from 'naive-ui'
import HandDrawnCard from '@/components/HandDrawnCard.vue'
import HandDrawnIcon from '@/components/HandDrawnIcon.vue'
import HandDrawnConfirm from '@/components/HandDrawnConfirm.vue'
import HandDrawnBackground from '@/components/HandDrawnBackground.vue'
import { useBlogStore, type BlogPost } from '@/stores/blog'
import { blogApi } from '@/api'

const blogStore = useBlogStore()
const router = useRouter()
const message = useMessage()

const searchKeyword = ref('')

const loading = computed(() => blogStore.loading)
const posts = computed(() => blogStore.posts)

const filteredPosts = computed(() => {
  if (!searchKeyword.value.trim()) {
    return posts.value
  }
  const keyword = searchKeyword.value.toLowerCase()
  return posts.value.filter(post =>
    post.title.toLowerCase().includes(keyword) ||
    post.excerpt.toLowerCase().includes(keyword) ||
    post.tags.some(tag => tag.toLowerCase().includes(keyword))
  )
})

const handleDelete = async (id: number) => {
  try {
    await blogApi.deletePost(id)
    message.success('删除成功')
    blogStore.fetchPosts()
  } catch (e) {
    message.error('删除失败')
  }
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const createColumns = (): DataTableColumns<BlogPost> => [
  {
    title: 'ID',
    key: 'id',
    width: 60
  },
  {
    title: '标题',
    key: 'title',
    ellipsis: true
  },
  {
    title: '标签',
    key: 'tags',
    render: (row) => h(NSpace, () => row.tags.map(tag => h(NTag, { size: 'small', round: true }, () => tag)))
  },
  {
    title: '日期',
    key: 'date',
    width: 120,
    render: (row) => formatDate(row.date)
  },
  {
    title: '操作',
    key: 'actions',
    width: 150,
    render: (row) => h(NSpace, () => [
      h(HandDrawnConfirm, {
        message: '确定要删除这篇文章吗？',
        onConfirm: () => handleDelete(row.id)
      }, {
        default: () => h(NButton, { size: 'small', quaternary: true, type: 'error' }, () => '删除')
      })
    ])
  }
]

const columns = createColumns()

onMounted(() => {
  blogStore.fetchPosts()
})
</script>

<style scoped>
.admin-posts-page {
  position: relative;
  min-height: 100vh;
  padding: 40px 20px;
}

.admin-container {
  position: relative;
  z-index: 1;
  max-width: 1000px;
  margin: 0 auto;
}

.admin-card {
  width: 100%;
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.admin-title {
  font-family: 'Caveat', cursive;
  font-size: 2rem;
  color: #2c3e50;
  margin: 0;
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #7f8c8d;
}

.empty-state p {
  margin-top: 16px;
}

/* 移除表格所有边框 */
:deep(.n-data-table-wrapper) {
  border: none !important;
  background: transparent !important;
}

:deep(.n-data-table-th) {
  background: transparent !important;
  border-bottom: none !important;
  border-right: none !important;
  box-shadow: none !important;
}

:deep(.n-data-table-th::after),
:deep(.n-data-table-th::before) {
  display: none !important;
}

:deep(.n-data-table-td) {
  border-bottom: none !important;
  border-right: none !important;
  box-shadow: none !important;
}

:deep(.n-data-table-tr) {
  border-bottom: none !important;
}

:deep(.n-table) {
  border: none !important;
}

/* 隐藏表格分割线 */
:deep(th + th::before),
:deep(td + td::before) {
  display: none !important;
}

/* 调整表格行间距 */
:deep(.n-data-table-tr) {
  padding: 12px 0 !important;
}

:deep(.n-data-table-td) {
  padding: 12px 8px !important;
}

:deep(.n-data-table-th) {
  padding: 12px 8px !important;
}
</style>
