/**
 * Blog Store - 博客文章状态管理
 *
 * 本模块使用 Pinia 管理博客文章的全局状态，
 * 提供文章数据的获取、缓存和查询功能。
 *
 * 状态包含：
 * - posts: 文章列表
 * - loading: 加载状态
 * - error: 错误信息
 */

import { defineStore } from 'pinia'
import { ref } from 'vue'
import { blogApi, viewApi } from '@/api'
import type { BlogPost, ViewCountResponse } from '@/types'

/**
 * 创建博客 Store
 * 使用 Vue 3 Composition API 风格（setup 语法）
 */
export const useBlogStore = defineStore('blog', () => {
  // ========== 状态定义 ==========

  /**
   * 文章列表
   * 存储从后端获取的所有文章数据
   */
  const posts = ref<BlogPost[]>([])

  /**
   * 加载状态
   * 用于控制页面上的加载指示器显示
   */
  const loading = ref(false)

  /**
   * 错误信息
   * 当请求失败时存储错误描述
   */
  const error = ref<string | null>(null)

  /**
   * 原始错误对象
   * 当请求失败时存储原始错误，用于调试和详细错误处理
   */
  const originalError = ref<Error | null>(null)

  /**
   * 热门文章列表
   * 存储阅读量最高的文章
   */
  const popularPosts = ref<BlogPost[]>([])

  /**
   * 文章总数
   */
  const totalCount = ref(0)

  /**
   * 当前页码
   */
  const currentPage = ref(1)

  /**
   * 每页数量
   */
  const pageSize = ref(10)

  // ========== 辅助函数 ==========

  /**
   * 设置加载状态
   */
  const setLoading = (isLoading: boolean) => {
    loading.value = isLoading
  }

  /**
   * 设置错误状态
   */
  const setError = (err: string, original?: Error) => {
    error.value = err
    originalError.value = original instanceof Error ? original : original ? new Error(String(original)) : null
    console.error(original)
  }

  /**
   * 重置错误状态
   */
  const resetError = () => {
    error.value = null
    originalError.value = null
  }

  // ========== 方法定义 ==========

  /**
   * 获取所有文章
   *
   * 从后端 API 获取文章列表，更新 posts 状态。
   * 包含完整的错误处理。
   */
  const fetchPosts = async (page: number = 1, size: number = 10) => {
    setLoading(true)
    resetError()

    currentPage.value = page
    pageSize.value = size

    const skip = (page - 1) * size

    try {
      const [postsData, countData] = await Promise.all([
        blogApi.getPosts(skip, size),
        blogApi.getPostCount(),
      ])
      posts.value = postsData || []
      totalCount.value = typeof countData === 'number' ? countData : 0
    } catch (e) {
      setError('获取文章列表失败', e instanceof Error ? e : new Error(String(e)))
    } finally {
      setLoading(false)
    }
  }

  /**
   * 获取所有文章（不分页）
   */
  const fetchAllPosts = async (includeScheduled: boolean = false) => {
    setLoading(true)
    resetError()

    try {
      posts.value = await blogApi.getPosts(0, 1000, includeScheduled)
    } catch (e) {
      setError('获取文章列表失败', e instanceof Error ? e : new Error(String(e)))
    } finally {
      setLoading(false)
    }
  }

  /**
   * 获取所有文章（包括定时发布的）
   * 供管理员使用
   */
  const fetchAdminPosts = async () => {
    await fetchAllPosts(true)
  }

  /**
   * 根据 ID 查找文章（从缓存中）
   *
   * @param id 文章 ID
   * @returns 找到的文章或 undefined
   */
  const getPostById = (id: number) => {
    return posts.value.find((post: BlogPost) => post.id === id)
  }

  /**
   * 获取单篇文章
   *
   * 如果文章已在缓存中，直接返回；
   * 否则从后端获取，并更新缓存。
   *
   * @param id 文章 ID
   * @returns 文章数据或 null（获取失败时）
   */
  const fetchPostById = async (id: number): Promise<BlogPost | null> => {
    setLoading(true)
    resetError()

    try {
      // 从后端获取文章详情
      const post = await blogApi.getPost(id)

      // 如果文章不在缓存列表中，添加到列表
      if (!posts.value.find((p: BlogPost) => p.id === id)) {
        posts.value.push(post)
      }

      return post
    } catch (e) {
      setError('获取文章失败', e instanceof Error ? e : new Error(String(e)))
      return null
    } finally {
      setLoading(false)
    }
  }

  /**
   * 获取热门文章排行
   *
   * 从后端获取阅读量最高的文章列表。
   *
   * @param limit 返回数量，默认 5
   */
  const fetchPopularPosts = async (limit: number = 5) => {
    try {
      popularPosts.value = await viewApi.getPopularPosts(limit)
    } catch (e) {
      console.error('获取热门文章失败', e)
    }
  }

  /**
   * 记录并获取文章的阅读量
   *
   * 调用后端 API 记录文章阅读量（同一 IP 24 小时内只计一次），
   * 同时更新本地缓存的阅读量。
   *
   * @param postId 文章 ID
   * @returns 当前阅读量，失败返回 0
   */
  const recordAndGetViewCount = async (postId: number): Promise<number> => {
    try {
      const result: ViewCountResponse = await viewApi.recordView(postId)
      // 更新缓存中的阅读量
      const post = posts.value.find((p: BlogPost) => p.id === postId)
      if (post) {
        post.view_count = result.view_count
      }
      return result.view_count
    } catch (e) {
      console.error('获取阅读量失败', e)
      return 0
    }
  }

  // ========== 返回暴露的接口 ==========

  return {
    posts,
    loading,
    error,
    originalError,
    popularPosts,
    totalCount,
    currentPage,
    pageSize,
    fetchPosts,
    fetchAllPosts,
    fetchAdminPosts,
    getPostById,
    fetchPostById,
    fetchPopularPosts,
    recordAndGetViewCount,
  }
})
