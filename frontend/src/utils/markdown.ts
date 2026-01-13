/**
 * Markdown 工具模块
 *
 * 提供 Markdown 到 HTML 的转换功能：
 * - renderMarkdown: 基础 Markdown 渲染（无代码块特殊处理）
 * - renderMarkdownWithCode: Markdown 渲染，支持代码块 base64 编码（用于复制功能）
 */

import DOMPurify from 'dompurify'

/**
 * 基础 Markdown 渲染函数
 * 将 Markdown 格式的文本转换为 HTML（不含代码块特殊处理）
 *
 * 支持的语法：
 * - 代码块（```code```）
 * - 行内代码（`code`）
 * - 粗体（**text**）
 * - 斜体（*text*）
 * - 删除线（~~text~~）
 * - 链接（[text](url)）
 * - 引用（> text）
 * - 标题（# ## ###）
 * - 列表（- 1.）
 *
 * @param text Markdown 原文
 * @returns 渲染后的 HTML 字符串
 */
export const renderMarkdown = (text: string): string => {
  if (!text) return ''

  let html = text
    // 代码块
    .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
    // 行内代码
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    // 粗体
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    // 斜体
    .replace(/\*([^*]+)\*/g, '<em>$1</em>')
    // 删除线
    .replace(/~~([^~]+)~~/g, '<del>$1</del>')
    // 链接：验证 URL 是否安全，只允许 http/https 协议
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_, text, url) => {
      // 移除危险协议
      const normalizedUrl = url.replace(/^\s*(javascript|data|vbscript):/gi, '')
      // 编码 URL 参数部分
      const safeUrl = encodeURI(normalizedUrl)
      // 仅允许 http/https 链接
      const isSafeProtocol = /^https?:\/\//i.test(safeUrl) || !/^[a-z]+:/i.test(normalizedUrl)
      const href = isSafeProtocol ? safeUrl : '#'
      return `<a href="${href}" target="_blank" rel="noopener noreferrer">${text}</a>`
    })
    // 引用
    .replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>')
    // 标题
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    // 无序列表
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    // 有序列表
    .replace(/^\d+\. (.+)$/gm, '<li>$1</li>')
    // 段落
    .replace(/\n\n/g, '</p><p>')
    // 换行
    .replace(/\n/g, '<br>')

  return `<p>${html}</p>`
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

  let html = text
    // 代码块（添加特殊标记以便识别）
    // 格式：```语言名 代码内容 ```
    .replace(/```(\w*)\n([\s\S]*?)```/g, (_, lang, code) => {
      // 使用 btoa/atob 进行 base64 编码，以便在 data 属性中存储
      const encodedCode = btoa(unescape(encodeURIComponent(code)))
      return `<pre class="code-block" data-code="${encodedCode}"><code>${code}</code></pre>`
    })
    // 行内代码
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    // 粗体
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    // 斜体
    .replace(/\*([^*]+)\*/g, '<em>$1</em>')
    // 删除线
    .replace(/~~([^~]+)~~/g, '<del>$1</del>')
    // 链接：验证 URL 是否安全，只允许 http/https 协议
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_, text, url) => {
      // 移除危险协议
      const normalizedUrl = url.replace(/^\s*(javascript|data|vbscript):/gi, '')
      // 编码 URL 参数部分
      const safeUrl = encodeURI(normalizedUrl)
      // 仅允许 http/https 链接
      const isSafeProtocol = /^https?:\/\//i.test(safeUrl) || !/^[a-z]+:/i.test(normalizedUrl)
      const href = isSafeProtocol ? safeUrl : '#'
      return `<a href="${href}" target="_blank" rel="noopener noreferrer">${text}</a>`
    })
    // 引用
    .replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>')
    // 标题
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    // 无序列表
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    // 有序列表
    .replace(/^\d+\. (.+)$/gm, '<li>$1</li>')
    // 段落
    .replace(/\n\n/g, '</p><p>')
    // 换行
    .replace(/\n/g, '<br>')

  return `<p>${html}</p>`
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
