/**
 * Theme Store - 主题状态管理
 *
 * 本模块使用 Pinia 管理应用的主题模式（浅色/深色），
 * 支持手动切换，并持久化存储用户选择。
 *
 * 功能：
 * - 两种主题模式：浅色（light）、深色（dark）
 * - 主题持久化（localStorage）
 * - CSS 变量和 class 动态更新
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

/**
 * 主题模式类型定义
 */
export type ThemeMode = 'light' | 'dark'

/**
 * 创建 Theme Store
 * 使用 Vue 3 Composition API 风格（setup 语法）
 */
export const useThemeStore = defineStore('theme', () => {
  // ========== 状态定义 ==========

  /**
   * 当前主题模式
   * 默认值：'light'（浅色模式）
   * 可通过 localStorage 恢复用户上次选择
   */
  const theme = ref<ThemeMode>('light')

  /**
   * 是否为深色模式
   */
  const isDark = computed(() => theme.value === 'dark')

  // ========== 方法定义 ==========

  /**
   * 初始化主题
   *
   * 从 localStorage 恢复用户上次选择的主题，
   * 并应用主题样式。
   */
  const init = () => {
    // 从本地存储恢复主题设置
    const saved = localStorage.getItem('themeMode') as ThemeMode | null
    if (saved) {
      theme.value = saved
    }

    // 应用当前主题到 DOM
    updateTheme()
  }

  /**
   * 设置主题模式
   *
   * @param newTheme 要切换的新主题模式
   */
  const setTheme = (newTheme: ThemeMode) => {
    theme.value = newTheme
    // 持久化存储用户选择
    localStorage.setItem('themeMode', newTheme)
    // 更新 DOM 样式
    updateTheme()
  }

  /**
   * 切换主题
   *
   * 在浅色和深色之间切换
   */
  const toggleTheme = () => {
    if (theme.value === 'light') {
      setTheme('dark')
    } else {
      setTheme('light')
    }
  }

  /**
   * 更新 DOM 主题样式
   *
   * 通过设置 HTML 元素的 data-theme 属性和 dark class，
   * 配合 CSS 变量实现主题切换效果。
   */
  const updateTheme = () => {
    // 设置 data-theme 属性
    document.documentElement.setAttribute('data-theme', theme.value)

    // 根据深浅模式添加/移除 dark class
    if (isDark.value) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  // ========== 返回暴露的接口 ==========

  return {
    theme,
    isDark,
    init,
    setTheme,
    toggleTheme,
    updateTheme,
  }
})
