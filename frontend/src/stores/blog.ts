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
import { blogApi, viewApi, type BlogPost, type ViewCountResponse } from '@/api'

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
   * 热门文章列表
   * 存储阅读量最高的文章
   */
  const popularPosts = ref<BlogPost[]>([])

  // ========== 方法定义 ==========

  /**
   * 获取所有文章
   *
   * 从后端 API 获取文章列表，更新 posts 状态。
   * 包含完整的错误处理。
   */
  const fetchPosts = async () => {
    loading.value = true   // 开始加载
    error.value = null     // 清空错误

    try {
      // 调用 API 获取文章列表
      posts.value = await blogApi.getPosts()
    } catch (e) {
      // 请求失败：设置错误信息
      error.value = '获取文章列表失败'
      console.error(e)
    } finally {
      // 无论成功或失败，都结束加载状态
      loading.value = false
    }
  }

  /**
   * 根据 ID 查找文章（从缓存中）
   *
   * @param id 文章 ID
   * @returns 找到的文章或 undefined
   */
  const getPostById = (id: number) => {
    return posts.value.find(post => post.id === id)
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
    loading.value = true
    error.value = null

    try {
      // 从后端获取文章详情
      const post = await blogApi.getPost(id)

      // 如果文章不在缓存列表中，添加到列表
      if (!posts.value.find(p => p.id === id)) {
        posts.value.push(post)
      }

      return post
    } catch (e) {
      error.value = '获取文章失败'
      console.error(e)
      return null
    } finally {
      loading.value = false
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
   * 记录文章浏览
   *
   * 调用后端 API 记录文章阅读量。
   * 同一 IP 24 小时内只计一次。
   *
   * @param postId 文章 ID
   * @returns 是否成功计数
   */
  const recordView = async (postId: number): Promise<boolean> => {
    try {
      const result: ViewCountResponse = await viewApi.recordView(postId)
      // 更新文章阅读量
      const post = posts.value.find(p => p.id === postId)
      if (post) {
        post.view_count = result.view_count
      }
      return result.counted
    } catch (e) {
      console.error('记录浏览失败', e)
      return false
    }
  }

  /**
   * 获取并更新文章的阅读量
   *
   * @param postId 文章 ID
   * @returns 当前阅读量
   */
  const updatePostViewCount = async (postId: number): Promise<number> => {
    try {
      const result: ViewCountResponse = await viewApi.recordView(postId)
      // 更新缓存中的阅读量
      const post = posts.value.find(p => p.id === postId)
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
    posts,           // 文章列表
    loading,         // 加载状态
    error,           // 错误信息
    popularPosts,    // 热门文章
    fetchPosts,      // 获取所有文章
    getPostById,     // 查找文章（缓存）
    fetchPostById,   // 获取单篇文章
    fetchPopularPosts, // 获取热门文章
    recordView,      // 记录文章浏览
    updatePostViewCount // 获取并更新阅读量
  }
})
