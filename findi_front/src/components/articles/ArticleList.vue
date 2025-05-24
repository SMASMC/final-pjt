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
        <tr class="border-b">
          <th class="p-2">제목</th>
          <th class="p-2 w-28">작성자</th>
          <th class="p-2 w-32">작성일</th>
          <th class="p-2 w-16 text-right">조회</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="article in articles"
          :key="article.id"
          class="border-b"
        >
          <td
            class="p-2 hover:bg-gray-50 cursor-pointer"
            @click="goToDetail(article.id)"
          >
            {{ article.title }}
          </td>
          <td class="p-2">{{ article.user.userName }}</td>
          <td class="p-2">{{ article.created_at.split('T')[0] }}</td>
          <td class="p-2 text-right">{{ article.views }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/axios'

const articles = ref([])
const searchQuery = ref('')
const router = useRouter()

const fetchArticles = async () => {
  try {
    const { data } = await api.get('/articles/', {
      params: searchQuery.value.trim()
        ? { search: searchQuery.value }
        : undefined
    })
    articles.value = data
  } catch (err) {
    console.error('게시글 목록을 불러오지 못했습니다.', err)
  }
}

const goToDetail = (id) => {
  router.push(`/articles/${id}`)
}

onMounted(() => {
  fetchArticles()
})

// 외부(부모)에서 불러쓸 수 있도록 export
defineExpose({ fetchArticles })
</script>

<style scoped>
</style>
