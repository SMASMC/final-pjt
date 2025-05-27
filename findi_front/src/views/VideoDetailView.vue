<!-- src/views/VideoDetailView.vue -->

<template>
  <div class="max-w-5xl mx-auto px-6 pt-28 pb-12">
    <!--  pt-28로 상단 여백 추가 -->
    <button class="text-[#8A69E1] font-semibold mb-6 hover:underline" @click="goBack">
      ← 뒤로가기
    </button>

    <h1 class="text-3xl font-bold text-gray-900 leading-tight">
      {{ video?.snippet.title }}
    </h1>
    <p class="text-sm text-gray-500 mt-1 mb-4">
      업로드: {{ formatDate(video?.snippet.publishedAt) }}
      <span v-if="video?.snippet.channelTitle"> · {{ video.snippet.channelTitle }}</span>
    </p>

    <div class="w-full h-[480px] mb-6 rounded-lg overflow-hidden shadow">
      <iframe
        class="w-full h-full"
        :src="`https://www.youtube.com/embed/${videoId}`"
        frameborder="0"
        allowfullscreen
      ></iframe>
    </div>

    <div class="flex items-center gap-4 mb-6">
      <button
        class="px-5 py-2 rounded-md text-sm font-semibold transition border"
        :class="
          isSaved
            ? 'bg-purple-500 text-white border-purple-500 hover:bg-purple-800'
            : 'bg-white text-purple-600 border-purple-400 hover:bg-purple-100 hover:border-purple-500'
        "
        @click="toggleSave"
      >
        {{ isSaved ? '✔️ 저장됨' : '❤️ 나중에 보기' }}
      </button>

      <a
        class="text-sm text-blue-600 hover:underline"
        :href="`https://www.youtube.com/watch?v=${videoId}`"
        target="_blank"
      >
        ▶ 유튜브에서 영상 보기
      </a>
    </div>

    <p class="text-gray-800 whitespace-pre-line leading-relaxed mb-8">
      {{ video?.snippet.description }}
    </p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import api from '@/api/axios'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const videoId = route.params.videoId
const video = ref(null)
const isSaved = ref(false)
const authStore = useAuthStore()

const API_URL = 'https://www.googleapis.com/youtube/v3/videos'
const API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY

const fetchVideoDetail = async () => {
  try {
    const response = await axios.get(API_URL, {
      params: {
        key: API_KEY,
        part: 'snippet',
        id: videoId
      }
    })

    if (response.data.items.length === 0) {
      console.warn('⚠️ 해당 videoId에 대한 영상 없음')
      video.value = null
      return
    }
    video.value = response.data.items[0]

    // //  저장 여부 체크 로직 추가
    const check = await api.get(`/videos/later-videos/${videoId}/`)
    isSaved.value = check.data.isSaved
  } catch (error) {
    console.error('❌ 비디오 정보 불러오기 실패:', error)
  }
}

const toggleSave = async () => {
  if (!video.value) return

  try {
    if (isSaved.value) {
      await api.delete(`/videos/later-videos/${videoId}/`) //  axios → api
    } else {
      await api.post('/videos/later-videos/', {
        videoId,
        title: video.value.snippet.title,
        description: video.value.snippet.description,
        thumbnailUrl: video.value.snippet.thumbnails.medium.url,
        publishedAt: video.value.snippet.publishedAt
      })
    }
    isSaved.value = !isSaved.value
  } catch (err) {
    console.error('저장 실패:', err)
    if (err.response) {
      console.error('📦 응답 상태:', err.response.status)
      console.error('📄 응답 내용:', err.response.data)
    }
  }
}

const goBack = () => router.back()
const formatDate = (d) => d?.split('T')[0] || ''

onMounted(() => {
  fetchVideoDetail()
})
</script>
