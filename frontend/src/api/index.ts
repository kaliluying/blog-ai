/**
 * API 模块 - 后端接口封装
 *
 * 本模块使用 Axios 封装了与后端 FastAPI 服务器的所有 HTTP 请求。
 * 包含：
 * 1. Axios 实例配置（基础 URL、超时、拦截器、认证）
 * 2. 博客文章相关的 API 方法
 * 3. 匿名评论 API 方法
 */

import axios from 'axios'
import type {
  BlogPost,
  BlogPostCreate,
  BlogPostUpdate,
  TitleCheckRequest,
  TitleCheckResponse,
  Comment,
  CommentCreate,
  ArchiveGroup,
  ArchiveYear,
  ViewCountResponse,
  AdminLoginResponse,
  DashboardStats,
  AdminCommentsResponse,
} from '@/types'

/**
 * 创建 Axios 实例
 *
 * baseURL: 从环境变量读取后端 API 地址，默认 localhost:8000
 * timeout: 请求超时时间 10 秒
 * headers: 默认请求头配置
 */
const api = axios.create({
  // 环境变量 VITE_API_BASE_URL 可配置后端地址
  // 生产环境留空，通过 Nginx 代理 /api 到后端
  baseURL: import.meta.env.VITE_API_BASE_URL || '',

  // 请求超时时间（毫秒）
  timeout: 10000,

  // 默认请求头
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * 请求拦截器 - 自动添加管理员 Token
 */
api.interceptors.request.use(
  (config: import('axios').InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('adminToken')
    if (token) {
      config.headers.set('Authorization', `Bearer ${token}`)
    }
    return config
  },
  (error: unknown) => {
    return Promise.reject(error)
  },
)

/**
 * 响应拦截器
 *
 * 在请求响应后统一处理：
 * 1. 提取响应数据（response.data）
 * 2. 错误处理：统一错误格式，401 时清除 token 并可扩展通知用户
 */
api.interceptors.response.use(
  // 成功响应：直接返回 data 部分
  (response: import('axios').AxiosResponse) => response.data,

  // 错误响应
  (error: unknown) => {
    const axiosError = error as import('axios').AxiosError

    // 401 未授权 - 清除失效的 token
    if (axiosError.response?.status === 401) {
      localStorage.removeItem('adminToken')
      // 可扩展：发送事件通知用户需要重新登录
      // dispatch('auth/logout')
    }

    // 返回统一格式的错误信息
    const errorData = axiosError.response?.data as Record<string, unknown> | undefined
    const errorMessage = (errorData?.message as string) ||
      axiosError.message ||
      '请求失败，请稍后重试'

    return Promise.reject({
      message: errorMessage,
      status: axiosError.response?.status,
      originalError: axiosError,
    })
  },
)

// ========== 博客 API ==========

export const blogApi = {
  /**
   * 获取所有文章列表
   * @param skip 跳过的记录数，默认 0
   * @param limit 返回的最大记录数，默认 100
   * @param includeScheduled 是否包含定时发布的文章，默认 false
   * @returns Promise<BlogPost[]> 文章数组
   */
  getPosts: async (skip: number = 0, limit: number = 100, includeScheduled: boolean = false): Promise<BlogPost[]> => {
    return api.get('/api/posts', { params: { skip, limit, include_scheduled: includeScheduled } })
  },

  /**
   * 获取文章总数
   * @returns Promise<number> 文章总数
   */
  getPostCount: async (): Promise<number> => {
    const response = (await api.get('/api/posts/count')) as { count: number }
    return response.count ?? 0
  },

  /**
   * 获取单篇文章详情
   * @param id 文章 ID
   * @returns Promise<BlogPost> 文章详情
   */
  getPost: async (id: number): Promise<BlogPost> => {
    return api.get(`/api/posts/${id}`)
  },

  /**
   * 检查标题是否已存在
   * @param data 标题检查请求
   * @returns Promise<TitleCheckResponse> 检查结果
   */
  checkTitle: async (data: TitleCheckRequest): Promise<TitleCheckResponse> => {
    return api.post('/api/posts/check-title', data)
  },

  /**
   * 创建新文章（需要管理员认证）
   * @param post 文章数据（不含 id 和 date，由后端生成）
   * @returns Promise<BlogPost> 创建后的文章（含 id）
   */
  createPost: async (post: BlogPostCreate): Promise<BlogPost> => {
    return api.post('/api/posts', post)
  },

  /**
   * 更新文章（需要管理员认证）
   * @param id 文章 ID
   * @param post 要更新的字段（部分更新）
   * @returns Promise<BlogPost> 更新后的文章
   */
  updatePost: async (id: number, post: BlogPostUpdate): Promise<BlogPost> => {
    return api.put(`/api/posts/${id}`, post)
  },

  /**
   * 删除文章（需要管理员认证）
   * @param id 要删除的文章 ID
   * @returns Promise<void>
   */
  deletePost: async (id: number): Promise<void> => {
    return api.delete(`/api/posts/${id}`)
  },

  /**
   * 搜索文章
   * @param query 搜索关键词
   * @returns Promise<BlogPost[]> 搜索结果
   */
  searchPosts: async (query: string): Promise<BlogPost[]> => {
    return api.get('/api/search', { params: { q: query } })
  },

  /**
   * 获取相关文章推荐
   * @param postId 当前文章 ID
   * @param limit 返回数量，默认 5
   * @returns Promise<BlogPost[]> 相关文章列表
   */
  getRelatedPosts: async (postId: number, limit: number = 5): Promise<BlogPost[]> => {
    return api.get(`/api/posts/${postId}/related`, { params: { limit } })
  },
}

// ========== 评论 API ==========

export const commentApi = {
  /**
   * 获取文章的评论列表
   * @param postId 文章 ID
   * @param sort 排序方式：'newest' 最新优先，'oldest' 最早优先，默认 'newest'
   * @returns Promise<Comment[]> 评论列表
   */
  getComments: async (postId: number, sort: 'newest' | 'oldest' = 'newest'): Promise<Comment[]> => {
    return api.get(`/api/posts/${postId}/comments`, { params: { sort } })
  },

  /**
   * 创建匿名评论
   * @param data 评论数据
   * @returns Promise<Comment> 创建的评论
   */
  createComment: async (data: CommentCreate): Promise<Comment> => {
    return api.post('/api/comments', data)
  },

  /**
   * 删除评论（需要管理员认证）
   * @param commentId 评论 ID
   * @returns Promise<void>
   */
  deleteComment: async (commentId: number): Promise<void> => {
    return api.delete(`/api/comments/${commentId}`)
  },
}

// ========== 归档 API ==========

export const archiveApi = {
  /**
   * 获取所有归档
   * @returns Promise<ArchiveYear[]> 归档列表
   */
  getArchive: async (): Promise<ArchiveYear[]> => {
    return api.get('/api/archive')
  },

  /**
   * 获取指定年份的归档
   * @param year 年份
   * @returns Promise<ArchiveYear> 年度归档
   */
  getArchiveByYear: async (year: number): Promise<ArchiveYear> => {
    return api.get(`/api/archive/${year}`)
  },

  /**
   * 获取指定年月的归档
   * @param year 年份
   * @param month 月份
   * @returns Promise<ArchiveGroup> 月度归档
   */
  getArchiveByYearMonth: async (year: number, month: number): Promise<ArchiveGroup> => {
    return api.get(`/api/archive/${year}/${month}`)
  },
}

// ========== 阅读量 API ==========

export const viewApi = {
  /**
   * 记录文章浏览
   * @param postId 文章 ID
   * @returns Promise<ViewCountResponse> 是否计数及当前阅读量
   */
  recordView: async (postId: number): Promise<ViewCountResponse> => {
    return api.post(`/api/posts/${postId}/view`)
  },

  /**
   * 获取热门文章排行
   * @param limit 返回数量，默认 5
   * @returns Promise<BlogPost[]> 热门文章列表
   */
  getPopularPosts: async (limit: number = 5): Promise<BlogPost[]> => {
    return api.get('/api/posts/popular', { params: { limit } })
  },
}

// ========== 管理员认证 API ==========

export const adminApi = {
  /**
   * 管理员登录
   * @param password 管理员密码
   * @returns Promise<AdminLoginResponse> 登录结果及 token
   */
  login: async (password: string): Promise<AdminLoginResponse> => {
    return api.post('/api/admin/login', { password })
  },

  /**
   * 管理员登出
   * @returns Promise<void>
   */
  logout: async (): Promise<void> => {
    return api.post('/api/admin/logout')
  },

  /**
   * 获取仪表盘统计数据
   * @returns Promise<DashboardStats> 包含文章数、评论数、总阅读量等
   */
  getStats: async (): Promise<DashboardStats> => {
    return api.get('/api/admin/stats')
  },

  /**
   * 获取所有评论（管理后台）
   * @param skip 跳过的记录数
   * @param limit 返回数量限制
   * @param postId 按文章 ID 筛选
   * @param keyword 按昵称或内容搜索
   * @returns Promise<AdminCommentsResponse> 评论列表
   */
  getComments: async (
    skip: number = 0,
    limit: number = 50,
    postId?: number,
    keyword?: string
  ): Promise<AdminCommentsResponse> => {
    return api.get('/api/admin/comments', {
      params: { skip, limit, post_id: postId, keyword }
    })
  },

  /**
   * 删除评论（管理后台）
   * @param commentId 评论 ID
   * @returns Promise<void>
   */
  deleteComment: async (commentId: number): Promise<void> => {
    return api.delete(`/api/comments/${commentId}`)
  },
}

// ========== 设置 API ==========

export interface SettingItem {
  key: string
  value: string
  description?: string
}

export interface SettingsResponse {
  settings: SettingItem[]
}

export const settingsApi = {
  /**
   * 获取所有设置
   * @returns Promise<SettingsResponse> 设置列表
   */
  getSettings: async (): Promise<SettingsResponse> => {
    return api.get('/api/admin/settings')
  },

  /**
   * 创建或更新设置
   * @param key 设置键
   * @param value 设置值
   * @param description 设置描述（可选）
   * @returns Promise<SettingItem> 更新后的设置
   */
  updateSetting: async (
    key: string,
    value: string,
    description?: string
  ): Promise<SettingItem> => {
    return api.post('/api/admin/settings', { key, value, description })
  },
}

// 导出 Axios 实例（可自定义配置时使用）
export default api
