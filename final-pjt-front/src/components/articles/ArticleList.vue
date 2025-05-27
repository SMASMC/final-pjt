<template>
  <div>
    <!-- 검색창 -->
    <div class="flex gap-2 justify-end mb-4">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="제목으로 검색"
        class="border border-gray-300 px-3 py-1 rounded w-80"
      />
      <button
        @click="fetchArticles"
        class="bg-[#8A69E1] text-white px-4 py-1 rounded hover:bg-purple-700 transition"
      >
        검색
      </button>
    </div>

    <!-- 로딩 중 -->
    <div v-if="isLoading" class="flex justify-center items-center mt-6">
      <div
        class="w-6 h-6 border-4 border-purple-400 border-t-transparent rounded-full animate-spin"
      ></div>
    </div>

    <!-- 게시글 목록 테이블 -->
    <table v-if="!isLoading" class="table-auto w-full text-sm border-collapse">
      <thead class="bg-gray-100 text-gray-700 text-left">
        <tr class="border-b border-purple-500">
          <th class="p-2 w-12 text-center">번호</th>
          <th class="p-2">제목</th>
          <th class="p-2 w-28">작성자</th>
          <th class="p-2 w-32">작성일</th>
          <th class="p-2 w-16 text-right">조회</th>
        </tr>
      </thead>
      <transition-group name="fade" tag="tbody">
        <tr
          v-for="(article, index) in articles"
          :key="article.id"
          class="hover:bg-gray-100 cursor-pointer text-center hover:scale-105 duration-300"
        >
          <td class="p-2">{{ totalCount - ((currentPage - 1) * articlesPerPage + index) }}</td>
          <td class="p-2" @click="goToDetail(article.id)">
            {{ article.title }}
          </td>
          <td class="p-2">{{ article.user?.userName || '알 수 없음' }}</td>
          <td class="p-2">{{ formatDate(article.created_at) }}</td>
          <td class="p-2 text-right">{{ article.views }}</td>
        </tr>
        <tr v-if="articles.length === 0">
          <td colspan="5" class="p-4 text-center text-gray-400">게시글이 없습니다.</td>
        </tr>
      </transition-group>
    </table>

    <!-- 페이지네이션 -->
    <div v-if="totalPages > 1" class="flex justify-center gap-1 mt-6 flex-wrap">
      <!-- 이전 화살표 -->
      <button
        @click="changePage(currentPage - 1)"
        :disabled="currentPage === 1"
        class="w-8 h-8 flex items-center justify-center rounded-full border border-gray-300 bg-gray-50 hover:bg-gray-100 transition disabled:opacity-30"
      >
        <span
          class="inline-block w-2 h-2 border-t-2 border-l-2 border-[#8A69E1] rotate-[-45deg]"
        ></span>
      </button>

      <!-- 페이지 번호 -->
      <button
        v-for="page in visiblePageNumbers"
        :key="page"
        @click="changePage(page)"
        :class="[
          'min-w-[2.25rem] h-8 flex items-center justify-center rounded-full border text-sm transition',
          page === currentPage
            ? 'bg-[#8A69E1] text-white font-bold'
            : 'bg-white text-[#8A69E1] hover:bg-purple-100 hover:text-[#8A69E1]'
        ]"
      >
        {{ page }}
      </button>

      <!-- 다음 화살표 -->
      <button
        @click="changePage(currentPage + 1)"
        :disabled="currentPage === totalPages"
        class="w-8 h-8 flex items-center justify-center rounded-full border border-gray-300 bg-gray-50 hover:bg-gray-100 transition disabled:opacity-30"
      >
        <span
          class="inline-block w-2 h-2 border-t-2 border-r-2 border-[#8A69E1] rotate-[45deg]"
        ></span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/axios'

const articles = ref([])
const searchQuery = ref('')
const router = useRouter()

const currentPage = ref(1)
const articlesPerPage = 15
const totalPages = ref(1)
const totalCount = ref(0)
const isLoading = ref(false)

const maxVisiblePages = 5
const visiblePageNumbers = computed(() => {
  const pages = []
  const half = Math.floor(maxVisiblePages / 2)
  let start = Math.max(1, currentPage.value - half)
  let end = Math.min(totalPages.value, start + maxVisiblePages - 1)

  if (end - start < maxVisiblePages - 1) {
    start = Math.max(1, end - maxVisiblePages + 1)
  }

  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})

const fetchArticles = async () => {
  isLoading.value = true
  try {
    const { data } = await api.get('/articles/', {
      params: {
        page: currentPage.value,
        page_size: articlesPerPage,
        search: searchQuery.value.trim() || undefined
      }
    })

    if (Array.isArray(data.results)) {
      articles.value = data.results
      totalCount.value = data.count
      totalPages.value = Math.ceil(data.count / articlesPerPage)
    } else {
      articles.value = data
      totalPages.value = 1
      totalCount.value = data.length || 0
    }
  } catch (err) {
    console.error('게시글 목록을 불러오지 못했습니다.', err)
    articles.value = []
    totalPages.value = 1
    totalCount.value = 0
  } finally {
    isLoading.value = false
  }
}

const changePage = (page) => {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
  fetchArticles()
}

const goToDetail = (id) => {
  router.push(`/articles/${id}`)
}

const formatDate = (iso) => {
  if (!iso) return ''
  const date = new Date(iso)
  return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`
}

onMounted(() => {
  fetchArticles()
})

defineExpose({ fetchArticles })
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
