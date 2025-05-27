<!-- /src/views/articles/ArticleDetailView.vue -->

<template>
  <div class="max-w-3xl mx-auto pt-40">
    <h1 class="text-2xl font-bold mb-4">{{ article.title }}</h1>
    <p class="text-sm text-gray-500 mb-4">
      작성자: {{ article.user?.userName || '알 수 없음' }} | 작성일:
      {{ formatDate(article.created_at) }} | 조회수: {{ article.views }}
    </p>

    <div class="prose whitespace-pre-line mb-6" v-html="article.content"></div>

    <div v-if="article.is_author" class="flex justify-end gap-2 mb-6">
      <button
        @click="isEditOpen = true"
        class="text-sm px-3 py-1 border rounded hover:bg-gray-100 cursor-pointer"
      >
        수정
      </button>
      <button
        @click="deleteArticle"
        class="text-sm px-3 py-1 border rounded text-red-500 hover:bg-red-50 cursor-pointer"
      >
        삭제
      </button>
    </div>

    <CommentSection
      v-if="article.id"
      :article-id="article.id"
      @comment-added="fetchArticle"
      @comment-deleted="fetchArticle"
    />

    <ArticleEditModal
      v-if="isEditOpen"
      :article-id="article.id"
      :initial-title="article.title"
      :initial-content="article.content"
      @close="isEditOpen = false"
      @updated="handleArticleUpdated"
    />
  </div>

  <ToastMessage v-if="toast.visible" :type="toast.type" :message="toast.message" />

  <ConfirmModal
    :show="showModal"
    title="게시물 삭제 확인"
    content="정말로 게시물을 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다."
    confirmText="삭제하기"
    cancelText="취소"
    @confirm="confirmDeleteArticle"
    @cancel="showModal = false"
  />
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/axios'
import { useAuthStore } from '@/stores/auth'
import CommentSection from '@/components/articles/CommentSection.vue'
import ArticleEditModal from '@/components/articles/ArticleEditModal.vue'
import ToastMessage from '@/components/ToastMessage.vue'
import ConfirmModal from '@/components/ConfirmModal.vue'

const showModal = ref(false)
const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const article = ref({
  id: null,
  title: '',
  content: '',
  views: 0,
  user: null,
  is_author: false,
  created_at: ''
})

const isEditOpen = ref(false)
let timer = null
let hasViewed = false

const toast = ref({ visible: false, type: 'success', message: '' })

const showToast = (type, message) => {
  toast.value = { visible: true, type, message }
  setTimeout(() => (toast.value.visible = false), 3000)
}

const fetchArticle = async () => {
  try {
    const { data } = await api.get(`/articles/${route.params.id}/`, {
      headers: { Authorization: `Bearer ${authStore.accessToken}` }
    })
    article.value = data
  } catch (error) {
    console.error('게시글 로드 실패:', error)
  }
}

const delayedViewCount = async () => {
  timer = setTimeout(async () => {
    if (!hasViewed) {
      try {
        await api.post(
          `/articles/${route.params.id}/increment-views/`,
          {},
          {
            headers: { Authorization: `Bearer ${authStore.accessToken}` }
          }
        )
        hasViewed = true
        article.value.views += 1
      } catch (error) {
        console.error('조회수 증가 실패:', error)
      }
    }
  }, 3000)
}
const deleteArticle = () => {
  showModal.value = true
}

const confirmDeleteArticle = async () => {
  try {
    await api.delete(`/articles/${route.params.id}/`, {
      headers: { Authorization: `Bearer ${authStore.accessToken}` }
    })
    showToast('success', '삭제 완료')

    setTimeout(() => {
      router.push('/articles')
    }, 1000)
  } catch (error) {
    showToast('danger', '삭제 실패')
  } finally {
    showModal.value = false
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
