/**
 * 异步状态管理 Composable
 * 提供统一的 loading、error、data 状态管理
 */

import { ref } from 'vue'

/**
 * 异步状态管理 hook
 *
 * @template T 数据类型
 * @returns 状态对象和执行函数
 *
 * @example
 * const { loading, error, data, execute } = useAsyncState<string>()
 * execute(fetchData())
 */
export function useAsyncState<T>() {
  const loading = ref(false)
  const error = ref<string | null>(null)
  const data = ref<T | null>(null)

  const execute = async (promise: Promise<T>): Promise<T> => {
    loading.value = true
    error.value = null
    try {
      data.value = await promise
      return data.value
    } catch (e) {
      error.value = e instanceof Error ? e.message : '操作失败'
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    error,
    data,
    execute
  }
}
