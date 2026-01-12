<template>
  <div ref="iconRef" class="hand-drawn-icon"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import rough from 'roughjs'

const props = defineProps<{
  type: 'star' | 'heart' | 'bookmark' | 'comment'
  size?: number
}>()

const iconRef = ref<HTMLElement | null>(null)

const icons: Record<string, (x: number, y: number, size: number) => rough.Node[]> = {
  star: (x, y, size) => {
    const generator = rough.svg(document.createElementNS('http://www.w3.org/2000/svg', 'svg'))
    const points: [number, number][] = []
    const outerRadius = size / 2
    const innerRadius = size / 4

    for (let i = 0; i < 5; i++) {
      const angle = (i * 4 * Math.PI) / 5 - Math.PI / 2
      points.push([x + outerRadius * Math.cos(angle), y + outerRadius * Math.sin(angle)])
      points.push([x + innerRadius * Math.cos(angle + Math.PI / 5), y + innerRadius * Math.sin(angle + Math.PI / 5)])
    }

    return [generator.polygon(points, { stroke: '#34495e', strokeWidth: 2, fill: 'none', roughness: 1.5 })]
  },

  heart: (x, y, size) => {
    const generator = rough.svg(document.createElementNS('http://www.w3.org/2000/svg', 'svg'))
    const path = `M ${x} ${y + size * 0.3}
      C ${x - size * 0.5} ${y - size * 0.2}, ${x - size * 0.5} ${y + size * 0.4}, ${x} ${y + size * 0.8}
      C ${x + size * 0.5} ${y + size * 0.4}, ${x + size * 0.5} ${y - size * 0.2}, ${x} ${y + size * 0.3}`

    return [generator.path(path, { stroke: '#e74c3c', strokeWidth: 2, fill: 'none', roughness: 1 })]
  },

  bookmark: (x, y, size) => {
    const generator = rough.svg(document.createElementNS('http://www.w3.org/2000/svg', 'svg'))
    return [generator.path(
      `M ${x - size * 0.3} ${y - size * 0.4}
       L ${x - size * 0.3} ${y + size * 0.4}
       L ${x} ${y + size * 0.2}
       L ${x + size * 0.3} ${y + size * 0.4}
       L ${x + size * 0.3} ${y - size * 0.4}
       Z`,
      { stroke: '#34495e', strokeWidth: 2, fill: '#f39c12', fillStyle: 'hachure', roughness: 1.5 }
    )]
  },

  comment: (x, y, size) => {
    const generator = rough.svg(document.createElementNS('http://www.w3.org/2000/svg', 'svg'))
    return [generator.rectangle(x - size * 0.4, y - size * 0.3, size * 0.8, size * 0.6, {
      stroke: '#34495e', strokeWidth: 2, fill: 'none', roughness: 1.2
    })]
  }
}

const drawIcon = () => {
  if (!iconRef.value) return

  const element = iconRef.value
  const size = props.size || 24

  element.innerHTML = ''

  const svgNS = 'http://www.w3.org/2000/svg'
  const svg = document.createElementNS(svgNS, 'svg')
  svg.setAttribute('width', `${size}`)
  svg.setAttribute('height', `${size}`)
  svg.style.display = 'block'

  const nodes = icons[props.type]?.(size / 2, size / 2, size) || []
  nodes.forEach(node => svg.appendChild(node))

  element.appendChild(svg)
}

onMounted(drawIcon)
watch(() => props.type, drawIcon)
</script>

<style scoped>
.hand-drawn-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
</style>
