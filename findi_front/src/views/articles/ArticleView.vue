<!-- src/views/articles/ArticleView.vue -->
<template>
  <div class="max-w-6xl mx-auto p-4 pt-20">
    <!-- 글 생성 버튼 -->
    <div class="flex justify-end mb-4">
      <button
        @click="handleCreateClick"
        class="px-4 py-2 bg-[#8A69E1] text-white rounded hover:bg-purple-500 cursor-pointer"
      >
        글 생성
      </button>
    </div>

    <!-- 게시글 목록 -->
    <ArticleList ref="listRef" />

    <!-- 게시글 생성 모달 -->
    <ArticleFormModal
      v-if="isModalOpen"
      @close="isModalOpen = false"
      @created="handleArticleCreated"
    />
  </div>

  <ToastMessage v-if="toast.visible" :type="toast.type" :message="toast.message" />
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import ArticleList from '@/components/articles/ArticleList.vue'
import ArticleFormModal from '@/components/articles/ArticleFormModal.vue'
import ToastMessage from '@/components/ToastMessage.vue'

const router = useRouter()
const authStore = useAuthStore()
const isModalOpen = ref(false)
const listRef = ref(null)

const toast = ref({ visible: false, type: 'success', message: '' })

const showToast = (type, message) => {
  toast.value = { visible: true, type, message }
  setTimeout(() => (toast.value.visible = false), 3000)
}

const handleCreateClick = () => {
  if (!authStore.isAuthenticated) {
    showToast('danger', '로그인이 필요한 기능입니다.')
    return
  }
  isModalOpen.value = true
}

const handleArticleCreated = () => {
  isModalOpen.value = false
  listRef.value?.fetchArticles()
}
</script>

<style scoped></style>
