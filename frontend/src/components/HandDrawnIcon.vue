<!--
  HandDrawnIcon.vue - 手绘风格图标组件

  本组件使用 Rough.js 库绘制手绘风格的基础图标，
  支持四种图标类型：star（星星）、heart（心形）、bookmark（书签）、comment（评论）。

  特点：
  - 使用 SVG 矢量图形
  - 手绘风格的不规则线条
  - 可自定义图标大小
  - 支持响应图标类型变化
-->

<template>
  <!-- 图标容器 -->
  <div ref="iconRef" class="hand-drawn-icon"></div>
</template>

<script setup lang="ts">
// 从 vue 导入 Composition API 工具
import { ref, onMounted, watch } from 'vue'

// 导入 Rough.js 库
import rough from 'roughjs'

// ========== Props 定义 ==========

/**
 * 组件属性
 * @param type - 图标类型：'star' | 'heart' | 'bookmark' | 'comment'
 * @param size - 图标尺寸（像素），默认 24px
 */
const props = defineProps<{
  type: 'star' | 'heart' | 'bookmark' | 'comment'
  size?: number
}>()

// ========== 响应式状态 ==========

// DOM 元素引用
const iconRef = ref<HTMLElement | null>(null)

// ========== 图标绘制函数 ==========

/**
 * 图标类型映射表
 * 每种图标类型对应一个绘制函数，返回 Rough.js 节点数组
 */
const icons: Record<string, (x: number, y: number, size: number) => rough.Node[]> = {
  /**
   * 星星图标
   * 使用五角星几何计算，绘制 10 个顶点（5 外 + 5 内）
   */
  star: (x, y, size) => {
    const generator = rough.svg(document.createElementNS('http://www.w3.org/2000/svg', 'svg'))
    const points: [number, number][] = []
    const outerRadius = size / 2      // 外半径
    const innerRadius = size / 4      // 内半径

    // 计算五角星的所有顶点
    for (let i = 0; i < 5; i++) {
      // 外顶点角度
      const angle = (i * 4 * Math.PI) / 5 - Math.PI / 2
      points.push([x + outerRadius * Math.cos(angle), y + outerRadius * Math.sin(angle)])
      // 内顶点角度
      points.push([x + innerRadius * Math.cos(angle + Math.PI / 5), y + innerRadius * Math.sin(angle + Math.PI / 5)])
    }

    // 绘制多边形
    return [generator.polygon(points, {
      stroke: '#34495e',   // 深蓝灰色描边
      strokeWidth: 2,      // 描边宽度
      fill: 'none',        // 无填充
      roughness: 1.5       // 适中粗糙度
    })]
  },

  /**
   * 心形图标
   * 使用贝塞尔曲线绘制心形路径
   */
  heart: (x, y, size) => {
    const generator = rough.svg(document.createElementNS('http://www.w3.org/2000/svg', 'svg'))
    // 心形路径：两个贝塞尔曲线段
    const path = `M ${x} ${y + size * 0.3}
      C ${x - size * 0.5} ${y - size * 0.2}, ${x - size * 0.5} ${y + size * 0.4}, ${x} ${y + size * 0.8}
      C ${x + size * 0.5} ${y + size * 0.4}, ${x + size * 0.5} ${y - size * 0.2}, ${x} ${y + size * 0.3}`

    return [generator.path(path, {
      stroke: '#e74c3c',   // 红色描边
      strokeWidth: 2,
      fill: 'none',
      roughness: 1         // 较低粗糙度（心形较圆润）
    })]
  },

  /**
   * 书签图标
   * 菱形/书签形状，带填充
   */
  bookmark: (x, y, size) => {
    const generator = rough.svg(document.createElementNS('http://www.w3.org/2000/svg', 'svg'))
    // 书签形状路径
    return [generator.path(
      `M ${x - size * 0.3} ${y - size * 0.4}
       L ${x - size * 0.3} ${y + size * 0.4}
       L ${x} ${y + size * 0.2}
       L ${x + size * 0.3} ${y + size * 0.4}
       L ${x + size * 0.3} ${y - size * 0.4}
       Z`,
      {
        stroke: '#34495e',
        strokeWidth: 2,
        fill: '#f39c12',         // 橙色填充
        fillStyle: 'hachure',    // 填充样式：影线
        roughness: 1.5
      }
    )]
  },

  /**
   * 评论/对话框图标
   * 矩形气泡形状
   */
  comment: (x, y, size) => {
    const generator = rough.svg(document.createElementNS('http://www.w3.org/2000/svg', 'svg'))
    // 矩形（气泡形状）
    return [generator.rectangle(x - size * 0.4, y - size * 0.3, size * 0.8, size * 0.6, {
      stroke: '#34495e',
      strokeWidth: 2,
      fill: 'none',
      roughness: 1.2
    })]
  }
}

// ========== 方法 ==========

/**
 * 绘制图标
 * 根据类型生成对应的手绘风格 SVG
 */
const drawIcon = () => {
  if (!iconRef.value) return

  const element = iconRef.value
  // 获取图标尺寸（默认 24px）
  const size = props.size || 24

  // 清空容器
  element.innerHTML = ''

  // 创建 SVG 命名空间和元素
  const svgNS = 'http://www.w3.org/2000/svg'
  const svg = document.createElementNS(svgNS, 'svg')
  svg.setAttribute('width', `${size}`)
  svg.setAttribute('height', `${size}`)
  svg.style.display = 'block'

  // 获取对应类型的绘制函数并执行
  const nodes = icons[props.type]?.(size / 2, size / 2, size) || []
  nodes.forEach(node => svg.appendChild(node))

  // 将 SVG 添加到容器
  element.appendChild(svg)
}

// ========== 生命周期和监听 ==========

// 组件挂载时绘制图标
onMounted(drawIcon)

// 监听图标类型变化，重新绘制
watch(() => props.type, drawIcon)
</script>

<style scoped>
.hand-drawn-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
</style>
