<!--
  HandDrawnBackground.vue - 手绘风格背景组件

  本组件使用 Rough.js 库在页面上绘制手绘风格的装饰元素，
  包括圆形、线条和波浪线，营造出手绘/素描的视觉效果。
-->

<template>
  <!-- 背景容器，通过 ref 获取 DOM 引用 -->
  <div class="hand-drawn-background" ref="bgRef"></div>
</template>

<script setup lang="ts">
// 从 vue 导入 Composition API 工具
import { ref, onMounted } from 'vue'

// 导入 Rough.js 库，用于生成手绘风格图形
import rough from 'roughjs'

// ========== 响应式状态 ==========

// DOM 元素引用（用于访问容器尺寸和添加 SVG）
const bgRef = ref<HTMLElement | null>(null)

// ========== 生命周期 ==========

/**
 * 组件挂载时绘制手绘装饰
 * onMounted 在 DOM 渲染完成后执行
 */
onMounted(() => {
  // 确保容器已渲染
  if (!bgRef.value) return

  // 获取容器元素
  const container = bgRef.value

  // 获取容器尺寸
  const width = container.offsetWidth
  const height = container.offsetHeight

  // 创建 SVG 命名空间
  const svgNS = 'http://www.w3.org/2000/svg'

  // 创建 SVG 元素
  const svg = document.createElementNS(svgNS, 'svg')
  svg.setAttribute('width', '100%')
  svg.setAttribute('height', '100%')

  // 设置 SVG 样式：绝对定位，不阻挡鼠标事件
  svg.style.position = 'absolute'
  svg.style.top = '0'
  svg.style.left = '0'
  svg.style.pointerEvents = 'none'

  // 创建 Rough.js 生成器
  const generator = rough.svg(svg)

  // 装饰元素配置：类型和数量
  const decorations = [
    { type: 'circle', count: 5 },    // 圆形：5 个
    { type: 'line', count: 8 },      // 线条：8 条
    { type: 'squiggle', count: 6 }   // 波浪线：6 条
  ]

  // 遍历每种装饰类型并绘制
  decorations.forEach(({ type, count }) => {
    for (let i = 0; i < count; i++) {
      // 随机位置
      const x = Math.random() * width
      const y = Math.random() * height

      // 随机大小
      const size = 10 + Math.random() * 30

      // 根据类型绘制不同图形
      switch (type) {
        case 'circle':
          // 圆形：空心描边
          svg.appendChild(generator.circle(x, y, size, {
            stroke: '#bdc3c7',     // 浅灰色描边
            strokeWidth: 1,        // 描边宽度
            fill: 'none',          // 无填充
            roughness: 2           // 粗糙度（手绘效果）
          }))
          break

        case 'line':
          // 线条：斜线
          svg.appendChild(generator.line(x, y, x + size, y + size * 0.3, {
            stroke: '#bdc3c7',
            strokeWidth: 1,
            roughness: 1.5
          }))
          break

        case 'squiggle':
          // 波浪线：使用贝塞尔曲线绘制
          const path = `M ${x} ${y} Q ${x + size * 0.3} ${y - size * 0.2} ${x + size * 0.5} ${y} T ${x + size} ${y}`
          svg.appendChild(generator.path(path, {
            stroke: '#bdc3c7',
            strokeWidth: 1,
            roughness: 1.5
          }))
          break
      }
    }
  })

  // 将 SVG 添加到容器
  container.appendChild(svg)
})
</script>

<style scoped>
.hand-drawn-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: 0;
}
</style>
