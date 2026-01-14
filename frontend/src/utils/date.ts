/**
 * 日期格式化工具
 */

/**
 * 中文月份名称映射
 */
export const MONTH_NAMES: Record<number, string> = {
  1: '一月', 2: '二月', 3: '三月', 4: '四月',
  5: '五月', 6: '六月', 7: '七月', 8: '八月',
  9: '九月', 10: '十月', 11: '十一月', 12: '十二月'
}

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
