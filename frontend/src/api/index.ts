/**
 * API 模块 - 后端接口封装
 *
 * 本模块使用 Axios 封装了与后端 FastAPI 服务器的所有 HTTP 请求。
 * 包含：
 * 1. Axios 实例配置（基础 URL、超时、拦截器、认证）
 * 2. BlogPost 接口类型定义
 * 3. 博客文章相关的 API 方法
 * 4. 匿名评论 API 方法
 */

import axios from 'axios'

/**
 * 创建 Axios 实例
 *
 * baseURL: 从环境变量读取后端 API 地址，默认 localhost:8000
 * timeout: 请求超时时间 10 秒
 * headers: 默认请求头配置
 */
const api = axios.create({
  // 环境变量 VITE_API_BASE_URL 可配置后端地址
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',

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
  (config) => {
    const token = localStorage.getItem('adminToken')
    if (token) {
      config.headers.set('Authorization', `Bearer ${token}`)
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

/**
 * 响应拦截器
 *
 * 在请求响应后统一处理：
 * 1. 提取响应数据（response.data）
 * 2. 错误处理：静默处理 401（未授权），打印其他错误
 */
api.interceptors.response.use(
  // 成功响应：直接返回 data 部分
  (response) => response.data,

  // 错误响应
  (error) => {
    // 401 未授权是预期情况，不打印错误
    if (error.response?.status === 401) {
      return Promise.reject(error)
    }
    console.error('API Error:', error)
    return Promise.reject(error)
  },
)

// ========== 类型定义 ==========

/**
 * 博客文章接口类型
 * 定义前后端交互的数据结构
 */
export interface BlogPost {
  id: number // 文章唯一标识
  title: string // 文章标题
  excerpt: string // 文章摘要
  content: string // 文章内容（Markdown 格式）
  date: string // 发布日期
  tags: string[] // 标签数组
  created_at: string // 创建时间
  updated_at: string // 更新时间
  view_count: number // 阅读量
}

/**
 * 创建文章请求类型
 */
export interface BlogPostCreate {
  title: string
  excerpt: string
  content: string
  tags: string[]
}

/**
 * 更新文章请求类型
 */
export interface BlogPostUpdate {
  title?: string
  excerpt?: string
  content?: string
  tags?: string[]
}

/**
 * 标题检查请求类型
 */
export interface TitleCheckRequest {
  title: string
  excludeId?: number
}

/**
 * 标题检查响应类型
 */
export interface TitleCheckResponse {
  exists: boolean
  message: string
}

/**
 * 匿名评论类型
 */
export interface Comment {
  id: number
  post_id: number
  nickname: string // 匿名评论者昵称
  content: string
  parent_id: number | null
  created_at: string
  updated_at: string
  replies?: Comment[]
}

/**
 * 创建评论请求类型（匿名）
 */
export interface CommentCreate {
  post_id: number
  nickname: string
  content: string
  parent_id?: number
}

/**
 * 归档分组接口
 */
export interface ArchiveGroup {
  year: number
  month: number
  month_name: string
  post_count: number
  posts: BlogPost[]
}

/**
 * 年度归档接口
 */
export interface ArchiveYear {
  year: number
  post_count: number
  months: ArchiveGroup[]
}

// ========== 博客 API ==========

export const blogApi = {
  /**
   * 获取所有文章列表
   * @param skip 跳过的记录数，默认 0
   * @param limit 返回的最大记录数，默认 100
   * @returns Promise<BlogPost[]> 文章数组
   */
  getPosts: async (skip: number = 0, limit: number = 100): Promise<BlogPost[]> => {
    return api.get('/api/posts', { params: { skip, limit } })
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
}

// ========== 评论 API ==========

export const commentApi = {
  /**
   * 获取文章的评论列表
   * @param postId 文章 ID
   * @returns Promise<Comment[]> 评论列表
   */
  getComments: async (postId: number): Promise<Comment[]> => {
    return api.get(`/api/posts/${postId}/comments`)
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

/**
 * 阅读量响应类型
 */
export interface ViewCountResponse {
  counted: boolean // 是否成功计数
  view_count: number // 当前阅读量
}

/**
 * 管理员登录请求类型
 */
export interface AdminLoginRequest {
  password: string
}

/**
 * 管理员登录响应类型
 */
export interface AdminLoginResponse {
  success: boolean
  message: string
  token: string | null
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
}

// 导出 Axios 实例（可自定义配置时使用）
export default api
