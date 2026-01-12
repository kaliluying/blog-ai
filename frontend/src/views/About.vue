<template>
  <div class="about-page">
    <HandDrawnBackground />

    <div class="about-container">
      <HandDrawnCard title="关于我" class="about-card">
        <div class="about-content">
          <div class="about-avatar">
            <HandDrawnIcon type="heart" :size="80" />
          </div>

          <p class="about-intro">
            你好！我是一个热爱技术和设计的开发者。
            这个博客是我记录学习心得、分享技术经验的地方。
          </p>

          <p>
            我喜欢探索新的前端技术，热爱 Vue 生态系统，
            同时也对用户体验设计充满热情。
          </p>

          <h4>技能标签</h4>
          <div class="skills-list">
            <n-tag v-for="skill in skills" :key="skill" round size="medium">
              {{ skill }}
            </n-tag>
          </div>

          <h4>联系我</h4>
          <div class="contact-links">
            <n-button quaternary>
              <HandDrawnIcon type="comment" :size="20" />
              GitHub
            </n-button>
            <n-button quaternary>
              <HandDrawnIcon type="bookmark" :size="20" />
              邮箱
            </n-button>
          </div>
        </div>
      </HandDrawnCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import HandDrawnCard from '@/components/HandDrawnCard.vue'
import HandDrawnIcon from '@/components/HandDrawnIcon.vue'
import HandDrawnBackground from '@/components/HandDrawnBackground.vue'

const skills = ['Vue 3', 'TypeScript', 'Node.js', 'UI Design', 'FastAPI', 'PostgreSQL']
</script>

<style scoped>
.about-page {
  position: relative;
  min-height: 100vh;
  padding: 40px 20px;
}

.about-container {
  position: relative;
  z-index: 1;
  max-width: 600px;
  margin: 0 auto;
}

.about-card {
  width: 100%;
}

.about-content {
  text-align: center;
}

.about-avatar {
  margin-bottom: 24px;
  opacity: 0.8;
}

.about-intro {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #34495e;
  margin-bottom: 16px;
}

.about-content p {
  color: #5d6d7e;
  line-height: 1.6;
  margin-bottom: 16px;
}

.about-content h4 {
  font-family: 'Caveat', cursive;
  font-size: 1.5rem;
  color: #2c3e50;
  margin: 24px 0 16px 0;
}

.skills-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px;
}

.contact-links {
  display: flex;
  justify-content: center;
  gap: 16px;
}
</style>
