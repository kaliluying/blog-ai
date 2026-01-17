<!--
  ReplyForm.vue - 回复表单组件

  本组件提供统一的回复表单 UI，
  用于评论回复和二级回复。
-->

<template>
  <div class="reply-form">
    <n-input
      :value="modelValue"
      type="textarea"
      placeholder="写下你的回复..."
      :rows="2"
      @update:value="emit('update:modelValue', $event)"
    />
    <div class="form-actions">
      <n-button size="small" @click="$emit('cancel')">取消</n-button>
      <n-button
        type="primary"
        size="small"
        :loading="loading"
        :disabled="!canSubmit"
        @click="handleSubmit"
      >
        回复
      </n-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

defineOptions({
  name: 'ReplyForm'
})

const props = defineProps<{
  modelValue: string
  loading: boolean
  canSubmit: boolean
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'submit'): void
  (e: 'cancel'): void
}>()

const canSubmit = computed(() => props.canSubmit && props.modelValue.trim())

const handleSubmit = () => {
  if (canSubmit.value) {
    emit('submit')
  }
}
</script>

<style scoped>
.reply-form {
  margin-top: 12px;
  padding: 12px;
  background: var(--card-bg);
  border: 1px dashed var(--border-color);
  border-radius: 4px;
}

.form-actions {
  margin-top: 8px;
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}
</style>
