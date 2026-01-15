<!--
  TableOfContents.vue - 文章目录组件

  功能：
  - 右侧固定显示
  - 滚动联动高亮
  - 点击平滑跳转
  - 支持 h1-h3 标题
-->
<template>
  <nav v-if="headings.length > 0" class="toc-container">
    <HandDrawnCard class="toc-card">
      <h4 class="toc-title">目录</h4>
      <ul class="toc-list">
        <li
          v-for="heading in headings"
          :key="heading.id"
          :class="['toc-item', `toc-level-${heading.level}`, { active: activeId === heading.id }]"
          @click="scrollTo(heading.id)"
        >
          {{ heading.text }}
        </li>
      </ul>
    </HandDrawnCard>
  </nav>
</template>

<script setup lang="ts">
import HandDrawnCard from '@/components/HandDrawnCard.vue'

/**
 * 标题类型
 */
interface Heading {
  id: string
  text: string
  level: number
}

defineProps<{
  headings: Heading[]
  activeId: string
}>()

const emit = defineEmits<{
  (e: 'select', id: string): void
}>()

const scrollTo = (id: string) => {
  emit('select', id)
}
</script>

<style scoped>
.toc-container {
  width: 100%;
}

.toc-card {
  width: 100%;
  padding: 16px;
}

.toc-title {
  margin: 0 0 12px;
  font-family: 'Caveat', cursive;
  font-size: 1.5rem;
  color: var(--text-primary);
  font-weight: normal;
}

.toc-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.toc-item {
  padding: 6px 12px;
  margin: 4px 0;
  color: var(--text-secondary);
  font-size: 0.95rem;
  cursor: pointer;
  border-left: 3px solid transparent;
  border-radius: 0 6px 6px 0;
  transition: all 0.2s ease;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.toc-item:hover {
  color: #3498db;
  background: rgba(52, 152, 219, 0.08);
  border-left-color: rgba(52, 152, 219, 0.3);
}

.toc-item.active {
  color: #3498db;
  border-left-color: #3498db;
  background: rgba(52, 152, 219, 0.12);
  font-weight: 500;
}

/* 层级缩进 */
.toc-level-1 {
  padding-left: 12px;
}

.toc-level-2 {
  padding-left: 24px;
  font-size: 0.9rem;
}

.toc-level-3 {
  padding-left: 36px;
  font-size: 0.85rem;
}

/* 滚动条美化 */
.toc-list::-webkit-scrollbar {
  width: 4px;
}

.toc-list::-webkit-scrollbar-track {
  background: transparent;
}

.toc-list::-webkit-scrollbar-thumb {
  background: #ddd;
  border-radius: 4px;
}

.toc-list::-webkit-scrollbar-thumb:hover {
  background: #bbb;
}
</style>
