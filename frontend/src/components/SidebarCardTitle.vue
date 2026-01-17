<!--
  SidebarCardTitle.vue - 侧边栏卡片标题组件

  本组件提供侧边栏卡片的统一标题样式，
  解决 .info-title 样式在多个组件中重复的问题。
-->

<template>
  <h3 class="sidebar-card-title">
    <HandDrawnIcon v-if="icon" :type="icon" :size="24" />
    <slot>{{ title }}</slot>
  </h3>
</template>

<script setup lang="ts">
import HandDrawnIcon from '@/components/HandDrawnIcon.vue'

defineOptions({
  name: 'SidebarCardTitle'
})

// 图标类型（与 HandDrawnIcon 组件匹配）
type IconType = 'star' | 'heart' | 'bookmark' | 'comment' | 'tag'

defineProps<{
  title?: string
  icon?: IconType
}>()
</script>

<style scoped>
.sidebar-card-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-family: 'Caveat', cursive;
  font-size: 1.5rem;
  color: var(--text-primary);
  margin: 0 0 16px 0;
}
</style>
