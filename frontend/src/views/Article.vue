<template>
  <div class="article-page">
    <HandDrawnBackground />

    <div class="article-container">
      <div v-if="loading" class="loading-state">
        <HandDrawnCard>
          <div class="loading-content">
            <n-spin size="large" />
            <p>加载中...</p>
          </div>
        </HandDrawnCard>
      </div>

      <div v-else-if="error" class="error-state">
        <HandDrawnCard title="加载失败">
          <p>{{ error }}</p>
          <n-button type="primary" @click="fetchPost">重试</n-button>
        </HandDrawnCard>
      </div>

      <HandDrawnCard v-else-if="post" class="article-card">
        <div class="article-header">
          <h1 class="article-title">{{ post.title }}</h1>
          <div class="article-meta">
            <n-tag v-for="tag in post.tags" :key="tag" size="small" round>
              {{ tag }}
            </n-tag>
            <span class="article-date">{{ formatDate(post.date) }}</span>
          </div>
        </div>

        <div class="article-content" ref="contentRef" v-html="renderedContent"></div>

        <div class="article-footer">
          <n-button quaternary @click="router.back()">
            ← 返回首页
          </n-button>
        </div>
      </HandDrawnCard>

      <div v-else class="not-found">
        <HandDrawnCard title="文章不存在">
          <p>抱歉，您要查看的文章不存在。</p>
          <n-button type="primary" @click="router.push('/')">
            返回首页
          </n-button>
        </HandDrawnCard>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUpdated, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMessage } from 'naive-ui'
import HandDrawnCard from '@/components/HandDrawnCard.vue'
import HandDrawnBackground from '@/components/HandDrawnBackground.vue'
import { blogApi, type BlogPost } from '@/api'

const route = useRoute()
const router = useRouter()
const message = useMessage()

const contentRef = ref<HTMLElement | null>(null)
const postId = computed(() => Number(route.params.id))
const post = ref<BlogPost | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

const fetchPost = async () => {
  loading.value = true
  error.value = null
  try {
    post.value = await blogApi.getPost(postId.value)
    await nextTick()
    setupCopyButtons()
  } catch (e) {
    error.value = '获取文章失败'
    console.error(e)
    post.value = null
  } finally {
    loading.value = false
  }
}

onMounted(fetchPost)

onUpdated(() => {
  setupCopyButtons()
})

watch(() => route.params.id, fetchPost)

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// Markdown 渲染函数
const renderMarkdown = (text: string): string => {
  if (!text) return ''

  let html = text
    // 代码块（添加特殊标记以便识别）
    .replace(/```(\w*)\n([\s\S]*?)```/g, (_, lang, code) => {
      // 使用 btoa/atob 进行 base64 编码
      const encodedCode = btoa(unescape(encodeURIComponent(code)))
      return `<pre class="code-block" data-code="${encodedCode}"><code>${code}</code></pre>`
    })
    // 行内代码
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    // 粗体
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    // 斜体
    .replace(/\*([^*]+)\*/g, '<em>$1</em>')
    // 删除线
    .replace(/~~([^~]+)~~/g, '<del>$1</del>')
    // 链接
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>')
    // 引用
    .replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>')
    // 标题
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    // 无序列表
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    // 有序列表
    .replace(/^\d+\. (.+)$/gm, '<li>$1</li>')
    // 段落
    .replace(/\n\n/g, '</p><p>')
    // 换行
    .replace(/\n/g, '<br>')

  return `<p>${html}</p>`
}

const renderedContent = computed(() => renderMarkdown(post.value?.content || ''))

// 为代码块添加复制按钮
const setupCopyButtons = () => {
  if (!contentRef.value) return

  const preList = contentRef.value.querySelectorAll('pre.code-block')
  preList.forEach((pre) => {
    // 检查是否已添加复制按钮
    if (pre.querySelector('.copy-btn')) return

    const encodedCode = pre.dataset.code || ''
    // 使用 atob 解码
    const code = decodeURIComponent(escape(atob(encodedCode)))

    const btn = document.createElement('button')
    btn.className = 'copy-btn'
    btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>'
    btn.title = '复制代码'

    btn.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(code)
        btn.classList.add('copied')
        btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg>'
        message.success('已复制')
        setTimeout(() => {
          btn.classList.remove('copied')
          btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>'
        }, 2000)
      } catch (e) {
        message.error('复制失败')
      }
    })

    pre.appendChild(btn)
  })
}
</script>

<style scoped>
.article-page {
  position: relative;
  min-height: 100vh;
  padding: 40px 20px;
}

.article-container {
  position: relative;
  z-index: 1;
  max-width: 800px;
  margin: 0 auto;
}

.article-card {
  width: 100%;
}

.article-header {
  text-align: center;
}

.article-title {
  font-family: 'Caveat', cursive;
  font-size: 2.5rem;
  color: #2c3e50;
  margin: 0 0 16px 0;
}

.article-meta {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
}

.article-date {
  color: #7f8c8d;
}

.article-content {
  padding: 20px 0;
  line-height: 1.8;
  color: #34495e;
  font-size: 1.1rem;
}

.article-content p {
  margin-bottom: 16px;
}

.article-content :deep(h1),
.article-content :deep(h2),
.article-content :deep(h3) {
  margin: 24px 0 12px;
  color: #2c3e50;
}

.article-content :deep(pre) {
  background: #f5f5f5;
  padding: 16px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 16px 0;
}

.article-content :deep(code) {
  background: #f5f5f5;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Fira Code', 'Consolas', monospace;
  font-size: 0.9em;
}

.article-content :deep(pre code) {
  background: none;
  padding: 0;
}

.article-content :deep(blockquote) {
  margin: 16px 0;
  padding: 8px 16px;
  border-left: 4px solid #3498db;
  background: #f8f8f8;
  color: #666;
}

.article-content :deep(li) {
  margin-left: 24px;
  margin-bottom: 4px;
}

.article-content :deep(del) {
  color: #999;
}

.article-content :deep(a) {
  color: #3498db;
}

.article-content :deep(img) {
  max-width: 100%;
  border-radius: 8px;
}

.article-content :deep(pre) {
  position: relative;
  padding-right: 40px;
}

.article-content :deep(pre .copy-btn) {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 28px;
  height: 28px;
  border: none;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
  transition: all 0.2s;
}

.article-content :deep(pre .copy-btn:hover) {
  background: rgba(0, 0, 0, 0.1);
  color: #333;
}

.article-content :deep(pre .copy-btn.copied) {
  color: #27ae60;
}

.article-footer {
  padding-top: 20px;
}

.not-found {
  display: flex;
  justify-content: center;
}

.loading-state,
.error-state {
  display: flex;
  justify-content: center;
}

.loading-content {
  text-align: center;
  padding: 40px;
}

.loading-content p {
  margin-top: 16px;
  color: #7f8c8d;
}
</style>
