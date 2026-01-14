<!--
  AdminPostNew.vue - 新建/编辑文章页面组件

  本组件提供后台新建和编辑文章功能，包括：
  1. 文章标题、摘要、标签编辑
  2. Markdown 内容编辑（支持实时预览）
  3. 表单验证和提交
  4. 支持编辑模式加载已有文章数据
-->

<template>
  <!-- 页面容器 -->
  <div class="admin-new-page">
    <!-- 手绘风格背景 -->
    <HandDrawnBackground />

    <!-- 管理页面容器 -->
    <div class="admin-container">
      <HandDrawnCard class="admin-card">

        <!-- 页面头部 -->
        <div class="page-header">
          <!-- 返回按钮 -->
          <n-button quaternary @click="router.back()">
            ← 返回
          </n-button>
          <h1 class="page-title">{{ isEditMode ? '编辑文章' : '新建文章' }}</h1>
        </div>

        <!-- 加载状态 -->
        <div v-if="loading" class="loading-state">
          <n-spin size="large" />
          <p>加载中...</p>
        </div>

        <!-- 分隔线 -->
        <HandDrawnDivider />

        <!-- 表单区域 -->
        <div v-if="!loading" class="form-container">
          <!-- 标题输入 -->
          <div class="form-row">
            <span class="form-label">标题</span>
            <n-input v-model:value="formData.title" placeholder="请输入文章标题" size="large"
              :status="titleValidation.exists ? 'error' : undefined" />
            <!-- 标题验证提示 -->
            <div v-if="titleValidation.checking" class="title-validation checking">
              <n-spin size="small" /> 正在检查标题...
            </div>
            <div v-else-if="titleValidation.exists" class="title-validation error">
              ⚠️ {{ titleValidation.message }}
            </div>
            <div v-else-if="titleValidation.message && !titleValidation.checking" class="title-validation success">
              ✓ {{ titleValidation.message }}
            </div>
          </div>

          <!-- 摘要输入 -->
          <div class="form-row">
            <span class="form-label">摘要</span>
            <n-input v-model:value="formData.excerpt" type="textarea" placeholder="请输入文章摘要" :rows="2" />
          </div>

          <!-- 标签输入 -->
          <div class="form-row">
            <span class="form-label">标签</span>
            <n-dynamic-tags v-model:value="formData.tags" />
          </div>

          <!-- 内容编辑/预览 -->
          <div class="form-row">
            <span class="form-label">内容</span>
            <div class="editor-container">
              <!-- 编辑器标签页 -->
              <div class="editor-tabs">
                <n-button :type="editorMode === 'edit' ? 'primary' : 'default'" @click="editorMode = 'edit'"
                  size="small">
                  编辑
                </n-button>
                <n-button :type="editorMode === 'preview' ? 'primary' : 'default'" @click="editorMode = 'preview'"
                  size="small">
                  预览
                </n-button>
              </div>

              <!-- 编辑模式：Markdown 输入框 -->
              <n-input v-if="editorMode === 'edit'" v-model:value="formData.content" type="textarea"
                placeholder="支持 Markdown 语法&#10;&#10;**粗体** *斜体* ~~删除线~~&#10;# 一级标题&#10;## 二级标题&#10;- 列表项&#10;> 引用&#10;`代码`&#10;```代码块```"
                :rows="16" class="markdown-editor" />

              <!-- 预览模式：渲染后的 HTML -->
              <div v-else class="markdown-preview" v-html="renderedContent"></div>
            </div>
          </div>

          <!-- 表单操作按钮 -->
          <div class="form-actions">
            <n-button @click="router.back()">取消</n-button>
            <n-button type="primary" :loading="submitting" @click="handleSubmit">
              {{ isEditMode ? '保存修改' : '发布文章' }}
            </n-button>
          </div>
        </div>

      </HandDrawnCard>
    </div>
  </div>
</template>

<script setup lang="ts">
// 从 vue 导入 Composition API 工具
import { ref, computed, onMounted, watch } from 'vue'

// 从 vue-router 导入路由功能
import { useRouter, useRoute } from 'vue-router'

// 从 naive-ui 导入消息提示和对话框
import { useMessage, useDialog } from 'naive-ui'

// 导入自定义手绘风格组件
import HandDrawnCard from '@/components/HandDrawnCard.vue'
import HandDrawnDivider from '@/components/HandDrawnDivider.vue'
import HandDrawnBackground from '@/components/HandDrawnBackground.vue'

// 导入 API 和工具函数
import { blogApi, type BlogPostCreate, type BlogPostUpdate } from '@/api'
import { renderMarkdownSafe } from '@/utils/markdown'

// 导入 auth store
import { useAuthStore } from '@/stores/auth'

// ========== 类型定义 ==========

type FormData = BlogPostCreate

interface TitleCheckResponse {
  exists: boolean
  message: string
}

// ========== 组合式函数 ==========

// 路由实例
const router = useRouter()

// 路由参数（用于判断是否为编辑模式）
const route = useRoute()

// 消息提示实例
const message = useMessage()

// 对话框实例
const dialog = useDialog()

// 认证状态
const authStore = useAuthStore()

// ========== 辅助函数 ==========

// 显示登录对话框
const showLoginDialog = () => {
  const passwordRef = ref('')

  dialog.create({
    title: '博主登录',
    content: '请输入管理员密码以继续',
    positiveText: '登录',
    negativeText: '返回',
    maskClosable: false,
    onPositiveClick: async () => {
      if (!passwordRef.value) {
        message.warning('请输入密码')
        return false
      }
      const success = await authStore.login(passwordRef.value)
      if (success) {
        message.success('登录成功')
        fetchPost()
      } else {
        message.error(authStore.error || '密码错误')
      }
    },
    onNegativeClick: () => {
      router.back()
    }
  })
}

// ========== 响应式状态 ==========

// 是否为编辑模式
const isEditMode = computed(() => !!route.params.id)

// 文章 ID（编辑模式时使用）
const postId = computed(() => {
  const id = Number(route.params.id)
  return isNaN(id) ? null : id
})

// 加载状态
const loading = ref(false)

// 提交状态（控制按钮 loading）
const submitting = ref(false)

// 编辑器模式：'edit' 编辑模式 | 'preview' 预览模式
const editorMode = ref<'edit' | 'preview'>('edit')

// 表单数据
const formData = ref<FormData>({
  title: '',
  excerpt: '',
  content: '',
  tags: []
})

// 标题验证状态
const titleValidation = ref<{
  checking: boolean
  exists: boolean
  message: string
}>({
  checking: false,
  exists: false,
  message: ''
})

// 防抖定时器
let titleCheckTimer: ReturnType<typeof setTimeout> | null = null

// ========== 计算属性 ==========

/**
 * 渲染后的内容（计算属性）
 * 使用共享的 Markdown 渲染函数并消毒 HTML
 * 当 formData.content 变化时自动重新渲染
 */
const renderedContent = computed(() => {
  if (!formData.value.content) return '<p class="empty-hint">预览区域</p>'
  return renderMarkdownSafe(formData.value.content)
})

/**
 * 获取文章数据（编辑模式使用）
 * 从后端 API 获取单篇文章的数据并填充表单
 */
const fetchPost = async () => {
  // 验证是否为有效的编辑模式
  if (!isEditMode.value || postId.value === null) return

  loading.value = true
  try {
    const post = await blogApi.getPost(postId.value)
    formData.value = {
      title: post.title,
      excerpt: post.excerpt,
      content: post.content,
      tags: post.tags || []
    }
    // 重置标题验证状态
    titleValidation.value = {
      checking: false,
      exists: false,
      message: ''
    }
  } catch (e) {
    message.error('获取文章失败')
    console.error(e)
    router.push('/admin/posts')
  } finally {
    loading.value = false
  }
}

/**
 * 检查标题是否重复
 * 使用防抖避免频繁请求
 */
const checkTitleDuplicate = async () => {
  const title = formData.value.title.trim()

  // 如果标题为空，重置验证状态
  if (!title) {
    titleValidation.value = {
      checking: false,
      exists: false,
      message: ''
    }
    return
  }

  // 设置检查中状态
  titleValidation.value.checking = true

  // 未登录时跳过标题检查
  const token = localStorage.getItem('adminToken')
  if (!token) {
    titleValidation.value = {
      checking: false,
      exists: false,
      message: ''
    }
    return
  }

  try {
    const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
    const response = await fetch(`${apiBaseUrl}/api/posts/check-title`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('adminToken') || ''}`
      },
      body: JSON.stringify({
        title,
        exclude_id: postId.value
      })
    })

    if (response.ok) {
      const data: TitleCheckResponse = await response.json()
      titleValidation.value = {
        checking: false,
        exists: data.exists,
        message: data.message
      }
    } else if (response.status === 401) {
      // 未授权 - 可能是 token 过期
      titleValidation.value = {
        checking: false,
        exists: false,
        message: ''
      }
    } else {
      // 其他错误，不阻断用户操作
      titleValidation.value = {
        checking: false,
        exists: false,
        message: ''
      }
    }
  } catch {
    // 网络错误时忽略，不阻断用户操作
    titleValidation.value = {
      checking: false,
      exists: false,
      message: ''
    }
  }
}

/**
 * 处理表单提交
 * 验证表单数据并调用 API 创建或更新文章
 */
const handleSubmit = async () => {
  // 检查标题是否存在
  if (titleValidation.value.exists) {
    message.warning('标题已存在，请使用其他标题')
    return
  }

  // 表单验证
  if (!formData.value.title || !formData.value.excerpt || !formData.value.content) {
    message.warning('请填写完整信息')
    return
  }

  // 编辑模式下的 ID 验证
  if (isEditMode.value && postId.value === null) {
    message.error('无效的文章 ID')
    return
  }

  // 开始提交
  submitting.value = true

  try {
    if (isEditMode.value) {
      await blogApi.updatePost(postId.value!, formData.value as BlogPostUpdate)
      message.success('文章更新成功')
    } else {
      await blogApi.createPost(formData.value)
      message.success('文章发布成功')
    }
    router.push('/admin/posts')
  } catch (e) {
    message.error(isEditMode.value ? '更新失败' : '发布失败')
    console.error(e)
  } finally {
    submitting.value = false
  }
}

// ========== 监听器 ==========

/**
 * 监听标题变化，使用防抖检查重复
 */
watch(() => formData.value.title, () => {
  // 清除之前的定时器
  if (titleCheckTimer) {
    clearTimeout(titleCheckTimer)
  }

  // 设置新的防抖定时器（500ms 后检查）
  titleCheckTimer = setTimeout(() => {
    checkTitleDuplicate()
  }, 500)
})

// ========== 生命周期 ==========

// 组件挂载时检查登录状态
onMounted(async () => {
  // 初始化 auth store
  if (!authStore.initialized) {
    await authStore.init()
  }

  // 未登录时显示登录对话框
  if (!authStore.isLoggedIn) {
    showLoginDialog()
  } else {
    fetchPost()
  }
})
</script>

<style scoped>
.admin-new-page {
  position: relative;
  min-height: 100vh;
  padding: 40px 20px;
}

.admin-container {
  position: relative;
  z-index: 1;
  max-width: 900px;
  margin: 0 auto;
}

.admin-card {
  width: 100%;
}

.loading-state {
  text-align: center;
  padding: 60px 20px;
  color: #7f8c8d;
}

.loading-state p {
  margin-top: 16px;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 20px;
}

.page-title {
  font-family: 'Caveat', cursive;
  font-size: 2rem;
  color: #2c3e50;
  margin: 0;
}

.form-container {
  padding: 20px 0;
}

.form-row {
  margin-bottom: 24px;
}

.form-label {
  display: block;
  font-weight: 500;
  color: #34495e;
  margin-bottom: 8px;
}

.editor-container {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
}

.editor-tabs {
  display: flex;
  gap: 4px;
  padding: 8px;
  background: #f8f8f8;
  border-bottom: 1px solid #e0e0e0;
}

.markdown-editor {
  :deep(textarea) {
    border: none !important;
    border-radius: 0 !important;
    font-family: 'Fira Code', 'Consolas', monospace;
    font-size: 14px;
    line-height: 1.6;
    resize: vertical;
  }
}

.markdown-preview {
  padding: 20px;
  min-height: 350px;
  max-height: 500px;
  overflow-y: auto;
  background: #fff;
  line-height: 1.8;
}

.markdown-preview :deep(h1),
.markdown-preview :deep(h2),
.markdown-preview :deep(h3) {
  margin: 16px 0 8px;
  color: #2c3e50;
}

.markdown-preview :deep(p) {
  margin: 8px 0;
}

.markdown-preview :deep(pre) {
  background: #f5f5f5;
  padding: 12px;
  border-radius: 4px;
  overflow-x: auto;
}

.markdown-preview :deep(code) {
  background: #f5f5f5;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Fira Code', 'Consolas', monospace;
  font-size: 0.9em;
}

.markdown-preview :deep(blockquote) {
  margin: 8px 0;
  padding: 8px 16px;
  border-left: 4px solid #3498db;
  background: #f8f8f8;
  color: #666;
}

.markdown-preview :deep(li) {
  margin-left: 20px;
}

.markdown-preview :deep(del) {
  color: #999;
}

.markdown-preview :deep(a) {
  color: #3498db;
}

.empty-hint {
  color: #999;
  font-style: italic;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #eee;
}

.title-validation {
  margin-top: 8px;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 6px;

  &.checking {
    color: #7f8c8d;
  }

  &.error {
    color: #e74c3c;
  }

  &.success {
    color: #27ae60;
  }
}
</style>
