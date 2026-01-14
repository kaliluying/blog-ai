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
  </nav>
</template>

<script setup lang="ts">
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
  position: sticky;
  top: 100px;
  max-height: calc(100vh - 140px);
  overflow-y: auto;
  padding: 16px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.toc-title {
  margin: 0 0 12px;
  font-family: 'Caveat', cursive;
  font-size: 1.25rem;
  color: #2c3e50;
  font-weight: normal;
}

.toc-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.toc-item {
  padding: 4px 8px;
  margin: 2px 0;
  color: #666;
  font-size: 0.9rem;
  cursor: pointer;
  border-left: 2px solid transparent;
  transition: all 0.2s;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.toc-item:hover {
  color: #3498db;
  background: #f8f9fa;
}

.toc-item.active {
  color: #3498db;
  border-left-color: #3498db;
  background: #f0f7ff;
  font-weight: 500;
}

/* 层级缩进 */
.toc-level-1 {
  padding-left: 8px;
}

.toc-level-2 {
  padding-left: 20px;
  font-size: 0.85rem;
}

.toc-level-3 {
  padding-left: 32px;
  font-size: 0.8rem;
}

/* 滚动条美化 */
.toc-container::-webkit-scrollbar {
  width: 4px;
}

.toc-container::-webkit-scrollbar-track {
  background: transparent;
}

.toc-container::-webkit-scrollbar-thumb {
  background: #ddd;
  border-radius: 4px;
}

.toc-container::-webkit-scrollbar-thumb:hover {
  background: #bbb;
}
</style>
