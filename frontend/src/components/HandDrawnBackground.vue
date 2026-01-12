<template>
  <div class="hand-drawn-background" ref="bgRef"></div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import rough from 'roughjs'

const bgRef = ref<HTMLElement | null>(null)

onMounted(() => {
  if (!bgRef.value) return

  const container = bgRef.value
  const width = container.offsetWidth
  const height = container.offsetHeight

  const svgNS = 'http://www.w3.org/2000/svg'
  const svg = document.createElementNS(svgNS, 'svg')
  svg.setAttribute('width', '100%')
  svg.setAttribute('height', '100%')
  svg.style.position = 'absolute'
  svg.style.top = '0'
  svg.style.left = '0'
  svg.style.pointerEvents = 'none'

  const generator = rough.svg(svg)

  const decorations = [
    { type: 'circle', count: 5 },
    { type: 'line', count: 8 },
    { type: 'squiggle', count: 6 }
  ]

  decorations.forEach(({ type, count }) => {
    for (let i = 0; i < count; i++) {
      const x = Math.random() * width
      const y = Math.random() * height
      const size = 10 + Math.random() * 30

      switch (type) {
        case 'circle':
          svg.appendChild(generator.circle(x, y, size, {
            stroke: '#bdc3c7',
            strokeWidth: 1,
            fill: 'none',
            roughness: 2
          }))
          break
        case 'line':
          svg.appendChild(generator.line(x, y, x + size, y + size * 0.3, {
            stroke: '#bdc3c7',
            strokeWidth: 1,
            roughness: 1.5
          }))
          break
        case 'squiggle':
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
