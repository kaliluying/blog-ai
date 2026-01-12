<template>
  <div class="admin-new-page">
    <HandDrawnBackground />

    <div class="admin-container">
      <HandDrawnCard class="admin-card">
        <div class="page-header">
          <n-button quaternary @click="router.back()">
            ← 返回
          </n-button>
          <h1 class="page-title">新建文章</h1>
        </div>

        <HandDrawnDivider />

        <div class="form-container">
          <div class="form-row">
            <span class="form-label">标题</span>
            <n-input
              v-model:value="formData.title"
              placeholder="请输入文章标题"
              size="large"
            />
          </div>

          <div class="form-row">
            <span class="form-label">摘要</span>
            <n-input
              v-model:value="formData.excerpt"
              type="textarea"
              placeholder="请输入文章摘要"
              :rows="2"
            />
          </div>

          <div class="form-row">
            <span class="form-label">标签</span>
            <n-dynamic-tags v-model:value="formData.tags" />
          </div>

          <div class="form-row">
            <span class="form-label">内容</span>
            <div class="editor-container">
              <div class="editor-tabs">
                <n-button
                  :type="editorMode === 'edit' ? 'primary' : 'default'"
                  @click="editorMode = 'edit'"
                  size="small"
                >
                  编辑
                </n-button>
                <n-button
                  :type="editorMode === 'preview' ? 'primary' : 'default'"
                  @click="editorMode = 'preview'"
                  size="small"
                >
                  预览
                </n-button>
              </div>

              <n-input
                v-if="editorMode === 'edit'"
                v-model:value="formData.content"
                type="textarea"
                placeholder="支持 Markdown 语法&#10;&#10;**粗体** *斜体* ~~删除线~~&#10;# 一级标题&#10;## 二级标题&#10;- 列表项&#10;> 引用&#10;`代码`&#10;```代码块```"
                :rows="16"
                class="markdown-editor"
              />

              <div v-else class="markdown-preview" v-html="renderedContent"></div>
            </div>
          </div>

          <div class="form-actions">
            <n-button @click="router.back()">取消</n-button>
            <n-button type="primary" :loading="submitting" @click="handleSubmit">
              发布文章
            </n-button>
          </div>
        </div>
      </HandDrawnCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage } from 'naive-ui'
import HandDrawnCard from '@/components/HandDrawnCard.vue'
import HandDrawnDivider from '@/components/HandDrawnDivider.vue'
import HandDrawnBackground from '@/components/HandDrawnBackground.vue'
import { blogApi } from '@/api'

const router = useRouter()
const message = useMessage()

const submitting = ref(false)
const editorMode = ref<'edit' | 'preview'>('edit')

const formData = ref({
  title: '',
  excerpt: '',
  content: '',
  tags: [] as string[]
})

// 简单的 Markdown 渲染函数
const renderMarkdown = (text: string): string => {
  if (!text) return '<p class="empty-hint">预览区域</p>'

  let html = text
    // 代码块
    .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
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

const renderedContent = computed(() => renderMarkdown(formData.value.content))

const handleSubmit = async () => {
  if (!formData.value.title || !formData.value.excerpt || !formData.value.content) {
    message.warning('请填写完整信息')
    return
  }

  submitting.value = true
  try {
    await blogApi.createPost(formData.value)
    message.success('文章发布成功')
    router.push('/admin/posts')
  } catch (e) {
    message.error('发布失败')
    console.error(e)
  } finally {
    submitting.value = false
  }
}
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
</style>
