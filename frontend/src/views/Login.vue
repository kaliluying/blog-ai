<template>
  <div class="login-page">
    <n-card title="用户登录" class="login-card">
      <n-form ref="formRef" :model="formData" :rules="rules">
        <n-form-item label="用户名" path="username">
          <n-input v-model:value="formData.username" placeholder="请输入用户名" />
        </n-form-item>

        <n-form-item label="密码" path="password">
          <n-input
            v-model:value="formData.password"
            type="password"
            placeholder="请输入密码"
            @keyup.enter="handleLogin"
          />
        </n-form-item>

        <n-alert v-if="authStore.error" type="error" :show-icon="true" class="error-alert">
          {{ authStore.error }}
        </n-alert>

        <n-button
          type="primary"
          block
          :loading="authStore.loading"
          @click="handleLogin"
        >
          登录
        </n-button>
      </n-form>

      <div class="form-footer">
        <span>还没有账号？</span>
        <router-link to="/register">立即注册</router-link>
      </div>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage } from 'naive-ui'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const message = useMessage()
const authStore = useAuthStore()

const formData = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名' }],
  password: [{ required: true, message: '请输入密码' }]
}

const handleLogin = async () => {
  const success = await authStore.login(formData.username, formData.password)
  if (success) {
    message.success('登录成功！')
    router.push('/')
  }
}
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 400px;
}

.error-alert {
  margin-bottom: 16px;
}

.form-footer {
  margin-top: 16px;
  text-align: center;
  color: #666;
}

.form-footer a {
  color: #34495e;
  font-weight: 600;
  margin-left: 8px;
}

.form-footer a:hover {
  text-decoration: underline;
}
</style>
