<template>
  <div class="comment-section">
    <h3 class="comment-title">
      <HandDrawnIcon type="comment" :size="24" />
      评论 ({{ comments.length }})
    </h3>

    <!-- 加载中状态 -->
    <div v-if="!authStore.initialized" class="loading-state">
      <n-spin size="small" />
    </div>

    <!-- 评论表单 -->
    <div v-else-if="authStore.isLoggedIn" class="comment-form">
      <n-input
        v-model:value="newComment"
        type="textarea"
        placeholder="写下你的评论..."
        :rows="3"
      />
      <div class="form-actions">
        <n-button
          type="primary"
          :loading="submitting"
          :disabled="!newComment.trim()"
          @click="handleSubmit"
        >
          发布评论
        </n-button>
      </div>
    </div>

    <div v-else class="login-prompt">
      <n-alert type="info" :show-icon="true">
        <router-link to="/login">登录</router-link> 后才能发表评论
      </n-alert>
    </div>

    <!-- 评论列表 -->
    <div v-if="comments.length > 0" class="comment-list">
      <div v-for="comment in comments" :key="comment.id" class="comment-item">
        <div class="comment-header">
          <span class="comment-author">{{ comment.username }}</span>
          <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
        </div>

        <div class="comment-content">{{ comment.content }}</div>

        <div class="comment-actions">
          <n-button text size="small" @click="showReplyForm(comment.id)">
            回复
          </n-button>
          <n-popconfirm
            v-if="canDelete(comment)"
            positive-text="确认删除"
            negative-text="取消"
            @positive-click="handleDelete(comment.id)"
          >
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
          <n-input
            v-model:value="replyContent"
            type="textarea"
            placeholder="写下你的回复..."
            :rows="2"
          />
          <div class="form-actions">
            <n-button size="small" @click="cancelReply">取消</n-button>
            <n-button
              type="primary"
              size="small"
              :loading="submitting"
              :disabled="!replyContent.trim()"
              @click="handleReply(comment.id)"
            >
              回复
            </n-button>
          </div>
        </div>

        <!-- 回复列表 -->
        <div v-if="comment.replies && comment.replies.length > 0" class="replies">
          <div v-for="reply in comment.replies" :key="reply.id" class="reply-item">
            <div class="reply-header">
              <span class="reply-author">{{ reply.username }}</span>
              <span class="reply-date">{{ formatDate(reply.created_at) }}</span>
            </div>
            <div class="reply-content">{{ reply.content }}</div>
            <div class="reply-actions">
              <n-button text size="small" @click="showReplyForm(reply.id, comment.id)">
                回复
              </n-button>
              <n-popconfirm
                v-if="canDelete(reply)"
                positive-text="确认删除"
                negative-text="取消"
                @positive-click="handleDelete(reply.id)"
              >
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
              <n-input
                v-model:value="replyContent"
                type="textarea"
                placeholder="写下你的回复..."
                :rows="2"
              />
              <div class="form-actions">
                <n-button size="small" @click="cancelReply">取消</n-button>
                <n-button
                  type="primary"
                  size="small"
                  :loading="submitting"
                  :disabled="!replyContent.trim()"
                  @click="handleReply(reply.id)"
                >
                  回复
                </n-button>
              </div>
            </div>

            <!-- 二级回复列表 -->
            <div v-if="reply.replies && reply.replies.length > 0" class="sub-replies">
              <div v-for="subReply in reply.replies" :key="subReply.id" class="sub-reply-item">
                <div class="sub-reply-header">
                  <span class="sub-reply-author">{{ subReply.username }}</span>
                  <span class="sub-reply-date">{{ formatDate(subReply.created_at) }}</span>
                </div>
                <div class="sub-reply-content">{{ subReply.content }}</div>
                <div class="sub-reply-actions">
                  <n-popconfirm
                    v-if="canDelete(subReply)"
                    positive-text="确认删除"
                    negative-text="取消"
                    @positive-click="handleDelete(subReply.id)"
                  >
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage, NPopconfirm } from 'naive-ui'
import { useAuthStore } from '@/stores/auth'
import { commentApi, type Comment } from '@/api'
import HandDrawnIcon from '@/components/HandDrawnIcon.vue'
import { formatDate } from '@/utils/date'

const props = defineProps<{
  postId: number
  comments: Comment[]
}>()

const emit = defineEmits<{
  (e: 'refresh'): void
}>()

const router = useRouter()
const message = useMessage()
const authStore = useAuthStore()

const newComment = ref('')
const replyContent = ref('')
const replyingTo = ref<number | null>(null)
const replyingToParent = ref<number | null>(null)
const submitting = ref(false)

// 组件挂载时等待 auth 初始化完成
onMounted(async () => {
  if (!authStore.initialized) {
    await authStore.init()
  }
})

const canDelete = (comment: Comment) => {
  return authStore.isAdmin || comment.user_id === authStore.user?.id
}

const showReplyForm = (commentId: number, parentId?: number) => {
  if (!authStore.isLoggedIn) {
    message.warning('请先登录后再回复')
    router.push('/login')
    return
  }
  replyingTo.value = commentId
  replyingToParent.value = parentId || null
  replyContent.value = ''
}

const cancelReply = () => {
  replyingTo.value = null
  replyingToParent.value = null
  replyContent.value = ''
}

const handleSubmit = async () => {
  if (!newComment.value.trim()) return
  if (!authStore.isLoggedIn) {
    message.warning('请先登录')
    router.push('/login')
    return
  }

  submitting.value = true
  try {
    await commentApi.createComment(props.postId, newComment.value)
    newComment.value = ''
    message.success('评论发布成功~')
    emit('refresh')
  } catch (e: any) {
    if (e.response?.status === 401) {
      message.warning('请先登录')
      router.push('/login')
    } else {
      message.error('评论失败，请稍后重试')
    }
  } finally {
    submitting.value = false
  }
}

const handleReply = async (parentId: number) => {
  if (!replyContent.value.trim()) return
  if (!authStore.isLoggedIn) {
    message.warning('请先登录')
    router.push('/login')
    return
  }

  submitting.value = true
  try {
    await commentApi.createComment(props.postId, replyContent.value, parentId)
    replyContent.value = ''
    replyingTo.value = null
    replyingToParent.value = null
    message.success('回复发布成功~')
    emit('refresh')
  } catch (e: any) {
    if (e.response?.status === 401) {
      message.warning('请先登录')
      router.push('/login')
    } else {
      message.error('回复失败，请稍后重试')
    }
  } finally {
    submitting.value = false
  }
}

const handleDelete = async (commentId: number) => {
  try {
    await commentApi.deleteComment(commentId)
    message.success('评论已删除')
    emit('refresh')
  } catch (error) {
    message.error('删除失败，请稍后重试')
  }
}
</script>

<style scoped>
.comment-section {
  margin-top: 40px;
  padding-top: 24px;
  border-top: 2px solid #34495e;
}

.comment-title {
  font-family: 'Caveat', cursive;
  font-size: 1.5rem;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 24px;
}

.comment-form {
  margin-bottom: 24px;
}

.form-actions {
  margin-top: 12px;
  display: flex;
  justify-content: flex-end;
}

.login-prompt {
  margin-bottom: 24px;
}

.login-prompt a {
  color: #34495e;
  font-weight: 600;
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
  background: #fafafa;
  border: 1px solid #e0e0e0;
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
  color: #2c3e50;
}

.comment-date {
  font-size: 0.85rem;
  color: #999;
}

.comment-content {
  line-height: 1.6;
  color: #333;
}

.comment-actions {
  margin-top: 12px;
  display: flex;
  gap: 12px;
}

.reply-form {
  margin-top: 12px;
  padding: 12px;
  background: #fff;
  border: 1px dashed #ccc;
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
  border-left: 2px solid #ddd;
}

.reply-item {
  padding: 12px;
  background: #fff;
  border: 1px solid #e0e0e0;
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
  color: #34495e;
}

.reply-date {
  font-size: 0.8rem;
  color: #999;
}

.reply-content {
  line-height: 1.5;
  font-size: 0.95rem;
}

.reply-actions {
  margin-top: 8px;
  display: flex;
  gap: 12px;
}

.sub-replies {
  margin-top: 12px;
  padding-left: 16px;
  border-left: 2px solid #eee;
}

.sub-reply-item {
  padding: 8px;
  background: #f8f8f8;
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
  color: #666;
}

.sub-reply-date {
  font-size: 0.75rem;
  color: #999;
}

.sub-reply-content {
  line-height: 1.4;
  font-size: 0.9rem;
  color: #555;
}

.sub-reply-actions {
  margin-top: 6px;
}
</style>
