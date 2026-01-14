<template>
  <div class="search-page">
    <div class="container">
      <div class="page-header">
        <n-button quaternary @click="router.back()">
          ← 返回
        </n-button>
        <h1 class="page-title">
          搜索结果: "{{ searchQuery }}"
        </h1>
      </div>

      <n-spin :show="loading">
        <div v-if="results.length > 0" class="results">
          <div v-for="post in results" :key="post.id" class="result-item">
            <router-link :to="'/article/' + post.id" class="result-title">
              {{ post.title }}
            </router-link>
            <p class="result-excerpt">{{ post.excerpt }}</p>
            <div class="result-meta">
              <n-tag v-for="tag in (post.tags || [])" :key="tag" size="small">
                {{ tag }}
              </n-tag>
              <span class="result-date">{{ formatShortDate(post.date) }}</span>
            </div>
          </div>
        </div>

        <div v-else-if="!loading" class="no-results">
          <n-empty description="未找到相关文章">
            <template #extra>
              <p>试试其他关键词吧~</p>
              <router-link to="/">
                <n-button type="primary">返回首页</n-button>
              </router-link>
            </template>
          </n-empty>
        </div>
      </n-spin>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { blogApi, type BlogPost } from '@/api'
import { formatShortDate } from '@/utils/date'

defineOptions({
  name: 'SearchPage'
})

const route = useRoute()
const router = useRouter()
const searchQuery = ref('')
const results = ref<BlogPost[]>([])
const loading = ref(false)

const performSearch = async () => {
  const query = route.query.q as string
  if (!query) {
    results.value = []
    return
  }

  searchQuery.value = query
  loading.value = true

  try {
    results.value = await blogApi.searchPosts(query)
  } catch (error) {
    console.error('搜索失败:', error)
    results.value = []
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  performSearch()
})

watch(() => route.query.q, () => {
  performSearch()
})
</script>

<style scoped>
.search-page {
  padding: 40px 20px;
  min-height: calc(100vh - 140px);
}

.container {
  max-width: 800px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 32px;
}

.page-title {
  font-family: 'Caveat', cursive;
  font-size: 2rem;
  color: #2c3e50;
  margin: 0;
  flex: 1;
  text-align: center;
  padding-right: 80px;
}

.results {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.result-item {
  background: #fff;
  padding: 24px;
  border: 2px solid #34495e;
  border-radius: 8px 8px 4px 4px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.result-item:hover {
  transform: translate(-2px, -2px);
  box-shadow: 4px 4px 0 #34495e;
}

.result-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #2c3e50;
  text-decoration: none;
  display: block;
  margin-bottom: 12px;
  font-family: 'Caveat', cursive;
}

.result-title:hover {
  color: #34495e;
}

.result-excerpt {
  color: #666;
  line-height: 1.6;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.result-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.result-date {
  color: #999;
  font-size: 0.9rem;
  margin-left: auto;
}

.no-results {
  text-align: center;
  padding: 60px 20px;
}
</style>
