<!-- src/components/VideoLater.vue -->
<template>
  <div class="mt-6">
    <h4 class="text-lg font-semibold mb-2">저장한 동영상</h4>

    <!-- 로그인 확인 -->
    <template v-if="authStore.isAuthenticated">
      <VideoCardList v-if="savedVideos.length" :videos="savedVideos" />
      <p v-else class="text-sm text-gray-400">아직 저장한 영상이 없습니다.</p>
    </template>

    <p v-else class="text-sm text-gray-400">로그인이 필요합니다.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import VideoCardList from './VideoCardList.vue'
import api from '@/api/axios'

const savedVideos = ref([])
const authStore = useAuthStore()

const fetchSavedVideos = async () => {
  if (!authStore.isAuthenticated) {
    console.log('로그인하지 않았습니다.')
    return
  }

  try {
    const res = await api.get('/videos/later-videos/')

    // YouTube API 포맷으로 맞춤
    savedVideos.value = res.data.map((v) => ({
      id: v.videoId,
      snippet: {
        title: v.title,
        description: v.description,
        publishedAt: v.publishedAt,
        thumbnails: {
          medium: {
            url: v.thumbnailUrl
          }
        }
      }
    }))
  } catch (err) {
    console.error('저장된 영상 불러오기 실패:', err)
  }
}

onMounted(() => {
  authStore.initAuth() 
  fetchSavedVideos()
})
</script>
