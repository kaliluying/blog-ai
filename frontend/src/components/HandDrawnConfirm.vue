<template>
  <div class="hand-drawn-confirm">
    <div class="confirm-trigger" @click="visible = true">
      <slot />
    </div>

    <n-modal
      v-model:show="visible"
      preset="card"
      title="确认删除"
      style="width: 320px"
      :bordered="false"
    >
      <div class="confirm-content">
        <HandDrawnIcon type="star" :size="32" />
        <p>{{ message }}</p>
      </div>
      <template #footer>
        <div class="confirm-footer">
          <n-button @click="visible = false">取消</n-button>
          <n-button type="error" :loading="loading" @click="handleConfirm">
            删除
          </n-button>
        </div>
      </template>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import HandDrawnIcon from './HandDrawnIcon.vue'

const props = defineProps<{
  message?: string
  onConfirm?: () => Promise<void> | void
}>()

const visible = ref(false)
const loading = ref(false)

const handleConfirm = async () => {
  loading.value = true
  try {
    await props.onConfirm?.()
    visible.value = false
  } finally {
    loading.value = false
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
