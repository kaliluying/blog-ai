/**
 * Auth Store - 用户认证状态管理
 *
 * 本模块使用 Pinia 管理用户认证的全局状态，
 * 提供登录、注册、登出和用户信息查询功能。
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi, type User, type TokenResponse } from '@/api'
import router from '@/router'

/**
 * 创建认证 Store
 */
export const useAuthStore = defineStore('auth', () => {
  // ========== 状态定义 ==========

  /**
   * 用户信息
   */
  const user = ref<User | null>(null)

  /**
   * Token
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

  /**
   * 初始化 Promise（用于等待初始化完成）
   */
  let initPromise: Promise<void> | null = null

  // ========== 计算属性 ==========

  /**
   * 是否已登录
   */
  const isLoggedIn = computed(() => !!token.value && !!user.value)

  /**
   * 是否为管理员
   */
  const isAdmin = computed(() => user.value?.is_admin ?? false)

  // ========== 方法定义 ==========

  /**
   * 初始化 - 从本地存储恢复登录状态
   * 返回 Promise 供调用者等待初始化完成
   */
  const init = async () => {
    // 如果已经有初始化在进行中，返回同一个 Promise
    if (initPromise) return initPromise

    // 创建初始化 Promise
    initPromise = (async () => {
      const storedToken = localStorage.getItem('token')
      // 确保 token ref 与 localStorage 保持同步
      token.value = storedToken
      if (storedToken) {
        try {
          // 验证 token 有效性
          const userData = await authApi.getMe()
          user.value = userData
        } catch (e: any) {
          // 401 表示 token 无效或过期，静默清除状态
          if (e.response?.status === 401) {
            token.value = null
            user.value = null
            localStorage.removeItem('token')
          }
        }
      }
      initialized.value = true
    })()

    return initPromise
  }

  /**
   * 用户登录
   */
  const login = async (username: string, password: string) => {
    loading.value = true
    error.value = null

    try {
      const response = await authApi.login(username, password)
      handleAuthSuccess(response)
      return true
    } catch (e: any) {
      error.value = e.response?.data?.detail || '登录失败'
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * 用户注册
   */
  const register = async (username: string, email: string, password: string) => {
    loading.value = true
    error.value = null

    try {
      const response = await authApi.register(username, email, password)
      handleAuthSuccess(response)
      return true
    } catch (e: any) {
      error.value = e.response?.data?.detail || '注册失败'
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * 处理认证成功
   */
  const handleAuthSuccess = (response: TokenResponse) => {
    token.value = response.access_token
    user.value = response.user
    localStorage.setItem('token', response.access_token)
  }

  /**
   * 用户登出
   */
  const logout = () => {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    router.push('/')
  }

  // ========== 返回暴露的接口 ==========

  return {
    user,
    token,
    loading,
    error,
    initialized,
    isLoggedIn,
    isAdmin,
    init,
    login,
    register,
    logout
  }
})
