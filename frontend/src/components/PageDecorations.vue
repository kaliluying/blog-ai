<!--
  PageDecorations.vue - 页面两侧手绘风格装饰组件

  本组件在页面两侧添加手绘风格的装饰元素：
  - 左侧：植物藤蔓风格装饰
  - 右侧：星星和几何线条装饰
-->

<template>
  <div class="page-decorations">
    <!-- 左侧装饰 -->
    <div class="decoration-left">
      <svg class="decoration-svg" viewBox="0 0 100 800" preserveAspectRatio="xMidYMax slice">
        <!-- 藤蔓线条 -->
        <path
          class="hand-drawn-line"
          d="M 10,800 Q 25,600 15,500 Q 5,400 20,300 Q 35,200 15,100 Q 5,50 10,0"
          fill="none"
        />
        <!-- 叶子装饰 -->
        <ellipse class="hand-drawn-shape" cx="15" cy="480" rx="8" ry="12" transform="rotate(-30 15 480)" />
        <ellipse class="hand-drawn-shape" cx="20" cy="350" rx="6" ry="10" transform="rotate(20 20 350)" />
        <ellipse class="hand-drawn-shape" cx="12" cy="220" rx="7" ry="11" transform="rotate(-15 12 220)" />
        <ellipse class="hand-drawn-shape" cx="18" cy="120" rx="5" ry="8" transform="rotate(25 18 120)" />
        <!-- 小圆形点缀 -->
        <circle class="hand-drawn-dot" cx="30" cy="550" r="3" />
        <circle class="hand-drawn-dot" cx="25" cy="420" r="2" />
        <circle class="hand-drawn-dot" cx="32" cy="280" r="3" />
        <circle class="hand-drawn-dot" cx="28" cy="180" r="2" />
      </svg>
    </div>

    <!-- 右侧装饰 -->
    <div class="decoration-right">
      <svg class="decoration-svg" viewBox="0 0 100 800" preserveAspectRatio="xMidYMax slice">
        <!-- 垂直线条 -->
        <path
          class="hand-drawn-line"
          d="M 80,800 L 82,700 L 78,600 L 84,500 L 76,400 L 80,300 L 75,200 L 82,100 L 78,0"
          fill="none"
        />
        <!-- 星星 -->
        <path
          class="hand-drawn-star"
          d="M 20,150 L 23,160 L 33,160 L 25,167 L 28,177 L 20,170 L 12,177 L 15,167 L 7,160 L 17,160 Z"
        />
        <path
          class="hand-drawn-star"
          d="M 70,300 L 72,307 L 79,307 L 73,312 L 75,319 L 70,314 L 65,319 L 67,312 L 61,307 L 68,307 Z"
        />
        <path
          class="hand-drawn-star"
          d="M 25,450 L 27,457 L 34,457 L 28,462 L 30,469 L 25,464 L 20,469 L 22,462 L 16,457 L 23,457 Z"
        />
        <path
          class="hand-drawn-star"
          d="M 75,550 L 77,557 L 84,557 L 78,562 L 80,569 L 75,564 L 70,569 L 72,562 L 66,557 L 73,557 Z"
        />
        <path
          class="hand-drawn-star"
          d="M 30,680 L 32,687 L 39,687 L 33,692 L 35,699 L 30,694 L 25,699 L 27,692 L 21,687 L 28,687 Z"
        />
        <!-- 小圆形点缀 -->
        <circle class="hand-drawn-dot" cx="50" cy="250" r="2" />
        <circle class="hand-drawn-dot" cx="60" cy="400" r="3" />
        <circle class="hand-drawn-dot" cx="45" cy="600" r="2" />
      </svg>
    </div>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: 'PageDecorations'
})
</script>

<style scoped>
.page-decorations {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.decoration-left,
.decoration-right {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 120px;
}

.decoration-left {
  left: 0;
}

.decoration-right {
  right: 0;
}

.decoration-svg {
  width: 100%;
  height: 100%;
}

.hand-drawn-line {
  stroke: var(--border-color, #2c3e50);
  stroke-width: 1.5;
  fill: none;
  opacity: 0.4;
}

.hand-drawn-shape {
  stroke: var(--border-color, #2c3e50);
  stroke-width: 1.5;
  fill: var(--card-bg, #fafafa);
  opacity: 0.4;
}

.hand-drawn-star {
  stroke: var(--border-color, #2c3e50);
  stroke-width: 1.5;
  fill: var(--card-bg, #fafafa);
  opacity: 0.5;
}

.hand-drawn-dot {
  stroke: var(--border-color, #2c3e50);
  stroke-width: 1.5;
  fill: var(--card-bg, #fafafa);
  opacity: 0.4;
}

/* 中等屏幕 */
@media (max-width: 1200px) {
  .decoration-left,
  .decoration-right {
    width: 60px;
  }
}

/* 小屏幕隐藏装饰 */
@media (max-width: 768px) {
  .decoration-left,
  .decoration-right {
    display: none;
  }
}
</style>
