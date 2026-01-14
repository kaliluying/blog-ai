<template>
  <div class="admin-login-container">
    <div class="login-card">
      <h1>管理员登录</h1>
      <p class="subtitle">请输入管理员密码</p>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="password">密码</label>
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="请输入密码"
            :disabled="loading"
            autocomplete="off"
          />
        </div>

        <p v-if="error" class="error-message">{{ error }}</p>

        <button type="submit" class="login-button" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>

      <div class="back-link">
        <router-link to="/">返回首页</router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAdminStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const adminStore = useAdminStore()

const password = ref('')
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  if (!password.value) {
    error.value = '请输入密码'
    return
  }

  loading.value = true
  error.value = ''

  try {
    const success = await adminStore.login(password.value)

    if (success) {
      // 登录成功，跳转到目标页面或管理页面
      const redirect = route.query.redirect as string
      router.push(redirect || '/admin/posts')
    } else {
      error.value = adminStore.error || '密码错误'
    }
  } catch {
    error.value = '登录失败，请稍后重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.admin-login-container {
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.login-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 2.5rem;
  width: 100%;
  max-width: 400px;
  text-align: center;
}

h1 {
  margin: 0 0 0.5rem;
  font-size: 1.75rem;
  color: #333;
}

.subtitle {
  margin: 0 0 2rem;
  color: #666;
  font-size: 0.95rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  text-align: left;
}

label {
  font-size: 0.9rem;
  color: #555;
  font-weight: 500;
}

input {
  padding: 0.75rem 1rem;
  border: 2px solid #e8e8e8;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

input:focus {
  outline: none;
  border-color: #4a9eff;
}

input:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
}

.error-message {
  color: #e74c3c;
  font-size: 0.9rem;
  margin: 0;
  padding: 0.75rem;
  background: #fdf2f2;
  border-radius: 6px;
}

.login-button {
  padding: 0.875rem;
  background: #4a9eff;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s, transform 0.1s;
}

.login-button:hover:not(:disabled) {
  background: #3a8eef;
}

.login-button:active:not(:disabled) {
  transform: scale(0.98);
}

.login-button:disabled {
  background: #a0c4ff;
  cursor: not-allowed;
}

.back-link {
  margin-top: 1.5rem;
  font-size: 0.9rem;
}

.back-link a {
  color: #666;
  text-decoration: none;
}

.back-link a:hover {
  color: #4a9eff;
}
</style>
