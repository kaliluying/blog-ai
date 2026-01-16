<template>
  <div class="related-posts" v-if="posts.length > 0">
    <HandDrawnCard>
      <template #header>
        <div class="related-header">
          <HandDrawnIcon type="star" :size="20" />
          <span>相关文章</span>
        </div>
      </template>
      <div class="related-list">
        <div v-for="post in posts" :key="post.id" class="related-item" @click="goToPost(post.id)">
          <div class="related-title">{{ post.title }}</div>
          <div class="related-meta">
            <span class="related-date">{{ formatDate(post.date) }}</span>
            <span class="related-views">{{ post.view_count || 0 }} 次阅读</span>
          </div>
        </div>
      </div>
    </HandDrawnCard>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useDebounceFn } from '@vueuse/core'
import { blogApi } from '@/api'
import type { BlogPost } from '@/types'
import { formatDate } from '@/utils/date'
import HandDrawnCard from '@/components/HandDrawnCard.vue'
import HandDrawnIcon from '@/components/HandDrawnIcon.vue'

defineOptions({
  name: 'RelatedPosts'
})

const props = defineProps<{
  postId: number
  tags: string[]
}>()

const router = useRouter()
const posts = ref<BlogPost[]>([])

const fetchRelatedPosts = async () => {
  if (!props.postId || !props.tags || props.tags.length === 0) {
    posts.value = []
    return
  }

  try {
    posts.value = await blogApi.getRelatedPosts(props.postId, 5)
  } catch (e) {
    console.error('获取相关文章失败:', e)
    posts.value = []
  }
}

// 使用防抖避免重复请求
const debouncedFetch = useDebounceFn(fetchRelatedPosts, 300)

const goToPost = (id: number) => {
  router.push(`/article/${id}`)
}

onMounted(() => {
  fetchRelatedPosts()
})

watch(() => props.postId, () => {
  debouncedFetch()
})
</script>

<style scoped>
.related-posts {
  margin-top: 24px;
}

.related-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: var(--text-primary);
  font-family: 'Caveat', cursive;
  font-size: 1.2rem;
}

.related-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.related-item {
  padding: 12px;
  border-radius: 6px;
  background: var(--bg-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

.related-item:hover {
  background: var(--card-bg);
  border-color: var(--border-color);
  transform: translateX(4px);
}

.related-title {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 6px;
  font-size: 1rem;
}

.related-meta {
  display: flex;
  gap: 12px;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

html.dark .related-item {
  background: var(--shadow-color);
}

html.dark .related-item:hover {
  background: var(--card-bg);
}
</style>
