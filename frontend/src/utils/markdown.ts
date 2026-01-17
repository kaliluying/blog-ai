/**
 * Markdown 工具模块
 *
 * 提供 Markdown 到 HTML 的转换功能：
 * - renderMarkdown: 基础 Markdown 渲染（无代码块特殊处理）
 * - renderMarkdownWithCode: Markdown 渲染，支持代码块 base64 编码（用于复制功能）
 */

import DOMPurify from 'dompurify'

/**
 * 允许的链接协议白名单
 */
const ALLOWED_PROTOCOLS = ['http:', 'https:']

/**
 * 链接安全处理函数
 */
const processLink = (_: string, text: string, url: string): string => {
  // 移除危险协议
  const normalizedUrl = url.replace(/^\s*(javascript|data|vbscript|file|ftp):/gi, '')
  // 编码 URL 参数部分
  const safeUrl = encodeURI(normalizedUrl)
  // 仅允许 http/https 链接，或没有协议的相对链接
  const isSafeProtocol = ALLOWED_PROTOCOLS.some(p => normalizedUrl.startsWith(p)) ||
                         !normalizedUrl.includes(':')
  const href = isSafeProtocol ? safeUrl : '#'
  return `<a href="${href}" target="_blank" rel="noopener noreferrer">${text}</a>`
}

/**
 * 通用 Markdown 转换配置
 * 包含除代码块外的所有转换规则
 */
const COMMON_TRANSFORMATIONS: Array<[RegExp, string]> = [
  // 行内代码
  [/`([^`]+)`/g, '<code>$1</code>'],
  // 粗体
  [/\*\*([^*]+)\*\*/g, '<strong>$1</strong>'],
  // 斜体
  [/\*([^*]+)\*/g, '<em>$1</em>'],
  // 删除线
  [/~~([^~]+)~~/g, '<del>$1</del>'],
  // 引用
  [/^> (.+)$/gm, '<blockquote>$1</blockquote>'],
  // 标题
  [/^### (.+)$/gm, '<h3>$1</h3>'],
  [/^## (.+)$/gm, '<h2>$1</h2>'],
  [/^# (.+)$/gm, '<h1>$1</h1>'],
  // 无序列表
  [/^- (.+)$/gm, '<li>$1</li>'],
  // 有序列表
  [/^\d+\. (.+)$/gm, '<li>$1</li>'],
  // 段落
  [/\n\n/g, '</p><p>'],
  // 换行
  [/\n/g, '<br>']
]

/**
 * 应用通用转换规则
 */
const applyCommonTransformations = (text: string, codeBlockHandler?: (match: string, lang: string, code: string) => string): string => {
  let result = text

  // 处理代码块（如果提供了处理器）
  if (codeBlockHandler) {
    result = result.replace(/```(\w*)\n([\s\S]*?)```/g, codeBlockHandler)
  } else {
    // 默认代码块处理
    result = result.replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
  }

  // 应用通用转换
  for (const [pattern, replacement] of COMMON_TRANSFORMATIONS) {
    result = result.replace(pattern, replacement)
  }

  // 链接单独处理
  result = result.replace(/\[([^\]]+)\]\(([^)]+)\)/g, processLink)

  return result
}

/**
 * 代码块处理器 - 带 base64 编码
 */
const codeBlockWithEncoding = (_: string, lang: string, code: string): string => {
  const encodedCode = btoa(unescape(encodeURIComponent(code)))
  return `<pre class="code-block" data-code="${encodedCode}"><code>${code}</code></pre>`
}

/**
 * 基础 Markdown 渲染函数
 * 将 Markdown 格式的文本转换为 HTML（不含代码块特殊处理）
 *
 * @param text Markdown 原文
 * @returns 渲染后的 HTML 字符串
 */
export const renderMarkdown = (text: string): string => {
  if (!text) return ''
  return `<p>${applyCommonTransformations(text)}</p>`
}

/**
 * 带代码块处理的 Markdown 渲染函数
 * 将 Markdown 转换为 HTML，代码块会添加 base64 编码以便复制功能使用
 *
 * @param text Markdown 原文
 * @returns 渲染后的 HTML 字符串，代码块带有 data-code 属性
 */
export const renderMarkdownWithCode = (text: string): string => {
  if (!text) return ''
  return `<p>${applyCommonTransformations(text, codeBlockWithEncoding)}</p>`
}

/**
 * 安全渲染 Markdown
 * 将 Markdown 转换为 HTML 并进行 XSS 防护
 *
 * @param text Markdown 原文
 * @returns 安全的 HTML 字符串（已消毒）
 */
export const renderMarkdownSafe = (text: string): string => {
  const html = renderMarkdown(text)
  return DOMPurify.sanitize(html, {
    ALLOWED_TAGS: [
      'p', 'br', 'strong', 'em', 'del', 'code', 'pre',
      'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
      'ul', 'ol', 'li', 'blockquote',
      'a'
    ],
    ALLOWED_ATTR: ['href', 'target', 'class', 'rel']
  })
}

/**
 * 安全渲染 Markdown（带代码块处理）
 *
 * @param text Markdown 原文
 * @returns 安全的 HTML 字符串（已消毒），代码块带有 data-code 属性
 */
export const renderMarkdownWithCodeSafe = (text: string): string => {
  const html = renderMarkdownWithCode(text)
  return DOMPurify.sanitize(html, {
    ALLOWED_TAGS: [
      'p', 'br', 'strong', 'em', 'del', 'code', 'pre',
      'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
      'ul', 'ol', 'li', 'blockquote',
      'a'
    ],
    ALLOWED_ATTR: ['href', 'target', 'class', 'rel', 'data-code']
  })
}

/**
 * 解码 base64 编码的代码块内容
 *
 * @param encodedCode base64 编码的代码
 * @returns 解码后的原始代码
 */
export const decodeCode = (encodedCode: string): string => {
  try {
    return decodeURIComponent(escape(atob(encodedCode)))
  } catch {
    return ''
  }
}
