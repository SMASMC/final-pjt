<!-- /src/views/articles/ArticleDetailView.vue -->
<template>
  <div class="max-w-3xl mx-auto pt-20">
    <h1 class="text-2xl font-bold mb-4">{{ article.title }}</h1>

    <p class="text-sm text-gray-500 mb-4">
      작성자: {{ article.user?.userName || '알 수 없음' }} |
      작성일: {{ formatDate(article.created_at) }} |
      조회수: {{ article.views }}
    </p>

    <div class="prose whitespace-pre-line mb-6" v-html="article.content"></div>

    <div v-if="article.is_author" class="flex gap-2 mb-6">
      <button @click="isEditOpen = true" class="px-4 py-2 border rounded">수정</button>
      <button @click="deleteArticle" class="px-4 py-2 border rounded text-red-500">삭제</button>
    </div>

    <CommentSection
      :comments="article.comments"
      :article-id="article.id"
      @comment-added="fetchArticle"
      @comment-deleted="fetchArticle"
    />

    <ArticleEditModal
      v-if="isEditOpen"
      :article="article"
      @close="isEditOpen = false"
      @updated="handleArticleUpdated"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/axios'
import CommentSection from '@/components/articles/CommentSection.vue'
import ArticleEditModal from '@/components/articles/ArticleEditModal.vue'

const route = useRoute()
const router = useRouter()

const article = ref({
  id: null,
  title: '',
  content: '',
  views: 0,
  user: null,
  is_author: false,
  created_at: '',
  comments: []
})

const isEditOpen = ref(false)
let timer = null
let hasViewed = false

const fetchArticle = async () => {
  try {
    const { data } = await api.get(`/articles/${route.params.id}/`)
    article.value = data
  } catch (error) {
    console.error('게시글 로드 실패:', error)
  }
}

const delayedViewCount = async () => {
  timer = setTimeout(async () => {
    if (!hasViewed) {
      try {
        await api.post(`/articles/${route.params.id}/increment-views/`)
        hasViewed = true
        article.value.views += 1
      } catch (error) {
        console.error('조회수 증가 실패:', error)
      }
    }
  }, 3000)
}

const deleteArticle = async () => {
  if (!confirm('정말 삭제하시겠습니까?')) return
  try {
    await api.delete(`/articles/${route.params.id}/`)
    alert('삭제 완료')
    router.push('/articles')
  } catch (error) {
    alert('삭제 실패')
  }
}

const handleArticleUpdated = () => {
  isEditOpen.value = false
  fetchArticle()
}

const formatDate = (iso) => {
  if (!iso) return ''
  const date = new Date(iso)
  return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`
}

onMounted(() => {
  fetchArticle()
  delayedViewCount()
})

onBeforeUnmount(() => {
  clearTimeout(timer)
})
</script>
