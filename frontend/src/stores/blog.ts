import { defineStore } from 'pinia'
import { ref } from 'vue'
import { blogApi, type BlogPost } from '@/api'

export const useBlogStore = defineStore('blog', () => {
  const posts = ref<BlogPost[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchPosts = async () => {
    loading.value = true
    error.value = null
    try {
      posts.value = await blogApi.getPosts()
    } catch (e) {
      error.value = '获取文章列表失败'
      console.error(e)
    } finally {
      loading.value = false
    }
  }

  const getPostById = (id: number) => {
    return posts.value.find(post => post.id === id)
  }

  const fetchPostById = async (id: number): Promise<BlogPost | null> => {
    loading.value = true
    error.value = null
    try {
      const post = await blogApi.getPost(id)
      // 如果文章不在列表中，添加到列表
      if (!posts.value.find(p => p.id === id)) {
        posts.value.push(post)
      }
      return post
    } catch (e) {
      error.value = '获取文章失败'
      console.error(e)
      return null
    } finally {
      loading.value = false
    }
  }

  return { posts, loading, error, fetchPosts, getPostById, fetchPostById }
})
