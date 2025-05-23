<template>
  <div>
    <!-- 검색 입력창 -->
    <div class="flex gap-2 justify-end mb-4">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="제목 검색"
        class="border border-gray-300 px-3 py-1 rounded w-64"
      />
      <button
        @click="handleSearch"
        class="bg-purple-500 text-white px-4 py-1 rounded hover:bg-purple-600"
      >
        검색
      </button>
    </div>

    <!-- 게시판 테이블 -->
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
          class="border-b hover:bg-gray-50 cursor-pointer"
          @click="goToDetail(article.id)"
        >
          <td class="p-2 text-blue-600 hover:underline">{{ article.title }}</td>
          <td class="p-2">{{ article.user }}</td>
          <td class="p-2">{{ article.created_at }}</td>
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

const router = useRouter()
const searchQuery = ref('')
const articles = ref([])

// 외부에서 접근 가능하게 export => 부모 컴포넌트(articleview.vue)가 새로고침 할 수 있게
const fetchArticles = async () => {
  try {
    const { data } = await api.get('/articles/', {
      params: searchQuery.value.trim() ? { search: searchQuery.value } : {}
    })
    articles.value = data
  } catch (err) {
    console.error('게시글 로드 실패:', err)
  }
}
defineExpose({ fetchArticles })

onMounted(fetchArticles)

const goToDetail = (id) => {
  router.push(`/articles/${id}`)
}
</script>
