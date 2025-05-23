<template>
  <div class="pt-20 max-w-3xl mx-auto">
    <h1 class="text-2xl font-bold mb-4">자유 게시판</h1>

    <div class="flex justify-end mb-4">
      <button
        @click="handleCreateClick"
        class="px-4 py-2 bg-purple-500 text-white rounded hover:bg-pink-400"
      >
        글 생성
      </button>
    </div>

    <!-- 게시글 리스트 ref 등록 -->
    <ArticleList ref="listRef" />

    <!-- 게시글 생성 모달 -->
    <ArticleFormModal
      v-if="isModalOpen"
      @close="isModalOpen = false"
      @created="handleArticleCreated"
    />

    <!-- <BaseToast ref="toast" /> -->
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import ArticleFormModal from '@/components/articles/ArticleFormModal.vue'
import ArticleList from '@/components/articles/ArticleList.vue'

const authStore = useAuthStore()
const isModalOpen = ref(false)
const listRef = ref(null) // ArticleList 컴포넌트 참조 아까 만든 fetchArticles 새로고침 쓰려고

const handleCreateClick = () => {
  if (!authStore.isAuthenticated) {
    // TODO: toast로 교체
    // toast.value.showToast('로그인이 필요한 기능입니다.')
    return
  }
  isModalOpen.value = true
}

// 글쓰기 완료 후 목록 새로고침
const handleArticleCreated = () => {
  listRef.value?.fetchArticles() // ArticleList 컴포넌트 내 메서드 호출
  isModalOpen.value = false
}
</script>
