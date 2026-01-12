<template>
  <div ref="dividerRef" class="hand-drawn-divider"></div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import rough from 'roughjs'

const dividerRef = ref<HTMLElement | null>(null)

onMounted(() => {
  if (!dividerRef.value) return

  const element = dividerRef.value
  const width = element.offsetWidth || 200

  const svgNS = 'http://www.w3.org/2000/svg'
  const svg = document.createElementNS(svgNS, 'svg')
  svg.setAttribute('width', `${width}`)
  svg.setAttribute('height', '20')
  svg.style.display = 'block'

  const generator = rough.svg(svg)

  const line1 = generator.line(0, 10, width, 10, {
    stroke: '#34495e',
    strokeWidth: 2,
    roughness: 1.5,
    bowing: 0.5
  })

  const line2 = generator.line(10, 12, width - 20, 8, {
    stroke: '#7f8c8d',
    strokeWidth: 1,
    roughness: 2,
    bowing: 1
  })

  svg.appendChild(line1)
  svg.appendChild(line2)

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
