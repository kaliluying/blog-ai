/**
 * API 模块 - 后端接口封装
 *
 * 本模块使用 Axios 封装了与后端 FastAPI 服务器的所有 HTTP 请求。
 * 包含：
 * 1. Axios 实例配置（基础 URL、超时、拦截器、认证）
 * 2. BlogPost 接口类型定义
 * 3. 博客文章相关的 API 方法
 * 4. 用户认证 API 方法
 * 5. 评论 API 方法
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
    'Content-Type': 'application/json'
  }
})

/**
 * 请求拦截器 - 自动添加 Token
 */
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.set('Authorization', `Bearer ${token}`)
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
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
  }
)

// ========== 类型定义 ==========

/**
 * 博客文章接口类型
 * 定义前后端交互的数据结构
 */
export interface BlogPost {
  id: number              // 文章唯一标识
  title: string           // 文章标题
  excerpt: string         // 文章摘要
  content: string         // 文章内容（Markdown 格式）
  date: string            // 发布日期
  tags: string[]          // 标签数组
  created_at?: string    // 创建时间（可选）
  updated_at?: string    // 更新时间（可选）
}

/**
 * 用户类型
 */
export interface User {
  id: number
  username: string
  email: string
  is_active: boolean
  is_admin: boolean
  created_at: string
}

/**
 * Token 响应类型
 */
export interface TokenResponse {
  access_token: string
  token_type: string
  user: User
}

/**
 * 评论类型
 */
export interface Comment {
  id: number
  post_id: number
  user_id: number
  username: string
  content: string
  parent_id: number | null
  created_at: string
  updated_at: string
  replies?: Comment[]
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
   * @returns Promise<BlogPost[]> 文章数组
   */
  getPosts: async (): Promise<BlogPost[]> => {
    return api.get('/api/posts')
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
   * 创建新文章
   * @param post 文章数据（不含 id 和 date，由后端生成）
   * @returns Promise<BlogPost> 创建后的文章（含 id）
   */
  createPost: async (post: Omit<BlogPost, 'id' | 'date'>): Promise<BlogPost> => {
    return api.post('/api/posts', post)
  },

  /**
   * 更新文章
   * @param id 文章 ID
   * @param post 要更新的字段（部分更新）
   * @returns Promise<BlogPost> 更新后的文章
   */
  updatePost: async (id: number, post: Partial<BlogPost>): Promise<BlogPost> => {
    return api.put(`/api/posts/${id}`, post)
  },

  /**
   * 删除文章
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
  }
}

// ========== 认证 API ==========

export const authApi = {
  /**
   * 用户注册
   * @param username 用户名
   * @param email 邮箱
   * @param password 密码
   * @returns Promise<TokenResponse> Token 和用户信息
   */
  register: async (username: string, email: string, password: string): Promise<TokenResponse> => {
    return api.post('/api/auth/register', { username, email, password })
  },

  /**
   * 用户登录
   * @param username 用户名
   * @param password 密码
   * @returns Promise<TokenResponse> Token 和用户信息
   */
  login: async (username: string, password: string): Promise<TokenResponse> => {
    // OAuth2 需要 form-data 格式
    const formData = new URLSearchParams()
    formData.append('username', username)
    formData.append('password', password)
    return api.post('/api/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
  },

  /**
    * 获取当前用户信息
    * @returns Promise<User> 当前用户信息
    */
  getMe: async (): Promise<User> => {
    return api.get('/api/auth/me')
  }
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
   * 创建评论
   * @param postId 文章 ID
   * @param content 评论内容
   * @param parentId 父评论 ID（可选，用于回复）
   * @returns Promise<Comment> 创建的评论
   */
  createComment: async (postId: number, content: string, parentId?: number): Promise<Comment> => {
    return api.post('/api/comments', { post_id: postId, content, parent_id: parentId })
  },

  /**
    * 删除评论
    * @param commentId 评论 ID
    * @returns Promise<void>
    */
   deleteComment: async (commentId: number): Promise<void> => {
     return api.delete(`/api/comments/${commentId}`)
   }
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
   }
 }

// 导出 Axios 实例（可自定义配置时使用）
export default api
