/**
 * 代码复制 Composable
 *
 * 提供代码块复制功能封装，支持：
 * - 一键复制代码到剪贴板
 * - 复制成功/失败状态反馈
 * - 自动恢复复制图标
 */

import { useMessage } from 'naive-ui'

/**
 * SVG 图标：复制
 */
const COPY_ICON = `<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>`

/**
 * SVG 图标：已复制（勾号）
 */
const COPIED_ICON = `<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg>`

/**
 * 解码 base64 编码的代码
 *
 * @param encoded 编码后的字符串
 * @returns 解码后的原始代码
 */
const decodeCode = (encoded: string): string => {
  try {
    return atob(encoded)
  } catch {
    return encoded
  }
}

/**
 * 代码复制 Composable
 *
 * @returns 代码复制相关方法和状态
 */
export function useCodeCopy() {
  // 消息提示实例
  const message = useMessage()

  /**
   * 为单个代码块添加复制按钮
   *
   * @param pre 代码块 DOM 元素
   * @param code 要复制的内容
   */
  const attachCopyButton = (pre: Element, code: string) => {
    // 移除已存在的复制按钮
    const existingBtn = pre.querySelector('.copy-btn')
    if (existingBtn) {
      existingBtn.remove()
    }

    // 创建复制按钮
    const btn = document.createElement('button')
    btn.className = 'copy-btn'
    btn.innerHTML = COPY_ICON
    btn.title = '复制代码'

    // 点击复制事件
    btn.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(code)
        btn.classList.add('copied')
        btn.innerHTML = COPIED_ICON
        message.success('已复制')
        // 2 秒后恢复原图标
        setTimeout(() => {
          btn.classList.remove('copied')
          btn.innerHTML = COPY_ICON
        }, 2000)
      } catch {
        message.error('复制失败')
      }
    })

    pre.appendChild(btn)
  }

  /**
   * 为容器内所有代码块添加复制按钮
   *
   * @param container 容器 DOM 元素
   */
  const setupCopyButtons = (container: HTMLElement) => {
    const preList = container.querySelectorAll('pre.code-block')
    preList.forEach((pre) => {
      // 从 data 属性中获取 base64 编码的代码
      const encodedCode = (pre as HTMLElement).dataset.code || ''
      // 解码 base64
      const code = decodeCode(encodedCode)
      attachCopyButton(pre, code)
    })
  }

  /**
   * 清理容器内所有复制按钮
   *
   * @param container 容器 DOM 元素
   */
  const cleanupCopyButtons = (container: HTMLElement) => {
    const btnList = container.querySelectorAll('pre .copy-btn')
    btnList.forEach((btn) => btn.remove())
  }

  return {
    attachCopyButton,
    setupCopyButtons,
    cleanupCopyButtons,
  }
}
