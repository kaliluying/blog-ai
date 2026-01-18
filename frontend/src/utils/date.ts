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

/**
 * 相对时间格式化（如：3分钟前、2小时前、3天前）
 * @param date ISO 日期字符串
 * @returns 相对时间字符串
 */
export const formatTimeAgo = (date: string | null | undefined): string => {
  if (!date) return '未知时间'
  const now = new Date()
  const past = new Date(date)
  const diffMs = now.getTime() - past.getTime()
  const diffSec = Math.floor(diffMs / 1000)
  const diffMin = Math.floor(diffSec / 60)
  const diffHour = Math.floor(diffMin / 60)
  const diffDay = Math.floor(diffHour / 24)
  const diffWeek = Math.floor(diffDay / 7)
  const diffMonth = Math.floor(diffDay / 30)
  const diffYear = Math.floor(diffDay / 365)

  if (diffSec < 60) {
    return '刚刚'
  } else if (diffMin < 60) {
    return `${diffMin}分钟前`
  } else if (diffHour < 24) {
    return `${diffHour}小时前`
  } else if (diffDay < 7) {
    return `${diffDay}天前`
  } else if (diffDay < 30) {
    // 7-29天显示为周（避免28天显示为4周而不是1个月）
    return `${diffWeek}周前`
  } else if (diffMonth < 12) {
    return `${diffMonth}个月前`
  } else {
    return `${diffYear}年前`
  }
}
