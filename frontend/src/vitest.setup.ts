/**
 * Vitest 测试设置文件
 *
 * 在每个测试文件运行前执行全局配置
 */

// 导入 vi 用于设置测试环境
import { beforeEach, vi } from 'vitest'
import { config } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'

// 设置全局 Date.now() 为固定值，确保时间相关测试的一致性
const now = new Date('2026-01-15T12:00:00.000Z')
vi.setSystemTime(now)

// 模拟 window.matchMedia (某些组件库需要)
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
})

// 模拟 ResizeObserver
global.ResizeObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}))

beforeEach(() => {
  setActivePinia(createPinia())
})

config.global.stubs = {
  'n-spin': true,
  'n-tag': true,
  'n-button': true,
  'n-pagination': true,
}
