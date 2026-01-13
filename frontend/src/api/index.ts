/**
 * API 模块 - 后端接口封装
 *
 * 本模块使用 Axios 封装了与后端 FastAPI 服务器的所有 HTTP 请求。
 * 包含：
 * 1. Axios 实例配置（基础 URL、超时、拦截器）
 * 2. BlogPost 接口类型定义
 * 3. 博客文章相关的 API 方法
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
 * 响应拦截器
 *
 * 在请求响应后统一处理：
 * 1. 提取响应数据（response.data）
 * 2. 错误处理：打印错误信息并拒绝 Promise
 */
api.interceptors.response.use(
  // 成功响应：直接返回 data 部分
  (response) => response.data,

  // 错误响应：记录错误并抛出
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

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
 * 博客 API 方法集合
 * 封装所有与文章相关的后端接口调用
 */
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
  }
}

// 导出 Axios 实例（可自定义配置时使用）
export default api
