/**
 * 日期格式化工具
 */

/**
 * 格式化日期（完整格式）
 * @param date ISO 日期字符串
 * @returns 格式化的中文日期字符串
 */
export const formatDate = (date: string): string => {
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

/**
 * 格式化日期（简短格式）
 * @param date ISO 日期字符串
 * @returns 简短的中文日期字符串
 */
export const formatShortDate = (date: string): string => {
  return new Date(date).toLocaleDateString('zh-CN', {
    month: 'short',
    day: 'numeric'
  })
}
