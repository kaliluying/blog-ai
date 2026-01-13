<!--
  HandDrawnCard.vue - 手绘风格卡片组件

  本组件是一个带有手绘风格边框的卡片容器，
  用于展示分组内容。支持可选的标题，
  标题下方有手绘风格的分隔线。
  鼠标悬停时会有轻微的旋转和放大效果。
-->

<template>
  <!-- 使用 HandDrawnBorder 组件创建手绘边框 -->
  <HandDrawnBorder
    :roughness="2"
    stroke="#34495e"
    class="hand-drawn-card"
  >
    <!-- 卡片内容区域 -->
    <div class="card-content">

      <!-- 可选标题区域 -->
      <div v-if="title" class="card-header">
        <h3>{{ title }}</h3>
        <!-- 手绘分隔线 -->
        <HandDrawnDivider />
      </div>

      <!-- 插槽：放置卡片内容 -->
      <slot />

    </div>
  </HandDrawnBorder>
</template>

<script setup lang="ts">
// 导入子组件
import HandDrawnBorder from './HandDrawnBorder.vue'
import HandDrawnDivider from './HandDrawnDivider.vue'

// ========== Props 定义 ==========

/**
 * 组件属性
 * @param title - 可选的卡片标题
 */
defineProps<{
  title?: string
}>()
</script>

<style scoped>
.hand-drawn-card {
  margin: 16px;
  transition: transform 0.2s ease;
}

.hand-drawn-card:hover {
  transform: rotate(-0.5deg) scale(1.01);
}

.card-content {
  padding: 16px;
  background: #fff;
}

.card-header {
  margin-bottom: 12px;
}

.card-header h3 {
  margin: 0 0 8px 0;
  font-family: 'Caveat', cursive;
  font-size: 1.5rem;
  color: #2c3e50;
}
</style>
