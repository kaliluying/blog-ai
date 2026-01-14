<!--
  AdminPosts.vue - 文章管理页面组件

  本组件提供后台文章管理功能，包括：
  1. 文章列表展示
  2. 搜索筛选功能
  3. 删除文章操作
  4. 新建文章入口
-->

<template>
  <!-- 页面容器 -->
  <div class="admin-posts-page">
    <!-- 手绘风格背景 -->
    <HandDrawnBackground />

    <!-- 管理页面容器 -->
    <div class="admin-container">
      <HandDrawnCard class="admin-card">

        <!-- 头部：标题和操作按钮 -->
        <div class="admin-header">
          <h1 class="admin-title">文章管理</h1>
          <div class="header-actions">
            <!-- 搜索框 -->
            <n-input v-model:value="searchKeyword" placeholder="搜索文章..." clearable style="width: 200px">
              <template #prefix>
                <HandDrawnIcon type="star" :size="16" />
              </template>
            </n-input>
            <!-- 新建文章按钮 -->
            <n-button type="primary" @click="router.push('/admin/posts/new')">
              <HandDrawnIcon type="star" :size="18" />
              新建文章
            </n-button>
            <!-- 登出按钮 -->
            <n-button quaternary type="error" @click="handleLogout">
              登出
            </n-button>
          </div>
        </div>

        <!-- 加载状态 -->
        <div v-if="loading" class="loading-state">
          <n-spin size="large" />
          <p>加载中...</p>
        </div>

        <!-- 空状态：无文章时显示 -->
        <div v-else-if="posts.length === 0" class="empty-state">
          <HandDrawnIcon type="star" :size="48" />
          <p>暂无文章，点击新建文章开始创作</p>
        </div>

        <!-- 文章表格 -->
        <n-data-table
          v-else
          :columns="columns"
          :data="paginatedPosts"
          :bordered="false"
          :row-key="(row: BlogPost) => row.id"
          :pagination="paginationConfig"
          :page-sizes="paginationConfig.pageSizes"
          :item-count="filteredPosts.length"
          @update:page="handlePageChange"
          @update:page-size="handlePageSizeChange"
        />

        <!-- 搜索无结果状态 -->
        <div v-if="filteredPosts.length === 0 && posts.length > 0" class="empty-state">
          <HandDrawnIcon type="star" :size="32" />
          <p>没有找到匹配的文章</p>
        </div>

      </HandDrawnCard>
    </div>
  </div>
</template>

<script setup lang="ts">
// 从 vue 导入 Composition API 工具
import { ref, computed, onMounted, watch, h } from 'vue'

// 从 vue-router 导入路由功能
import { useRouter } from 'vue-router'

// 从 naive-ui 导入组件和类型
import { useMessage, NButton, NTag, NSpace, NInput } from 'naive-ui'
import type { DataTableColumns } from 'naive-ui'

// 导入自定义手绘风格组件
import HandDrawnCard from '@/components/HandDrawnCard.vue'
import HandDrawnIcon from '@/components/HandDrawnIcon.vue'
import HandDrawnConfirm from '@/components/HandDrawnConfirm.vue'
import HandDrawnBackground from '@/components/HandDrawnBackground.vue'

// 导入 Store 和 API
import { useBlogStore } from '@/stores/blog'
import { useAdminStore } from '@/stores/auth'
import { blogApi, type BlogPost } from '@/api'
import { formatDate } from '@/utils/date'

// ========== 组合式函数 ==========

// 博客 Store 实例
const blogStore = useBlogStore()

// 管理员认证 Store 实例
const adminStore = useAdminStore()

// 路由实例
const router = useRouter()

// 消息提示实例
const message = useMessage()

// ========== 响应式状态 ==========

// 搜索关键词
const searchKeyword = ref('')

// 从 Store 获取加载状态
const loading = computed(() => blogStore.loading)

// 从 Store 获取文章列表
const posts = computed(() => blogStore.posts)

// ========== 计算属性 ==========

/**
 * 过滤后的文章列表
 * 根据搜索关键词在标题、摘要和标签中进行匹配
 */
const filteredPosts = computed(() => {
  // 如果没有搜索词，返回全部文章
  if (!searchKeyword.value.trim()) {
    return posts.value
  }

  // 将搜索词转为小写（不区分大小写搜索）
  const keyword = searchKeyword.value.toLowerCase()

  // 过滤文章
  return posts.value.filter(post => {
    const tags = post.tags || []
    // 匹配标题
    return post.title.toLowerCase().includes(keyword) ||
      // 匹配摘要
      post.excerpt.toLowerCase().includes(keyword) ||
      // 匹配标签
      tags.some(tag => tag.toLowerCase().includes(keyword))
  })
})

/**
 * 分页后的文章列表（用于表格显示）
 */
const paginatedPosts = computed(() => {
  const data = filteredPosts.value
  const { page, pageSize } = paginationConfig.value
  const start = (page - 1) * pageSize
  const end = start + pageSize
  return data.slice(start, end)
})

// ========== 方法 ==========

/**
 * 处理删除文章
 * @param id 要删除的文章 ID
 */
const handleDelete = async (id: number) => {
  try {
    await blogApi.deletePost(id)
    message.success('删除成功')
    blogStore.fetchPosts()
  } catch {
    message.error('删除失败')
  }
}

/**
 * 管理员登出
 */
const handleLogout = () => {
  adminStore.logout()
}

/**
 * 创建表格列配置
 * 使用 h 函数手动创建 JSX 风格的列渲染
 *
 * @returns 表格列配置数组
 */
const createColumns = (): DataTableColumns<BlogPost> => [
  // ID 列
  {
    title: 'ID',
    key: 'id',
    width: 60
  },
  // 标题列（支持省略显示，可点击跳转）
  {
    title: '标题',
    key: 'title',
    render: (row) => h('span', {
      class: 'title-link',
      onClick: () => router.push(`/article/${row.id}`)
    }, row.title),
    ellipsis: true
  },
  // 标签列（渲染为标签数组）
  {
    title: '标签',
    key: 'tags',
    render: (row) => h(NSpace, () => (row.tags || []).map((tag: string) => h(NTag, { size: 'small', round: true }, () => tag)))
  },
  // 日期列（格式化显示）
  {
    title: '日期',
    key: 'date',
    width: 120,
    render: (row) => formatDate(row.date)
  },
  // 操作列（编辑和删除按钮）
  {
    title: '操作',
    key: 'actions',
    width: 200,
    render: (row) => h(NSpace, () => [
      // 编辑按钮
      h(NButton, {
        size: 'small',
        quaternary: true,
        type: 'primary',
        onClick: () => router.push(`/admin/posts/${row.id}`)
      }, () => '编辑'),
      // 确认删除对话框
      h(HandDrawnConfirm, {
        message: '确定要删除这篇文章吗？',
        onConfirm: () => handleDelete(row.id)
      }, {
        default: () => h(NButton, { size: 'small', quaternary: true, type: 'error' }, () => '删除')
      })
    ])
  }
]

// 创建列配置实例
const columns = createColumns()

// ========== 分页配置 ==========

/**
 * 分页配置
 */
const paginationConfig = ref({
  page: 1,
  pageSize: 10,
  showSizePicker: true,
  pageSizes: [10, 20, 50],
  prefix: (info: { itemCount: number }) => `共 ${info.itemCount} 篇`
})

/**
 * 处理分页变化
 */
const handlePageChange = (page: number) => {
  paginationConfig.value.page = page
}

/**
 * 处理每页数量变化
 */
const handlePageSizeChange = (size: number) => {
  paginationConfig.value.pageSize = size
  paginationConfig.value.page = 1
}

// ========== 生命周期 ==========

// 组件挂载时获取文章列表
onMounted(() => {
  blogStore.fetchPosts()
})

// 监听搜索关键词变化，重置分页
watch(searchKeyword, () => {
  paginationConfig.value.page = 1
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

/* 标题链接样式 */
:deep(.title-link) {
  color: #2c3e50;
  cursor: pointer;
  transition: color 0.2s;
}

:deep(.title-link:hover) {
  color: #3498db;
}
</style>
