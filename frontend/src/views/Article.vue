<!--
  Article.vue - 文章详情页组件

  本组件用于展示单篇文章的完整内容，包括：
  1. 文章标题和元信息（标签、日期）
  2. Markdown 格式的文章内容渲染
  3. 代码块复制功能
  4. 文章目录（TOC）
  5. 加载状态、错误状态和不存在状态的友好提示
-->

<template>
  <!-- 页面容器 -->
  <div class="article-page">
    <!-- 手绘风格背景 -->
    <HandDrawnBackground />

    <!-- 文章容器 -->
    <div class="article-container">

      <!-- 1. 加载状态 -->
      <div v-if="loading" class="loading-state">
        <HandDrawnCard>
          <div class="loading-content">
            <n-spin size="large" />
            <p>加载中...</p>
          </div>
        </HandDrawnCard>
      </div>

      <!-- 2. 错误状态 -->
      <div v-else-if="error" class="error-state">
        <HandDrawnCard title="加载失败">
          <p>{{ error }}</p>
          <n-button type="primary" @click="fetchPost">重试</n-button>
        </HandDrawnCard>
      </div>

      <!-- 3. 文章内容 -->
      <template v-else-if="post">
        <div class="article-layout">
          <!-- 左侧：文章主体 -->
          <div class="article-main">
            <HandDrawnCard class="article-card">
              <!-- 文章头部：标题和元信息 -->
              <div class="article-header">
                <n-button quaternary @click="router.back()" class="back-btn">
                  ← 返回
                </n-button>
                <h1 class="article-title">{{ post.title }}</h1>
                <div class="article-meta">
                  <!-- 标签列表 -->
                  <n-tag v-for="tag in (post.tags || [])" :key="tag" size="small" round>
                    {{ tag }}
                  </n-tag>
                  <!-- 阅读量 -->
                  <span class="article-views">{{ post.view_count || 0 }} 次阅读</span>
                  <!-- 发布日期 -->
                  <span class="article-date">{{ formatDate(post.date) }}</span>
                </div>
              </div>

              <!-- 文章内容：使用 v-html 渲染 Markdown 转换后的 HTML（已消毒） -->
              <div class="article-content" ref="contentRef" v-html="safeContent"></div>
            </HandDrawnCard>

            <RelatedPosts v-if="post && post.tags && post.tags.length > 0" :post-id="post.id" :tags="post.tags" />

            <!-- 评论区域 -->
            <CommentSection :post-id="postId" :comments="comments" @refresh="fetchComments" />
          </div>

          <!-- 右侧：目录和侧边栏 -->
          <aside class="article-sidebar">
            <TableOfContents :headings="headings" :active-id="activeHeadingId" @select="scrollToHeading" />
            <ArticleSidebar :tags="post?.tags || []" />
          </aside>
        </div>
      </template>

      <!-- 4. 文章不存在状态 -->
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
// 从 vue 导入 Composition API 工具
import { ref, computed, onMounted, watch, onUnmounted, nextTick } from 'vue'

// 从 vue-router 导入路由功能
import { useRoute, useRouter } from 'vue-router'

// 从 naive-ui 导入消息提示
import { useMessage } from 'naive-ui'

// 导入自定义手绘风格组件
import HandDrawnCard from '@/components/HandDrawnCard.vue'
import HandDrawnBackground from '@/components/HandDrawnBackground.vue'

// 导入 API 和工具函数
import { blogApi, commentApi, type BlogPost, type Comment } from '@/api'
import { renderMarkdownWithCodeSafe, decodeCode } from '@/utils/markdown'
import { formatDate } from '@/utils/date'

// 导入博客 Store（用于记录浏览）
import { useBlogStore } from '@/stores/blog'

// 导入评论组件
import CommentSection from '@/components/CommentSection.vue'

// 导入目录组件
import TableOfContents from '@/components/TableOfContents.vue'

// 导入相关文章组件
import RelatedPosts from '@/components/RelatedPosts.vue'

// 导入侧边栏组件
import ArticleSidebar from '@/components/ArticleSidebar.vue'

// ========== 组件配置 ==========

defineOptions({
  name: 'ArticlePage'
})

// ========== 组合式函数 ==========

// 路由参数（获取文章 ID）
const route = useRoute()

// 路由实例（用于页面导航）
const router = useRouter()

// 消息提示实例
const message = useMessage()

// 博客 Store 实例（用于记录浏览）
const blogStore = useBlogStore()

// ========== 响应式状态 ==========

// 文章内容区域的 DOM 引用
const contentRef = ref<HTMLElement | null>(null)

// 从路由参数获取文章 ID（转为数字类型）
const postId = computed(() => Number(route.params.id))

// 文章数据（可为 null）
const post = ref<BlogPost | null>(null)

// 加载状态
const loading = ref(false)

// 错误信息（可为 null）
const error = ref<string | null>(null)

// 评论列表
const comments = ref<Comment[]>([])

// 目录标题列表
const headings = ref<Array<{ id: string; text: string; level: number }>>([])

// 当前高亮的标题 ID
const activeHeadingId = ref<string>('')

// 滚动观察器
let scrollObserver: IntersectionObserver | null = null

// ========== TOC 方法 ==========

/**
 * 提取文章中的标题
 */
const extractHeadings = () => {
  if (!contentRef.value) return

  headings.value = []
  const elements = contentRef.value.querySelectorAll('h1, h2, h3')

  elements.forEach((el, index) => {
    const id = `heading-${index}`
    el.id = id
    headings.value.push({
      id,
      text: el.textContent || '',
      level: parseInt(el.tagName.charAt(1))
    })
  })
}

/**
 * 设置滚动观察器
 */
const setupScrollObserver = () => {
  // 断开之前的观察器
  if (scrollObserver) {
    scrollObserver.disconnect()
  }

  scrollObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          activeHeadingId.value = entry.target.id
        }
      })
    },
    {
      rootMargin: '-80px 0px -70% 0px',
      threshold: 0
    }
  )

  headings.value.forEach(h => {
    const el = document.getElementById(h.id)
    if (el) scrollObserver?.observe(el)
  })
}

/**
 * 滚动到指定标题
 */
const scrollToHeading = (id: string) => {
  const el = document.getElementById(id)
  if (el) {
    const top = el.getBoundingClientRect().top + window.scrollY - 80
    window.scrollTo({ top, behavior: 'smooth' })
  }
}

/**
 * 清理滚动观察器
 */
const cleanupScrollObserver = () => {
  if (scrollObserver) {
    scrollObserver.disconnect()
    scrollObserver = null
  }
}

// ========== 方法 ==========

/**
 * 获取文章评论
 */
const fetchComments = async () => {
  try {
    comments.value = await commentApi.getComments(postId.value)
  } catch (e) {
    console.error('获取评论失败:', e)
    comments.value = []
  }
}

/**
 * 获取文章详情
 * 从后端 API 获取单篇文章的数据
 */
const fetchPost = async () => {
  loading.value = true   // 开始加载
  error.value = null     // 清空错误

  try {
    // 调用 API 获取文章
    post.value = await blogApi.getPost(postId.value)

    // 获取评论
    await fetchComments()

    // 等待 DOM 更新后设置代码块复制按钮
    await nextTick()
    // 延迟一下确保 v-html 完全渲染
    setTimeout(() => {
      setupCopyButtons()
      extractHeadings()
      setupScrollObserver()
    }, 50)

    // 记录浏览并更新阅读量（在获取文章完成后调用）
    const newViewCount = await blogStore.recordAndGetViewCount(postId.value)
    // 如果 post.value 存在且不在缓存中，手动更新阅读量
    if (post.value) {
      post.value.view_count = newViewCount
    }
  } catch (e) {
    // 获取失败：设置错误信息
    error.value = '获取文章失败'
    console.error(e)
    post.value = null
  } finally {
    loading.value = false  // 结束加载
  }
}

/**
 * 安全渲染后的内容（计算属性）
 * 使用共享的 Markdown 渲染函数并消毒 HTML
 * 当 post 变化时自动重新渲染
 */
const safeContent = computed(() => renderMarkdownWithCodeSafe(post.value?.content || ''))

/**
 * 为代码块添加复制按钮
 * 在 DOM 更新后调用，为所有代码块添加复制功能
 */
const setupCopyButtons = () => {
  if (!contentRef.value) return

  // 获取所有代码块
  const preList = contentRef.value.querySelectorAll('pre.code-block')
  preList.forEach((pre) => {
    // 移除已存在的复制按钮（确保重新创建）
    const existingBtn = pre.querySelector('.copy-btn')
    if (existingBtn) {
      existingBtn.remove()
    }

    // 从 data 属性中获取 base64 编码的代码
    const encodedCode = (pre as HTMLElement).dataset.code || ''
    // 解码 base64
    const code = decodeCode(encodedCode)

    // 创建复制按钮
    const btn = document.createElement('button')
    btn.className = 'copy-btn'
    // SVG 图标：复制图标
    btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>'
    btn.title = '复制代码'

    // 点击复制事件
    const handleClick = async () => {
      try {
        // 使用 Clipboard API 复制代码
        await navigator.clipboard.writeText(code)
        btn.classList.add('copied')
        // 切换为勾号图标
        btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg>'
        message.success('已复制')
        // 2 秒后恢复原图标
        setTimeout(() => {
          btn.classList.remove('copied')
          btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>'
        }, 2000)
      } catch {
        message.error('复制失败')
      }
    }

    btn.addEventListener('click', handleClick)

    // 将按钮添加到代码块
    pre.appendChild(btn)
  })
}

/**
 * 清理复制按钮
 * 在组件卸载时移除所有复制按钮
 */
const cleanupCopyButtons = () => {
  if (!contentRef.value) return
  const btnList = contentRef.value.querySelectorAll('pre .copy-btn')
  btnList.forEach((btn) => btn.remove())
}

// ========== 生命周期 ==========

// 组件挂载时获取文章
onMounted(async () => {
  await fetchPost()  // fetchPost 内部会调用 recordView
})

// 监听路由参数变化（文章 ID 变化时重新获取）
watch(() => route.params.id, async () => {
  post.value = null  // 先清空文章，确保触发更新
  await fetchPost()  // fetchPost 内部会调用 recordView
})

// 组件卸载时清理，防止内存泄漏
onUnmounted(() => {
  cleanupCopyButtons()
  cleanupScrollObserver()
})
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
  max-width: 1200px;
  margin: 0 auto;
}

.article-layout {
  display: grid;
  grid-template-columns: 1fr 260px;
  gap: 32px;
}

.article-main {
  min-width: 0;
}

.article-sidebar {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 260px;
  flex-shrink: 0;
}

.article-card {
  width: 100%;
}

/* 响应式：小屏幕隐藏侧边栏 */
@media (max-width: 1024px) {
  .article-layout {
    grid-template-columns: 1fr;
  }

  .article-sidebar {
    display: none;
  }

  .article-container {
    max-width: 800px;
  }
}

.article-header {
  position: relative;
  text-align: center;
  padding-top: 16px;
}

.back-btn {
  position: absolute;
  left: 0;
  top: 16px;
}

.article-title {
  font-family: 'Caveat', cursive;
  font-size: 2.5rem;
  color: var(--text-primary);
  margin: 16px 0 16px 0;
  padding: 0 60px;
}

.article-meta {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
}

.article-date {
  color: var(--text-secondary);
}

.article-views {
  color: var(--text-secondary);
}

.article-content {
  padding: 20px 0;
  line-height: 1.8;
  color: var(--text-primary);
  font-size: 1.1rem;
}

.article-content p {
  margin-bottom: 16px;
}

.article-content :deep(h1),
.article-content :deep(h2),
.article-content :deep(h3) {
  margin: 24px 0 12px;
  color: var(--text-primary);
}

.article-content :deep(pre) {
  background: var(--code-bg);
  padding: 16px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 16px 0;
}

.article-content :deep(code) {
  background: var(--code-bg);
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
  background: var(--blockquote-bg);
  color: var(--text-secondary);
}

.article-content :deep(li) {
  margin-left: 24px;
  margin-bottom: 4px;
}

.article-content :deep(del) {
  color: var(--text-secondary);
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
  color: var(--text-secondary);
  transition: all 0.2s;
}

.article-content :deep(pre .copy-btn:hover) {
  background: rgba(0, 0, 0, 0.1);
  color: var(--text-primary);
}

.article-content :deep(pre .copy-btn.copied) {
  color: #27ae60;
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
