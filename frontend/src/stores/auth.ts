/**
 * Admin Store - 博主管理认证状态管理
 *
 * 本模块使用 Pinia 管理博主管理后台的认证状态，
 * 使用简单的密码验证而非用户系统。
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { adminApi } from '@/api'
import router from '@/router'

/**
 * 创建 Admin Store
 */
export const useAdminStore = defineStore('admin', () => {
  // ========== 状态定义 ==========

  /**
   * 管理员 Token
   */
  const token = ref<string | null>(null)

  /**
   * 加载状态
   */
  const loading = ref(false)

  /**
   * 错误信息
   */
  const error = ref<string | null>(null)

  /**
   * 初始化完成状态
   */
  const initialized = ref(false)

  // ========== 计算属性 ==========

  /**
   * 是否已登录管理员
   */
  const isLoggedIn = computed(() => !!token.value)

  // ========== 方法定义 ==========

  /**
   * 初始化 - 从本地存储恢复登录状态
   */
  const init = async () => {
    // 迁移旧 localStorage key
    const oldToken = localStorage.getItem('token')
    const newToken = localStorage.getItem('adminToken')

    if (oldToken && !newToken) {
      // 迁移旧 token 到新 key
      localStorage.setItem('adminToken', oldToken)
      localStorage.removeItem('token')
      token.value = oldToken
    } else {
      token.value = newToken
    }
    initialized.value = true
  }

  /**
   * 管理员登录
   */
  const login = async (password: string): Promise<boolean> => {
    loading.value = true
    error.value = null

    try {
      const response = await adminApi.login(password)

      if (response.success && response.token) {
        token.value = response.token
        localStorage.setItem('adminToken', response.token)
        return true
      } else {
        error.value = response.message || '登录失败'
        return false
      }
    } catch (e: any) {
      error.value = e.response?.data?.message || '登录失败，请稍后重试'
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * 管理员登出
   */
  const logout = async () => {
    // 调用后端登出接口使 token 失效
    try {
      await adminApi.logout()
    } catch {
      // 忽略登出接口错误
    }

    token.value = null
    localStorage.removeItem('adminToken')
    router.push('/')
  }

  /**
   * 获取认证头
   */
  const getAuthHeader = () => {
    return token.value ? { Authorization: `Bearer ${token.value}` } : {}
  }

  // ========== 返回暴露的接口 ==========

  return {
    token,
    loading,
    error,
    initialized,
    isLoggedIn,
    init,
    login,
    logout,
    getAuthHeader
  }
})

// 向后兼容别名：useAuthStore 与 useAdminStore 等价
// 建议使用 useAdminStore 以保持命名一致性
export { useAdminStore as useAuthStore }
