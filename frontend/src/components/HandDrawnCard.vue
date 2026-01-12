<template>
  <HandDrawnBorder
    :roughness="2"
    stroke="#34495e"
    class="hand-drawn-card"
  >
    <div class="card-content">
      <div v-if="title" class="card-header">
        <h3>{{ title }}</h3>
        <HandDrawnDivider />
      </div>
      <slot />
    </div>
  </HandDrawnBorder>
</template>

<script setup lang="ts">
import HandDrawnBorder from './HandDrawnBorder.vue'
import HandDrawnDivider from './HandDrawnDivider.vue'

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
