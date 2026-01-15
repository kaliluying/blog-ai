/**
 * Vue 3 应用入口文件
 *
 * 本文件负责初始化 Vue 应用实例，配置并注册核心依赖：
 * - Pinia: 状态管理
 * - Naive UI: UI 组件库
 * - Vue Router: 路由管理
 */

// 从 vue 包中导入 createApp 函数，用于创建 Vue 应用实例
import { createApp } from 'vue'

// 从 pinia 包中导入 createPinia 函数，用于创建状态管理实例
import { createPinia } from 'pinia'

// 从 naive-ui 包中导入 Naive UI 组件库和暗色主题
import NaiveUI, { darkTheme } from 'naive-ui'

// 导入根组件 App.vue
import App from './App.vue'

// 导入路由配置
import router from './router'

// 导入主题 store 用于初始化
import { useThemeStore } from './stores/theme'

// 创建 Vue 应用实例，传入根组件
const app = createApp(App)

// 注册 Pinia 状态管理
app.use(createPinia())

// 注册 Naive UI 组件库
app.use(NaiveUI)

// 注册路由
app.use(router)

// 初始化主题
const themeStore = useThemeStore()
themeStore.init()

// 将应用挂载到 DOM 中的 #app 元素
app.mount('#app')

// 监听主题变化，更新 Naive UI 主题
themeStore.$subscribe(() => {
  const configProvider = document.querySelector('.n-config-provider') as HTMLElement & {
    __vue_parent_app?: {
      ctx: { config: { globalProperties: { $configProvider?: { theme: unknown } } } }
    }
  }
  if (configProvider) {
    const app = configProvider.__vue_parent_app
    if (app && app.ctx && app.ctx.config && app.ctx.config.globalProperties) {
      const provider = app.ctx.config.globalProperties.$configProvider
      if (provider) {
        provider.theme = themeStore.isDark ? darkTheme : null
      }
    }
  }
})
