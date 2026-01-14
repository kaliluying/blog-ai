<template>
  <div class="comment-section">
    <h3 class="comment-title">
      <HandDrawnIcon type="comment" :size="24" />
      评论 ({{ comments.length }})
    </h3>

    <!-- 评论表单（匿名评论） -->
    <div class="comment-form">
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
          <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
        </div>

        <div class="comment-content">{{ comment.content }}</div>

        <div class="comment-actions">
          <n-button text size="small" @click="showReplyForm(comment.id)">
            回复
          </n-button>
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
              <span class="reply-date">{{ formatDate(reply.created_at) }}</span>
            </div>
            <div class="reply-content">{{ reply.content }}</div>
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
                  <span class="sub-reply-date">{{ formatDate(subReply.created_at) }}</span>
                </div>
                <div class="sub-reply-content">{{ subReply.content }}</div>
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
import { ref, onMounted, computed } from 'vue'
import { useMessage } from 'naive-ui'
import { useAdminStore } from '@/stores/auth'
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

const message = useMessage()
const adminStore = useAdminStore()

const newComment = ref('')
const nickname = ref('')
const replyContent = ref('')
const replyingTo = ref<number | null>(null)
const replyingToParent = ref<number | null>(null)
const submitting = ref(false)

const randomNicknames = [
  '好奇的猫咪', '爱思考的云朵', '路过的旅人', '安静的观察者',
  '快乐的星星', '温柔的微风', '勇敢的小鸟', '智慧的树洞',
  '神秘的访客', '温暖的阳光', '自由的飞鸟', '善良的小熊',
  '可爱的兔子', '机智的狐狸', '优雅的天鹅', '活泼的松鼠',
  '沉稳的大象', '灵动的蝴蝶', '坚定的山峰', '清澈的溪流'
]

const generateNickname = () => {
  const randomIndex = Math.floor(Math.random() * randomNicknames.length)
  const randomNum = Math.floor(Math.random() * 1000)
  return `${randomNicknames[randomIndex]}${randomNum}`
}

const regenerateNickname = () => {
  nickname.value = generateNickname()
  saveNickname(nickname.value)
  message.info('已生成新昵称')
}

const saveNickname = (nick: string) => {
  localStorage.setItem('commentNickname', nick)
}

const canSubmit = computed(() => {
  return newComment.value.trim() && nickname.value.trim()
})

const canReplySubmit = computed(() => {
  return replyContent.value.trim()
})

const showReplyForm = (commentId: number, parentId?: number) => {
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
  if (!canSubmit.value) return

  submitting.value = true
  try {
    await commentApi.createComment({
      post_id: props.postId,
      nickname: nickname.value.trim(),
      content: newComment.value.trim()
    })
    saveNickname(nickname.value)
    newComment.value = ''
    message.success('评论发布成功~')
    emit('refresh')
  } catch {
    message.error('评论失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}

const handleReply = async (parentId: number) => {
  if (!canReplySubmit.value) return

  submitting.value = true
  try {
    await commentApi.createComment({
      post_id: props.postId,
      nickname: nickname.value.trim(),
      content: replyContent.value.trim(),
      parent_id: parentId
    })
    replyContent.value = ''
    replyingTo.value = null
    replyingToParent.value = null
    message.success('回复发布成功~')
    emit('refresh')
  } catch {
    message.error('回复失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}

const handleDelete = async (commentId: number) => {
  try {
    await commentApi.deleteComment(commentId)
    message.success('评论已删除')
    emit('refresh')
  } catch {
    message.error('删除失败，请稍后重试')
  }
}

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
