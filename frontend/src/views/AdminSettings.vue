<!--
  AdminSettings.vue - 管理后台设置页面

  管理站点配置：
  1. 评论频率限制
  2. 其他站点设置
-->

<template>
  <div class="admin-settings">
    <div class="settings-header">
      <h1 class="settings-title">站点设置</h1>
      <p class="settings-subtitle">管理博客的各项配置</p>
    </div>

    <!-- 评论设置 -->
    <div class="settings-section">
      <HandDrawnCard class="settings-card">
        <h3 class="section-title">评论设置</h3>
        <p class="section-desc">控制匿名评论的行为</p>

        <div class="setting-item">
          <div class="setting-info">
            <div class="setting-label">评论频率限制</div>
            <div class="setting-desc">
              每 {{ commentRateWindow }} 秒内最多可发送 {{ commentRateLimit }} 条评论
            </div>
          </div>
          <div class="setting-control">
            <n-space>
              <n-input-number
                v-model:value="commentRateWindow"
                :min="10"
                :max="3600"
                style="width: 120px"
              >
                <template #suffix>秒</template>
              </n-input-number>
              <span class="divider">/</span>
              <n-input-number
                v-model:value="commentRateLimit"
                :min="1"
                :max="100"
                style="width: 120px"
              >
                <template #suffix>条</template>
              </n-input-number>
              <n-button type="primary" @click="saveCommentRateLimit" :loading="saving">
                保存
              </n-button>
            </n-space>
          </div>
        </div>
      </HandDrawnCard>
    </div>

    <!-- 关于设置 -->
    <div class="settings-section">
      <HandDrawnCard class="settings-card">
        <h3 class="section-title">关于设置</h3>
        <p class="section-desc">系统预设配置说明</p>

        <div class="setting-item">
          <div class="setting-info">
            <div class="setting-label">JWT 令牌过期时间</div>
            <div class="setting-desc">管理员登录令牌的有效期</div>
          </div>
          <div class="setting-control">
            <n-tag type="info">{{ jwtExpireMinutes / 60 }} 小时</n-tag>
          </div>
        </div>

        <div class="setting-item">
          <div class="setting-info">
            <div class="setting-label">服务重启影响</div>
            <div class="setting-desc">使用 JWT 无状态认证，服务重启后无需重新登录</div>
          </div>
          <div class="setting-control">
            <n-tag type="success">已启用</n-tag>
          </div>
        </div>
      </HandDrawnCard>
    </div>

    <!-- 操作成功提示 -->
    <n-message-provider>
      <n-notification-provider>
        <n-dialog-provider>
          <div></div>
        </n-dialog-provider>
      </n-notification-provider>
    </n-message-provider>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useMessage } from 'naive-ui'
import HandDrawnCard from '@/components/HandDrawnCard.vue'
import HandDrawnIcon from '@/components/HandDrawnIcon.vue'
import { settingsApi } from '@/api'

const message = useMessage()
const saving = ref(false)

// 评论频率限制
const commentRateLimit = ref(5)
const commentRateWindow = ref(60)
const jwtExpireMinutes = ref(1440)

// 加载设置
const loadSettings = async () => {
  try {
    const response = await settingsApi.getSettings()
    for (const setting of response.settings) {
      switch (setting.key) {
        case 'comment_rate_limit':
          commentRateLimit.value = parseInt(setting.value) || 5
          break
        case 'comment_rate_window':
          commentRateWindow.value = parseInt(setting.value) || 60
          break
        case 'jwt_expire_minutes':
          jwtExpireMinutes.value = parseInt(setting.value) || 1440
          break
      }
    }
  } catch (error) {
    console.error('加载设置失败:', error)
    message.error('加载设置失败')
  }
}

// 保存评论频率限制
const saveCommentRateLimit = async () => {
  saving.value = true
  try {
    await settingsApi.updateSetting(
      'comment_rate_limit',
      String(commentRateLimit.value),
      '评论频率限制：每时间窗口内最多评论次数'
    )
    await settingsApi.updateSetting(
      'comment_rate_window',
      String(commentRateWindow.value),
      '评论频率限制：时间窗口（秒）'
    )
    message.success('评论频率限制已更新')
  } catch (error) {
    console.error('保存设置失败:', error)
    message.error('保存设置失败')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  loadSettings()
})
</script>

<style scoped>
.admin-settings {
  max-width: 800px;
  margin: 0 auto;
  padding: 24px;
}

.settings-header {
  margin-bottom: 32px;
}

.settings-title {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 8px;
}

.settings-subtitle {
  color: var(--n-text-color-secondary);
}

.settings-section {
  margin-bottom: 24px;
}

.settings-card {
  padding: 24px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
}

.section-desc {
  color: var(--n-text-color-secondary);
  font-size: 14px;
  margin-bottom: 24px;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0;
  border-bottom: 1px dashed var(--n-border-color);
}

.setting-item:last-child {
  border-bottom: none;
}

.setting-label {
  font-weight: 500;
  margin-bottom: 4px;
}

.setting-desc {
  color: var(--n-text-color-secondary);
  font-size: 13px;
}

.setting-control {
  display: flex;
  align-items: center;
  gap: 12px;
}

.divider {
  color: var(--n-text-color-secondary);
}
</style>
