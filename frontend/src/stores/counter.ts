/**
 * Counter Store - 计数器状态管理（示例/模板）
 *
 * 本模块是一个简单的计数器 Store 模板，
 * 演示 Pinia + Vue 3 Composition API 的基本用法。
 *
 * 包含功能：
 * - 计数器递增
 * - 计算属性（双倍计数）
 */

// 从 vue 导入 ref（响应式引用）和 computed（计算属性）
import { ref, computed } from 'vue'

// 从 pinia 导入 defineStore 用于创建 store
import { defineStore } from 'pinia'

/**
 * 创建计数器 Store
 *
 * 这是一个示例 Store，展示了 Pinia 的基本模式：
 * 1. 使用 ref 定义响应式状态
 * 2. 使用 computed 定义计算属性
 * 3. 定义操作状态的方法
 */
export const useCounterStore = defineStore('counter', () => {
  // ========== 状态 ==========

  /**
   * 计数器值
   * 使用 ref 包装为响应式数据
   */
  const count = ref(0)

  // ========== 计算属性 ==========

  /**
   * 双倍计数
   * 依赖 count 自动更新
   */
  const doubleCount = computed(() => count.value * 2)

  // ========== 方法 ==========

  /**
   * 计数器递增
   * 将 count 值加 1
   */
  function increment() {
    count.value++
  }

  // ========== 返回暴露的接口 ==========

  return {
    count,           // 计数器值
    doubleCount,     // 双倍计数（计算属性）
    increment        // 递增方法
  }
})
