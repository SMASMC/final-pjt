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
        class="bg-purple-500 text-white px-4 py-1 rounded hover:bg-purple-600"
      >
        검색
      </button>
    </div>

    <!-- 게시글 목록 테이블 -->
    <table class="table-auto w-full text-sm border-collapse">
      <thead class="bg-gray-100 text-gray-700 text-left">
        <tr class="border-b border-purple-500">
          <th class="p-2 w-12 text-center">번호</th>
          <th class="p-2">제목</th>
          <th class="p-2 w-28">작성자</th>
          <th class="p-2 w-32">작성일</th>
          <th class="p-2 w-16 text-right">조회</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(article, index) in articles"
          :key="article.id"
          class="border-b border-purple-200"
        >
          <td class="p-2 text-center">
            {{ totalCount - ((currentPage - 1) * articlesPerPage + index) }}
          </td>
          <td
            class="p-2 hover:bg-gray-50 cursor-pointer"
            @click="goToDetail(article.id)"
          >
            {{ article.title }}
          </td>
          <td class="p-2">{{ article.user?.userName || '알 수 없음' }}</td>
          <td class="p-2">{{ formatDate(article.created_at) }}</td>
          <td class="p-2 text-right">{{ article.views }}</td>
        </tr>
        <tr v-if="articles.length === 0">
          <td colspan="5" class="p-4 text-center text-gray-400">게시글이 없습니다.</td>
        </tr>
      </tbody>
    </table>

    <!-- 페이지네이션 -->
    <div v-if="totalPages > 1" class="flex justify-center gap-2 mt-6">
      <button
        v-for="page in totalPages"
        :key="page"
        @click="changePage(page)"
        :class="[
          'px-3 py-1 border rounded',
          currentPage === page ? 'bg-purple-500 text-white' : 'hover:bg-gray-100'
        ]"
      >
        {{ page }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/axios'

const articles = ref([])
const searchQuery = ref('')
const router = useRouter()

const currentPage = ref(1)
const articlesPerPage = 15
const totalPages = ref(1)
const totalCount = ref(0) // 전체 게시글 수

const fetchArticles = async () => {
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
  }
}

const changePage = (page) => {
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
</style>
