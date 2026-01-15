import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export type ThemeMode = 'light' | 'dark' | 'system'

export const useThemeStore = defineStore('theme', () => {
  const theme = ref<ThemeMode>('light')

  const isDark = computed(() => {
    if (theme.value === 'system') {
      return window.matchMedia('(prefers-color-scheme: dark)').matches
    }
    return theme.value === 'dark'
  })

  const init = () => {
    const saved = localStorage.getItem('themeMode') as ThemeMode | null
    if (saved) {
      theme.value = saved
    }
    updateTheme()

    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    const handleChange = () => {
      if (theme.value === 'system') {
        updateTheme()
      }
    }
    mediaQuery.addEventListener('change', handleChange)

    // 返回清理函数，用于移除事件监听器
    return () => mediaQuery.removeEventListener('change', handleChange)
  }

  const destroy = () => {
    const saved = localStorage.getItem('themeMode') as ThemeMode | null
    if (saved) {
      theme.value = saved
    }
    updateTheme()
  }

  const setTheme = (newTheme: ThemeMode) => {
    theme.value = newTheme
    localStorage.setItem('themeMode', newTheme)
    updateTheme()
  }

  const toggleTheme = () => {
    if (theme.value === 'light') {
      setTheme('dark')
    } else if (theme.value === 'dark') {
      setTheme('system')
    } else {
      setTheme('light')
    }
  }

  const updateTheme = () => {
    document.documentElement.setAttribute('data-theme', theme.value)
    if (isDark.value) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  return {
    theme,
    isDark,
    init,
    destroy,
    setTheme,
    toggleTheme,
    updateTheme,
  }
})
