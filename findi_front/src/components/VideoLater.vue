<!-- src/components/VideoLater.vue -->
<template>
  <div class="mt-6">
    <h4 class="text-lg font-semibold mb-2">저장한 동영상</h4>

    <template v-if="isAuthenticated">
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
import api from '@/api/axios' // ✅ axios instance 가져오기

const savedVideos = ref([])
const authStore = useAuthStore()
const isAuthenticated = ref(false)

const fetchSavedVideos = async () => {

    console.log('🔐 현재 토큰:', authStore.token)

  // 로그인이 안 된 경우 바로 종료 (강제 보호)
  if (!authStore.token) {
    isAuthenticated.value = false
    return
  }

  try {
    const res = await api.get('/videos/later-videos/')
    savedVideos.value = res.data
    isAuthenticated.value = true
  } catch (err) {
    console.error('❌ 저장된 영상 불러오기 실패:', err)
    isAuthenticated.value = false
  }
}


onMounted(() => {
    console.log('📌 VideoLater mounted')
  fetchSavedVideos()
})
</script>