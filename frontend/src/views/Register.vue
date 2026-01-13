<template>
  <div class="register-page">
    <n-card title="用户注册" class="register-card">
      <n-form ref="formRef" :model="formData" :rules="rules">
        <n-form-item label="用户名" path="username">
          <n-input v-model:value="formData.username" placeholder="请输入用户名（3-20字符）" />
        </n-form-item>

        <n-form-item label="邮箱" path="email">
          <n-input v-model:value="formData.email" placeholder="请输入邮箱" />
        </n-form-item>

        <n-form-item label="密码" path="password">
          <n-input
            v-model:value="formData.password"
            type="password"
            placeholder="请输入密码（至少6位）"
          />
        </n-form-item>

        <n-form-item label="确认密码" path="confirmPassword">
          <n-input
            v-model:value="formData.confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            @keyup.enter="handleRegister"
          />
        </n-form-item>

        <n-alert v-if="authStore.error" type="error" :show-icon="true" class="error-alert">
          {{ authStore.error }}
        </n-alert>

        <n-button
          type="primary"
          block
          :loading="authStore.loading"
          @click="handleRegister"
        >
          注册
        </n-button>
      </n-form>

      <div class="form-footer">
        <span>已有账号？</span>
        <router-link to="/login">立即登录</router-link>
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
  email: '',
  password: '',
  confirmPassword: ''
})

const validateConfirmPassword = (_rule: any, value: string) => {
  if (value !== formData.password) {
    return new Error('两次输入的密码不一致')
  }
  return true
}

const rules = {
  username: [
    { required: true, message: '请输入用户名' },
    { min: 3, max: 20, message: '用户名必须是3-20个字符' }
  ],
  email: [
    { required: true, message: '请输入邮箱' },
    { type: 'email', message: '请输入有效的邮箱地址' }
  ],
  password: [
    { required: true, message: '请输入密码' },
    { min: 6, message: '密码至少6个字符' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码' },
    { validator: validateConfirmPassword }
  ]
}

const handleRegister = async () => {
  if (formData.password !== formData.confirmPassword) {
    message.error('两次输入的密码不一致')
    return
  }

  const success = await authStore.register(formData.username, formData.email, formData.password)
  if (success) {
    message.success('注册成功！欢迎加入我们~')
    router.push('/')
  }
}
</script>

<style scoped>
.register-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
  padding: 20px;
}

.register-card {
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
