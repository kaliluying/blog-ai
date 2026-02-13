<!--
  CommentSection.vue - 评论组件

  本组件提供文章评论功能，支持：
  1. 匿名评论（无需登录）
  2. 多层级回复（最多支持 3 级）
  3. 昵称自动生成与本地存储
  4. 管理员删除评论
  5. 评论刷新与实时更新
-->

<template>
  <div class="comment-section">
    <h3 class="comment-title">
      <HandDrawnIcon type="comment" :size="24" />
      评论 ({{ comments.length }})
    </h3>

    <!-- 排序控制 -->
    <div class="comment-sort">
      <n-radio-group :value="sortOrder" size="small" @update:value="handleSortChange">
        <n-radio-button value="newest">最新</n-radio-button>
        <n-radio-button value="oldest">最早</n-radio-button>
      </n-radio-group>
    </div>

    <!-- 评论表单（匿名评论） -->
    <div class="comment-form">
      <p class="comment-hint">支持 Markdown 格式，最多支持 3 级回复</p>
      <n-input v-model:value="newComment" type="textarea" placeholder="写下你的评论..." :rows="3" />
      <div class="form-actions">
        <div class="nickname-wrapper">
          <n-input v-model:value="nickname" placeholder="你的昵称" class="nickname-input" :maxlength="50" show-count />
          <n-button text size="small" @click="regenerateNickname" title="重新生成昵称" class="regenerate-btn">
            🎲
          </n-button>
        </div>
        <n-button type="primary" :loading="submitting" :disabled="!canSubmit" @click="handleSubmit">
          发布评论
        </n-button>
      </div>
    </div>

    <!-- 评论列表 -->
    <div v-if="comments.length > 0" class="comment-list">
      <div v-for="comment in comments" :key="comment.id" class="comment-item">
        <div class="comment-header">
          <span class="comment-author">{{ comment.nickname }}</span>
          <span class="comment-date">{{ formatTimeAgo(comment.created_at) }}</span>
        </div>

        <div class="comment-content" v-html="renderMarkdownSafe(comment.content)"></div>

        <div class="comment-actions">
          <n-tooltip trigger="hover">
            <template #trigger>
              <n-button text size="small" @click="showReplyForm(comment.id)">
                回复
              </n-button>
            </template>
            最多支持 3 级回复
          </n-tooltip>
          <n-popconfirm v-if="adminStore.isLoggedIn" positive-text="确认删除" negative-text="取消"
            @positive-click="handleDelete(comment.id)">
            确定要删除这条评论吗？
            <template #trigger>
              <n-button text size="small" type="error">
                删除
              </n-button>
            </template>
          </n-popconfirm>
        </div>

        <!-- 回复表单 -->
        <div v-if="replyingTo === comment.id" class="reply-form">
          <n-input v-model:value="replyContent" type="textarea" placeholder="写下你的回复..." :rows="2" />
          <div class="form-actions">
            <n-button size="small" @click="cancelReply">取消</n-button>
            <n-button type="primary" size="small" :loading="submitting" :disabled="!canReplySubmit"
              @click="handleReply(comment.id)">
              回复
            </n-button>
          </div>
        </div>

        <!-- 回复列表 -->
        <div v-if="comment.replies && comment.replies.length > 0" class="replies">
          <div v-for="reply in comment.replies" :key="reply.id" class="reply-item">
            <div class="reply-header">
              <span class="reply-author">{{ reply.nickname }}</span>
              <span class="reply-date">{{ formatTimeAgo(reply.created_at) }}</span>
            </div>
            <div class="reply-content" v-html="renderMarkdownSafe(reply.content)"></div>
            <div class="reply-actions">
              <n-button text size="small" @click="showReplyForm(reply.id, comment.id)">
                回复
              </n-button>
              <n-popconfirm v-if="adminStore.isLoggedIn" positive-text="确认删除" negative-text="取消"
                @positive-click="handleDelete(reply.id)">
                确定要删除这条评论吗？
                <template #trigger>
                  <n-button text size="small" type="error">
                    删除
                  </n-button>
                </template>
              </n-popconfirm>
            </div>

            <!-- 二级回复表单 -->
            <div v-if="replyingTo === reply.id" class="reply-form">
              <n-input v-model:value="replyContent" type="textarea" placeholder="写下你的回复..." :rows="2" />
              <div class="form-actions">
                <n-button size="small" @click="cancelReply">取消</n-button>
                <n-button type="primary" size="small" :loading="submitting" :disabled="!canReplySubmit"
                  @click="handleReply(reply.id)">
                  回复
                </n-button>
              </div>
            </div>

            <!-- 二级回复列表 -->
            <div v-if="reply.replies && reply.replies.length > 0" class="sub-replies">
              <div v-for="subReply in reply.replies" :key="subReply.id" class="sub-reply-item">
                <div class="sub-reply-header">
                  <span class="sub-reply-author">{{ subReply.nickname }}</span>
                  <span class="sub-reply-date">{{ formatTimeAgo(subReply.created_at) }}</span>
                </div>
                <div class="sub-reply-content" v-html="renderMarkdownSafe(subReply.content)"></div>
                <div class="sub-reply-actions">
                  <n-popconfirm v-if="adminStore.isLoggedIn" positive-text="确认删除" negative-text="取消"
                    @positive-click="handleDelete(subReply.id)">
                    确定要删除这条评论吗？
                    <template #trigger>
                      <n-button text size="small" type="error">
                        删除
                      </n-button>
                    </template>
                  </n-popconfirm>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <n-empty v-else description="暂无评论，快来抢沙发~" />
  </div>
</template>

<script setup lang="ts">
/**
 * 评论组件脚本部分
 *
 * 包含：
 * - 组件属性定义（父组件传递的数据）
 * - 事件定义（向父组件发送的事件）
 * - 评论相关状态管理
 * - 评论操作方法
 */

// 从 vue 导入 Composition API 工具
import { ref, onMounted, computed } from 'vue'

// 从 naive-ui 导入消息提示
import { useMessage } from 'naive-ui'

// 从 stores 导入认证状态管理
import { useAdminStore } from '@/stores/auth'

// 从 api 导入评论 API
import { commentApi } from '@/api'

// 从 types 导入类型定义
import type { Comment } from '@/types'

// 导入手绘风格图标组件
import HandDrawnIcon from '@/components/HandDrawnIcon.vue'

// 导入日期格式化工具
import { formatTimeAgo } from '@/utils/date'

// 导入 Markdown 安全渲染
import { renderMarkdownSafe } from '@/utils/markdown'

// 导入昵称常量
import { generateNickname } from '@/constants/nicknames'

// ========== 组件接口定义 ==========

/**
 * 组件属性
 */
const props = defineProps<{
  postId: number                    // 文章 ID（必填）
  comments: Comment[]               // 评论列表（从父组件传入）
  sortOrder: 'newest' | 'oldest'    // 排序方式
}>()

/**
 * 组件事件
 */
const emit = defineEmits<{
  (e: 'refresh'): void                         // 刷新评论列表事件
  (e: 'sort-change', order: 'newest' | 'oldest'): void  // 排序变化事件
}>()

// ========== 组合式函数 ==========

// 消息提示实例
const message = useMessage()

// 认证 Store 实例（用于判断是否为管理员）
const adminStore = useAdminStore()

// ========== 响应式状态 ==========

// 新评论内容
const newComment = ref('')

// 评论者昵称
const nickname = ref('')

// 回复内容
const replyContent = ref('')

// 当前回复的目标评论 ID
const replyingTo = ref<number | null>(null)

// 当前回复的父评论 ID（用于嵌套回复）
const replyingToParent = ref<number | null>(null)

// 提交状态（控制按钮 loading）
const submitting = ref(false)

// ========== 方法定义 ==========

/**
 * 处理排序方式变化
 * @param order 新的排序方式
 */
const handleSortChange = async (order: 'newest' | 'oldest') => {
  emit('sort-change', order)
}

// ========== 计算属性 ==========

/**
 * 是否可以提交新评论
 * 条件：评论内容和昵称都不为空
 */
const canSubmit = computed(() => {
  return newComment.value.trim() && nickname.value.trim()
})

/**
 * 是否可以提交回复
 * 条件：回复内容不为空
 */
const canReplySubmit = computed(() => {
  return replyContent.value.trim()
})

// ========== 方法定义 ==========

/**
 * 重新生成昵称
 * 并保存到本地存储，显示提示信息
 */
const regenerateNickname = () => {
  nickname.value = generateNickname()
  saveNickname(nickname.value)
  message.info('已生成新昵称')
}

/**
 * 保存昵称到本地存储
 *
 * @param nick 要保存的昵称
 */
const saveNickname = (nick: string) => {
  localStorage.setItem('commentNickname', nick)
}

/**
 * 显示回复表单
 *
 * @param commentId 要回复的评论 ID
 * @param parentId 父评论 ID（可选，用于嵌套回复）
 */
const showReplyForm = (commentId: number, parentId?: number) => {
  replyingTo.value = commentId
  replyingToParent.value = parentId || null
  replyContent.value = ''
}

/**
 * 取消回复
 * 清空回复状态和内容
 */
const cancelReply = () => {
  replyingTo.value = null
  replyingToParent.value = null
  replyContent.value = ''
}

/**
 * 提交新评论
 *
 * 流程：
 * 1. 验证表单数据
 * 2. 调用 API 创建评论
 * 3. 保存昵称到本地
 * 4. 清空表单并触发刷新
 */
const handleSubmit = async () => {
  if (!canSubmit.value) return

  submitting.value = true
  try {
    // 截取最大长度防止超长
    const safeNickname = nickname.value.trim().slice(0, 50)
    const safeContent = newComment.value.trim()
    await commentApi.createComment({
      post_id: props.postId,
      nickname: safeNickname,
      content: safeContent
    })
    // 保存昵称以便下次使用
    saveNickname(nickname.value)
    // 清空评论内容
    newComment.value = ''
    message.success('评论发布成功~')
    // 通知父组件刷新评论列表
    emit('refresh')
  } catch (error) {
    console.error('评论失败:', error)
    message.error('评论失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}

/**
 * 提交回复
 *
 * @param parentId 父评论 ID
 */
const handleReply = async (parentId: number) => {
  if (!canReplySubmit.value) return

  submitting.value = true
  try {
    // 截取最大长度防止超长
    const safeNickname = nickname.value.trim().slice(0, 50)
    const safeContent = replyContent.value.trim()
    await commentApi.createComment({
      post_id: props.postId,
      nickname: safeNickname,
      content: safeContent,
      parent_id: parentId
    })
    // 清空回复表单
    replyContent.value = ''
    replyingTo.value = null
    replyingToParent.value = null
    message.success('回复发布成功~')
    emit('refresh')
  } catch (error) {
    console.error('回复失败:', error)
    message.error('回复失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}

/**
 * 删除评论
 *
 * @param commentId 要删除的评论 ID
 */
const handleDelete = async (commentId: number) => {
  try {
    await commentApi.deleteComment(commentId)
    message.success('评论已删除')
    emit('refresh')
  } catch (error) {
    console.error('删除失败:', error)
    message.error('删除失败，请稍后重试')
  }
}

// ========== 生命周期 ==========

/**
 * 组件挂载时初始化
 *
 * 流程：
 * 1. 初始化 auth store
 * 2. 检查本地存储的昵称
 * 3. 如果没有存储的昵称，生成并保存新昵称
 */
onMounted(async () => {
  if (!adminStore.initialized) {
    await adminStore.init()
  }
  const storedNickname = localStorage.getItem('commentNickname')
  if (storedNickname) {
    nickname.value = storedNickname
  } else {
    nickname.value = generateNickname()
    saveNickname(nickname.value)
  }
})
</script>

<style scoped>
.comment-section {
  margin-top: 40px;
  padding-top: 24px;
  border-top: 2px solid var(--border-color);
}

.comment-title {
  font-family: 'Caveat', cursive;
  font-size: 1.5rem;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}

.comment-sort {
  margin-bottom: 20px;
}

.comment-form {
  margin-bottom: 24px;
}

.comment-hint {
  font-size: 0.85rem;
  color: var(--text-tertiary);
  margin-bottom: 12px;
}

.form-actions {
  margin-top: 12px;
  display: flex;
  gap: 12px;
  align-items: center;
}

.nickname-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nickname-input {
  width: 180px;
}

.regenerate-btn {
  font-size: 18px;
  padding: 4px 8px;
  transition: transform 0.2s;
}

.regenerate-btn:hover {
  transform: rotate(180deg);
}

.loading-state {
  display: flex;
  justify-content: center;
  padding: 20px;
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.comment-item {
  padding: 16px;
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: 6px 6px 3px 3px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.comment-author {
  font-weight: 600;
  color: var(--text-primary);
}

.comment-date {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.comment-content {
  line-height: 1.6;
  color: var(--text-primary);
}

.comment-actions {
  margin-top: 12px;
  display: flex;
  gap: 12px;
}

.reply-form {
  margin-top: 12px;
  padding: 12px;
  background: var(--card-bg);
  border: 1px dashed var(--border-color);
  border-radius: 4px;
}

.reply-form .form-actions {
  margin-top: 8px;
  gap: 8px;
  justify-content: flex-end;
}

.replies {
  margin-top: 16px;
  padding-left: 24px;
  border-left: 2px solid var(--border-color);
}

.reply-item {
  padding: 12px;
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  margin-bottom: 12px;
}

.reply-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.reply-author {
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--text-primary);
}

.reply-date {
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.reply-content {
  line-height: 1.5;
  font-size: 0.95rem;
  color: var(--text-primary);
}

.reply-actions {
  margin-top: 8px;
  display: flex;
  gap: 12px;
}

.sub-replies {
  margin-top: 12px;
  padding-left: 16px;
  border-left: 2px solid var(--border-color);
}

.sub-reply-item {
  padding: 8px;
  background: var(--card-bg);
  border-radius: 4px;
  margin-bottom: 8px;
}

.sub-reply-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.sub-reply-author {
  font-weight: 600;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.sub-reply-date {
  font-size: 0.75rem;
  color: var(--text-tertiary);
}

.sub-reply-content {
  line-height: 1.4;
  font-size: 0.9rem;
  color: var(--text-primary);
}

.sub-reply-actions {
  margin-top: 6px;
}
</style>
