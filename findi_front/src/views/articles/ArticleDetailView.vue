<!-- /src/views/articles/ArticleDetailView.vue 게시글 상세 페이지 -->

<template>
  <div class="max-w-3xl mx-auto pt-20">
    <h1 class="text-2xl font-bold mb-4">{{ article.title }}</h1>
    <p class="text-sm text-gray-500 mb-4">
      작성자: {{ article.author }} | 작성일: {{ article.date }} | 조회수: {{ article.views }}
    </p>
    <div class="prose whitespace-pre-line" v-html="article.content"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api/axios'

const route = useRoute()

const article = ref({
  id: null,
  title: '',
  content: '',
  author: '',
  date: '',
  views: 0
})

let timer = null
let hasViewed = false // 중복 방지용

// 게시글 상세 조회
const fetchArticle = async () => {
  try {
    const { data } = await api.get(`/articles/${route.params.id}/`)
    article.value = data
  } catch (error) {
    console.error('게시글 로드 실패:', error)
  }
}

// 3초 이상 머무르면 조회수 증가
const delayedViewCount = async () => {
  timer = setTimeout(async () => {
    if (!hasViewed) {
      try {
        await api.post(`/articles/${route.params.id}/increment-views/`)
        hasViewed = true
        article.value.views += 1 // 즉시 반영
      } catch (error) {
        console.error('조회수 증가 실패:', error)
      }
    }
  }, 3000)
}

// 마운트 시 실행
onMounted(() => {
  fetchArticle()
  delayedViewCount()
})

// 언마운트 시 타이머 정리
onBeforeUnmount(() => {
  clearTimeout(timer)
})
</script>
