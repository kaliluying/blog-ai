/**
 * 博客系统类型定义
 *
 * 本模块定义前后端交互的数据结构类型，
 * 保持 API 相关类型集中管理，便于维护。
 */

// ========== 文章相关类型 ==========

/**
 * 博客文章接口类型
 * 定义前后端交互的数据结构
 */
export interface BlogPost {
  id: number                    // 文章唯一标识
  title: string                 // 文章标题
  excerpt: string               // 文章摘要
  content: string               // 文章内容（Markdown 格式）
  date: string                  // 发布日期
  tags: string[]                // 标签数组
  created_at: string            // 创建时间
  updated_at: string            // 更新时间
  view_count: number            // 阅读量
  is_scheduled?: boolean        // 是否定时发布（未来时间）
}

/**
 * 创建文章请求类型
 */
export interface BlogPostCreate {
  title: string
  excerpt: string
  content: string
  tags: string[]
  publish_date?: string  // 定时发布时间（可选）
}

/**
 * 更新文章请求类型
 */
export interface BlogPostUpdate {
  title?: string
  excerpt?: string
  content?: string
  tags?: string[]
  publish_date?: string  // 定时发布时间（可选）
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
 * 文章列表项类型（简化版）
 */
export interface BlogPostListItem {
  id: number
  title: string
  excerpt: string
  date: string
  tags: string[]
  view_count: number
}

// ========== 评论相关类型 ==========

/**
 * 匿名评论类型
 */
export interface Comment {
  id: number
  post_id: number
  nickname: string              // 匿名评论者昵称
  content: string
  parent_id: number | null
  created_at: string
  updated_at: string
  replies?: Comment[]           // 嵌套回复
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

// ========== 归档相关类型 ==========

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

// ========== 阅读量相关类型 ==========

/**
 * 阅读量响应类型
 */
export interface ViewCountResponse {
  counted: boolean              // 是否成功计数
  view_count: number            // 当前阅读量
}

// ========== 管理员认证相关类型 ==========

/**
 * 管理员登录响应类型
 */
export interface AdminLoginResponse {
  success: boolean
  message: string
  token: string | null
}
