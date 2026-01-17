/**
 * useLoginDialog composable - 登录对话框
 *
 * 提供可复用的登录对话框功能，
 * 用于需要管理员权限的操作。
 */

import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage, useDialog } from 'naive-ui'
import { useAuthStore } from '@/stores/auth'

/**
 * 登录对话框 composable
 *
 * @param options 配置选项
 */
export function useLoginDialog(options: {
  onSuccess?: () => void
  onCancel?: () => void
  title?: string
  content?: string
} = {}) {
  const router = useRouter()
  const message = useMessage()
  const dialog = useDialog()
  const authStore = useAuthStore()

  const passwordRef = ref('')

  /**
   * 安全地返回上一页（如果在路由环境中）
   */
  const safeBack = () => {
    try {
      router.back()
    } catch {
      // 如果不在路由环境中，忽略错误
    }
  }

  /**
   * 显示登录对话框
   */
  const showLoginDialog = () => {
    passwordRef.value = ''

    dialog.create({
      title: options.title || '博主登录',
      content: options.content || '请输入管理员密码以继续',
      positiveText: '登录',
      negativeText: '返回',
      maskClosable: false,
      onPositiveClick: async () => {
        if (!passwordRef.value) {
          message.warning('请输入密码')
          return false
        }
        const success = await authStore.login(passwordRef.value)
        if (success) {
          message.success('登录成功')
          options.onSuccess?.()
        } else {
          message.error(authStore.error || '密码错误')
          return false
        }
      },
      onNegativeClick: () => {
        options.onCancel?.()
        safeBack()
      }
    })
  }

  return {
    showLoginDialog
  }
}
