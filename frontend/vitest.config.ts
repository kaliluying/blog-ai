/**
 * Vitest 测试配置
 *
 * 配置 Vitest 测试运行器，包括：
 * - 测试环境 (jsdom)
 * - 全局 API (vi, describe, it, expect)
 * - 覆盖率配置
 * - 路径别名
 */

import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  test: {
    // 测试环境
    environment: 'jsdom',
    
    // 全局 API
    globals: true,
    
    // 包含的测试文件
    include: ['src/**/__tests__/*.{test,spec}.{js,ts}'],
    
    // 排除的文件
    exclude: ['node_modules', '.git', '.venv'],
    
    // 覆盖率配置
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      include: ['src/**/*.{js,ts,vue}'],
      exclude: [
        'src/**/*.d.ts',
        'src/**/*.test.ts',
        'src/**/*.spec.ts',
        'src/**/__tests__/**',
        'src/main.ts',
        'src/App.vue',
        'src/env.d.ts',
      ],
    },
    
    // 设置文件
    setupFiles: ['src/vitest.setup.ts'],
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
})
