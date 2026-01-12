import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 响应拦截器
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export interface BlogPost {
  id: number
  title: string
  excerpt: string
  content: string
  date: string
  tags: string[]
  created_at?: string
  updated_at?: string
}

export const blogApi = {
  // 获取所有文章
  getPosts: async (): Promise<BlogPost[]> => {
    return api.get('/api/posts')
  },

  // 获取单篇文章
  getPost: async (id: number): Promise<BlogPost> => {
    return api.get(`/api/posts/${id}`)
  },

  // 创建文章
  createPost: async (post: Omit<BlogPost, 'id' | 'date'>): Promise<BlogPost> => {
    return api.post('/api/posts', post)
  },

  // 更新文章
  updatePost: async (id: number, post: Partial<BlogPost>): Promise<BlogPost> => {
    return api.put(`/api/posts/${id}`, post)
  },

  // 删除文章
  deletePost: async (id: number): Promise<void> => {
    return api.delete(`/api/posts/${id}`)
  }
}

export default api
