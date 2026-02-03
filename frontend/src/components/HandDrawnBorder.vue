<!--
  HandDrawnBorder.vue - 手绘风格边框组件

  本组件为子元素添加手绘风格的不规则边框。
  使用 Rough.js 生成粗糙的手绘效果矩形边框，
  支持自定义粗糙度、弯曲度、描边颜色和宽度。
  边框会随容器尺寸变化自动重绘。
-->

<template>
  <!-- 容器：包含插槽内容和手绘边框 -->
  <div ref="containerRef" class="hand-drawn-border">
    <!-- 插槽：放置需要添加边框的内容 -->
    <slot />
  </div>
</template>

<script setup lang="ts">
// 从 vue 导入 Composition API 工具
import { ref, onMounted, onUnmounted, watch } from 'vue'

// 导入 Rough.js 库
import rough from 'roughjs'

// ========== Props 定义 ==========

/**
 * 组件属性
 * @param roughness - 粗糙度，值越大越粗糙（默认 2）
 * @param bowing - 弯曲度，控制线条的弯曲程度（默认 1）
 * @param stroke - 描边颜色（默认 #2c3e50 深蓝灰色）
 * @param strokeWidth - 描边宽度（默认 2）
 */
const props = defineProps<{
  roughness?: number
  bowing?: number
  stroke?: string
  strokeWidth?: number
}>()

// ========== 响应式状态 ==========

// 容器 DOM 引用
const containerRef = ref<HTMLElement | null>(null)

// ResizeObserver 实例（用于监听尺寸变化）
let resizeObserver: ResizeObserver | null = null

// ========== 方法 ==========

/**
 * 绘制手绘边框
 * 清除旧的 SVG，创建新的手绘矩形边框
 */
const drawBorder = () => {
  if (!containerRef.value) return

  const element = containerRef.value

  // 清除已存在的手绘边框 SVG
  const existingSvgs = element.querySelectorAll('svg.hand-drawn-border-svg')
  existingSvgs.forEach(svg => svg.remove())

  // 确保插槽内容已渲染（查找 card-content 元素）
  const slotContent = element.querySelector('.card-content')
  if (!slotContent) return

  // 获取容器尺寸
  const rect = element.getBoundingClientRect()

  // 跳过空尺寸情况
  if (rect.width === 0 || rect.height === 0) return

  // 创建 SVG 元素
  const svgNS = 'http://www.w3.org/2000/svg'
  const svg = document.createElementNS(svgNS, 'svg')
  svg.setAttribute('width', `${rect.width}`)
  svg.setAttribute('height', `${rect.height}`)
  svg.classList.add('hand-drawn-border-svg')

  // 设置 SVG 样式
  svg.style.position = 'absolute'
  svg.style.top = '0'
  svg.style.left = '0'
  svg.style.pointerEvents = 'none'  // 不阻挡鼠标事件
  svg.style.zIndex = '10'            // 位于内容上方

  // 创建 Rough.js 生成器
  const generator = rough.svg(svg)

  // 边框配置选项 - 使用更小的 roughness 和 bowing 减少偏移
  const options: rough.Options = {
    roughness: 1,         // 降低粗糙度
    bowing: 0.5,          // 降低弯曲度
    stroke: props.stroke ?? '#2c3e50', // 描边颜色
    strokeWidth: props.strokeWidth ?? 2, // 描边宽度
    fill: undefined,                   // 无填充
  }

  // 绘制矩形（留出 4px 内边距）
  const node = generator.rectangle(
    4,                    // x 坐标
    4,                    // y 坐标
    rect.width - 8,       // 宽度（减去内边距）
    rect.height - 8,      // 高度（减去内边距）
    options
  )

  // 将矩形节点添加到 SVG
  svg.appendChild(node)

  // 将 SVG 插入到元素最后（位于底层）
  element.appendChild(svg)
}

// ========== 生命周期 ==========

/**
 * 组件挂载时初始化
 * - 延迟绘制确保 DOM 已完全渲染
 * - 创建 ResizeObserver 监听尺寸变化
 */
onMounted(() => {
  // 延迟绘制（确保 DOM 已渲染）
  setTimeout(() => drawBorder(), 0)

  // 创建尺寸观察器
  resizeObserver = new ResizeObserver(() => {
    drawBorder()
  })

  // 开始观察容器尺寸变化
  if (containerRef.value) {
    resizeObserver.observe(containerRef.value)
  }
})

/**
 * 组件卸载时清理
 * 断开 ResizeObserver 连接，避免内存泄漏
 */
onUnmounted(() => {
  resizeObserver?.disconnect()
})

// ========== 响应式监听 ==========

/**
 * 监听属性变化
 * 当粗糙度、弯曲度、描边颜色或宽度变化时重绘边框
 */
watch(
  () => [props.roughness, props.bowing, props.stroke, props.strokeWidth],
  drawBorder
)
</script>

<style scoped>
.hand-drawn-border {
  position: relative;
  background: var(--card-bg);
  overflow: hidden;
}
</style>
