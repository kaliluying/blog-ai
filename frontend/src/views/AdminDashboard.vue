<!--
  AdminDashboard.vue - 管理后台仪表盘页面

  展示系统统计信息：
  1. 统计卡片（文章数、评论数、阅读量、定时文章）
  2. 月度发布趋势图
  3. 快捷操作入口
-->

<template>
  <div class="admin-dashboard">
    <div class="dashboard-header">
      <h1 class="dashboard-title">仪表盘</h1>
      <p class="dashboard-subtitle">欢迎回来，管理员</p>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-grid">
      <div class="stat-card" v-for="stat in statsCards" :key="stat.key">
        <HandDrawnCard class="stat-card-content">
          <div class="stat-icon" :class="stat.color">
            <HandDrawnIcon :type="stat.icon" :size="32" />
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ formatNumber(stat.value) }}</div>
            <div class="stat-label">{{ stat.label }}</div>
          </div>
        </HandDrawnCard>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="charts-section">
      <div class="chart-card">
        <HandDrawnCard class="chart-card-content">
          <h3 class="chart-title">月度发布趋势</h3>
          <div class="chart-container">
            <div class="bar-chart">
              <div
                v-for="item in monthlyStats"
                :key="item.month"
                class="bar-item"
              >
                <div class="bar-wrapper">
                  <div
                    class="bar"
                    :style="{ height: getBarHeight(item.count) + '%' }"
                  >
                    <span class="bar-value">{{ item.count }}</span>
                  </div>
                </div>
                <div class="bar-label">{{ formatMonth(item.month) }}</div>
              </div>
            </div>
          </div>
        </HandDrawnCard>
      </div>

      <!-- 快捷操作 -->
      <div class="quick-actions-card">
        <HandDrawnCard class="quick-actions-content">
          <h3 class="chart-title">快捷操作</h3>
          <div class="quick-actions-list">
            <n-button
              type="primary"
              block
              @click="router.push('/admin/posts/new')"
            >
              <HandDrawnIcon type="star" :size="18" />
              写新文章
            </n-button>
            <n-button
              block
              @click="router.push('/admin/posts')"
            >
              <HandDrawnIcon type="star" :size="18" />
              管理文章
            </n-button>
            <n-button
              block
              @click="router.push('/admin/comments')"
            >
              <HandDrawnIcon type="star" :size="18" />
              查看评论
            </n-button>
          </div>
        </HandDrawnCard>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { NButton } from 'naive-ui'
import HandDrawnCard from '@/components/HandDrawnCard.vue'
import HandDrawnIcon from '@/components/HandDrawnIcon.vue'
import { adminApi } from '@/api'
import type { DashboardStats } from '@/types'
import { useAdminStore } from '@/stores/auth'

// ========== 响应式状态 ==========

const router = useRouter()
const route = useRoute()
const adminStore = useAdminStore()
const stats = ref<DashboardStats>({
  total_posts: 0,
  total_comments: 0,
  total_views: 0,
  scheduled_posts: 0,
  monthly_posts: []
})
const loading = ref(true)

// ========== 计算属性 ==========

const statsCards = computed(() => [
  {
    key: 'posts',
    label: '文章总数',
    value: stats.value.total_posts,
    icon: 'bookmark' as const,
    color: 'blue'
  },
  {
    key: 'comments',
    label: '评论总数',
    value: stats.value.total_comments,
    icon: 'comment' as const,
    color: 'green'
  },
  {
    key: 'views',
    label: '总阅读量',
    value: stats.value.total_views,
    icon: 'star' as const,
    color: 'orange'
  },
  {
    key: 'scheduled',
    label: '定时发布',
    value: stats.value.scheduled_posts,
    icon: 'tag' as const,
    color: 'purple'
  }
])

const monthlyStats = computed(() => stats.value.monthly_posts)

const maxMonthlyCount = computed(() => {
  const counts = monthlyStats.value.map(m => m.count)
  return Math.max(...counts, 1)
})

// ========== 方法 ==========

const fetchStats = async () => {
  try {
    loading.value = true
    stats.value = await adminApi.getStats()
  } catch (error) {
    console.error('获取统计数据失败:', error)
  } finally {
    loading.value = false
  }
}

const formatNumber = (num: number): string => {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + '万'
  }
  return num.toString()
}

const getBarHeight = (count: number): number => {
  return (count / maxMonthlyCount.value) * 100
}

const formatMonth = (monthStr: string): string => {
  const [, month] = monthStr.split('-')
  return `${month}月`
}

// ========== 生命周期 ==========

onMounted(async () => {
  if (!adminStore.initialized) {
    await adminStore.init()
  }

  if (!adminStore.isLoggedIn) {
    router.replace({ name: 'AdminLogin', query: { redirect: route.fullPath } })
    return
  }

  fetchStats()
})
</script>

<style scoped>
.admin-dashboard {
  padding: 0;
}

.dashboard-header {
  margin-bottom: 32px;
}

.dashboard-title {
  font-family: 'Caveat', cursive;
  font-size: 2.5rem;
  color: var(--text-primary, #2c3e50);
  margin: 0 0 8px 0;
}

.dashboard-subtitle {
  color: var(--text-secondary, #666);
  margin: 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.stat-card-content {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon.blue {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.stat-icon.green {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
  color: white;
}

.stat-icon.orange {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.stat-icon.purple {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-primary, #2c3e50);
  line-height: 1.2;
}

.stat-label {
  font-size: 0.875rem;
  color: var(--text-secondary, #666);
  margin-top: 4px;
}

.charts-section {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
}

.chart-card-content,
.quick-actions-content {
  padding: 24px;
}

.chart-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary, #2c3e50);
  margin: 0 0 20px 0;
}

.chart-container {
  height: 200px;
}

.bar-chart {
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  height: 100%;
  padding-top: 20px;
}

.bar-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  max-width: 60px;
}

.bar-wrapper {
  height: 150px;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  width: 100%;
}

.bar {
  width: 32px;
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
  border-radius: 6px 6px 0 0;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 8px;
  min-height: 4px;
  transition: height 0.3s ease;
  position: relative;
}

.bar-value {
  font-size: 0.75rem;
  color: white;
  font-weight: 600;
  white-space: nowrap;
}

.bar-label {
  margin-top: 8px;
  font-size: 0.75rem;
  color: var(--text-secondary, #666);
}

.quick-actions-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* 暗黑模式适配 */
:global(.dark) .dashboard-title {
  color: var(--text-primary, #e0e0e0);
}

:global(.dark) .dashboard-subtitle {
  color: var(--text-secondary, #a0a0a0);
}

:global(.dark) .stat-value {
  color: var(--text-primary, #e0e0e0);
}

:global(.dark) .stat-label {
  color: var(--text-secondary, #a0a0a0);
}

:global(.dark) .chart-title {
  color: var(--text-primary, #e0e0e0);
}

:global(.dark) .bar-label {
  color: var(--text-secondary, #a0a0a0);
}

/* 响应式 */
@media (max-width: 1024px) {
  .charts-section {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
