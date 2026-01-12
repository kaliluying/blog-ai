<template>
  <div ref="containerRef" class="hand-drawn-border">
    <slot />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import rough from 'roughjs'

const props = defineProps<{
  roughness?: number
  bowing?: number
  stroke?: string
  strokeWidth?: number
}>()

const containerRef = ref<HTMLElement | null>(null)
let resizeObserver: ResizeObserver | null = null

const drawBorder = () => {
  if (!containerRef.value) return

  const element = containerRef.value

  // 只删除手绘边框的 svg
  const existingSvgs = element.querySelectorAll('svg.hand-drawn-border-svg')
  existingSvgs.forEach(svg => svg.remove())

  // 确保 slot 内容已渲染
  const slotContent = element.querySelector('.card-content')
  if (!slotContent) return

  const rect = element.getBoundingClientRect()

  if (rect.width === 0 || rect.height === 0) return

  const svgNS = 'http://www.w3.org/2000/svg'
  const svg = document.createElementNS(svgNS, 'svg')
  svg.setAttribute('width', `${rect.width}`)
  svg.setAttribute('height', `${rect.height}`)
  svg.classList.add('hand-drawn-border-svg')
  svg.style.position = 'absolute'
  svg.style.top = '0'
  svg.style.left = '0'
  svg.style.pointerEvents = 'none'
  svg.style.zIndex = '10'

  const generator = rough.svg(svg)

  const options: rough.Options = {
    roughness: props.roughness ?? 2,
    bowing: props.bowing ?? 1,
    stroke: props.stroke ?? '#2c3e50',
    strokeWidth: props.strokeWidth ?? 2,
    fill: undefined,
  }

  const node = generator.rectangle(2, 2, rect.width - 4, rect.height - 4, options)
  svg.appendChild(node)

  element.insertBefore(svg, slotContent)
}

onMounted(() => {
  // 延迟绘制，确保 DOM 已渲染
  setTimeout(() => drawBorder(), 0)

  resizeObserver = new ResizeObserver(() => {
    drawBorder()
  })
  if (containerRef.value) {
    resizeObserver.observe(containerRef.value)
  }
})

onUnmounted(() => {
  resizeObserver?.disconnect()
})

watch(() => [props.roughness, props.bowing, props.stroke, props.strokeWidth], drawBorder)
</script>

<style scoped>
.hand-drawn-border {
  position: relative;
  background: #fff;
}
</style>
