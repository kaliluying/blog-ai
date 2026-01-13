<!--
  HandDrawnConfirm.vue - 手绘风格确认对话框组件

  本组件提供一个带有手绘风格的确认弹窗，
  用于需要用户确认的 destructive 操作（如删除）。
  点击触发元素后显示确认对话框，
  确认后执行 onConfirm 回调。
-->

<template>
  <!-- 组件容器 -->
  <div class="hand-drawn-confirm">
    <!-- 触发区域：点击后显示对话框 -->
    <div class="confirm-trigger" @click="visible = true">
      <slot />
    </div>

    <!-- 确认对话框：使用 Naive UI 的 Modal 组件 -->
    <n-modal
      v-model:show="visible"
      preset="card"
      title="确认删除"
      style="width: 320px"
      :bordered="false"
    >
      <!-- 对话框内容 -->
      <div class="confirm-content">
        <!-- 手绘风格图标 -->
        <HandDrawnIcon type="star" :size="32" />
        <!-- 确认消息 -->
        <p>{{ message }}</p>
      </div>

      <!-- 对话框底部：操作按钮 -->
      <template #footer>
        <div class="confirm-footer">
          <!-- 取消按钮 -->
          <n-button @click="visible = false">取消</n-button>
          <!-- 确认/删除按钮 -->
          <n-button type="error" :loading="loading" @click="handleConfirm">
            删除
          </n-button>
        </div>
      </template>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
// 从 vue 导入 Composition API 工具
import { ref } from 'vue'

// 导入手绘风格图标组件
import HandDrawnIcon from './HandDrawnIcon.vue'

// ========== Props 定义 ==========

/**
 * 组件属性
 * @param message - 确认对话框中显示的消息文本
 * @param onConfirm - 用户确认后执行的回调函数
 */
const props = defineProps<{
  message?: string
  onConfirm?: () => Promise<void> | void
}>()

// ========== 响应式状态 ==========

// 对话框可见性（控制显示/隐藏）
const visible = ref(false)

// 加载状态（防止重复提交）
const loading = ref(false)

// ========== 方法 ==========

/**
 * 处理确认操作
 * 执行 onConfirm 回调，完成后关闭对话框
 */
const handleConfirm = async () => {
  loading.value = true  // 开始加载

  try {
    // 执行确认回调
    await props.onConfirm?.()
    // 关闭对话框
    visible.value = false
  } finally {
    loading.value = false  // 结束加载
  }
}
</script>

<style scoped>
.hand-drawn-confirm {
  display: inline-block;
}

.confirm-trigger {
  cursor: pointer;
}

.confirm-content {
  text-align: center;
  padding: 20px;
}

.confirm-content p {
  margin-top: 12px;
  color: #34495e;
  font-size: 1rem;
}

.confirm-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
