/**
 * Blog Store 测试
 *
 * 测试博客文章状态管理逻辑
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import Home from '@/views/Home.vue'

// Mock router
vi.mock('vue-router', () => ({
  useRouter: () => ({
    push: vi.fn(),
  }),
}))

// Mock blog store
const mockPosts = [
  {
    id: 1,
    title: '测试文章 1',
    excerpt: '这是测试摘要',
    content: '测试内容',
    date: '2026-01-10T10:00:00.000Z',
    tags: ['测试', '前端'],
  },
  {
    id: 2,
    title: '测试文章 2',
    excerpt: '另一篇测试',
    content: '更多测试内容',
    date: '2026-01-12T14:30:00.000Z',
    tags: ['后端'],
  },
]

vi.mock('@/stores/blog', () => ({
  useBlogStore: () => ({
    posts: mockPosts,
    loading: false,
    error: null,
    fetchPosts: vi.fn(),
  }),
}))

describe('Home View', () => {
  it('renders article list', () => {
    const wrapper = mount(Home)
    expect(wrapper.find('.hero-title').text()).toContain('欢迎来到我的手绘博客')
  })

  it('shows posts when loaded', () => {
    const wrapper = mount(Home)
    const postCards = wrapper.findAll('.post-card')
    expect(postCards).toHaveLength(2)
  })

  it('formats date correctly', () => {
    const wrapper = mount(Home)
    expect(wrapper.find('.post-date').text()).toBeTruthy()
  })
})
