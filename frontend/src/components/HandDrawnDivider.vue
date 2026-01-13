<!--
  HandDrawnDivider.vue - 手绘风格分隔线组件

  本组件使用 Rough.js 绘制两条交叉的手绘风格线条，
  作为视觉分隔元素，常用于卡片内的内容分组。
-->

<template>
  <!-- 分隔线容器 -->
  <div ref="dividerRef" class="hand-drawn-divider"></div>
</template>

<script setup lang="ts">
// 从 vue 导入 Composition API 工具
import { ref, onMounted } from 'vue'

// 导入 Rough.js 库
import rough from 'roughjs'

// ========== 响应式状态 ==========

// DOM 元素引用
const dividerRef = ref<HTMLElement | null>(null)

// ========== 生命周期 ==========

/**
 * 组件挂载时绘制分隔线
 */
onMounted(() => {
  // 确保元素已渲染
  if (!dividerRef.value) return

  const element = dividerRef.value

  // 获取容器宽度（默认 200px）
  const width = element.offsetWidth || 200

  // 创建 SVG 命名空间
  const svgNS = 'http://www.w3.org/2000/svg'

  // 创建 SVG 元素
  const svg = document.createElementNS(svgNS, 'svg')
  svg.setAttribute('width', `${width}`)
  svg.setAttribute('height', '20')
  svg.style.display = 'block'  // 块级显示

  // 创建 Rough.js 生成器
  const generator = rough.svg(svg)

  // 第一条线：主分隔线（深色）
  const line1 = generator.line(0, 10, width, 10, {
    stroke: '#34495e',     // 深蓝灰色
    strokeWidth: 2,        // 较粗
    roughness: 1.5,        // 适中粗糙度
    bowing: 0.5            // 轻微弯曲
  })

  // 第二条线：装饰线（浅色，与主线条交叉）
  const line2 = generator.line(10, 12, width - 20, 8, {
    stroke: '#7f8c8d',     // 浅灰色
    strokeWidth: 1,        // 较细
    roughness: 2,          // 较高粗糙度
    bowing: 1              // 较大弯曲
  })

  // 将线条添加到 SVG
  svg.appendChild(line1)
  svg.appendChild(line2)

  // 将 SVG 添加到容器
  element.appendChild(svg)
})
</script>

<style scoped>
.hand-drawn-divider {
  width: 100%;
  height: 20px;
  opacity: 0.7;
}
</style>
