<template>
  <div class="max-w-6xl mx-auto p-4 pt-20">
    <h1 class="text-2xl font-bold mb-4">자유 게시판</h1>

    <!-- 글 생성 버튼 -->
    <div class="flex justify-end mb-4">
      <button
        @click="handleCreateClick"
        class="px-4 py-2 bg-purple-500 text-white rounded hover:bg-pink-400"
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
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import ArticleList from '@/components/articles/ArticleList.vue'
import ArticleFormModal from '@/components/articles/ArticleFormModal.vue'

const router = useRouter()
const authStore = useAuthStore()
const isModalOpen = ref(false)
const listRef = ref(null)

const handleCreateClick = () => {
  if (!authStore.isAuthenticated) {
    // toast로 교체
    // toast.value.showToast('로그인이 필요한 기능입니다.')
    alert('로그인이 필요한 기능입니다.')
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
