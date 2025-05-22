<!-- src/views/VideoSearchView.vue -->
<template>
  <div class="max-w-6xl mx-auto p-4 pt-20">
    <div class="flex gap-2 items-center">
      <input 
      v-model="query" 
      class="w-full h-10 p-2 border border-purple-300 rounded" 
      placeholder="검색어를 입력하세요" @keyup.enter="fetchVideos"/>

      <button class="h-10 px-4 bg-purple-400 text-white rounded hover:bg-purple-700 text-sm whitespace-nowrap" 
      @click="fetchVideos">검색</button>
    </div>

    <h3 class="mt-6 text-xl font-semibold">검색 결과</h3>
    <VideoCardList :videos="searchResults" />
    <br>
    <hr class="border-t border-pink-300 my-4">
    <h3 class="mt-10 text-xl font-semibold">나중에 볼 동영상</h3>
    <VideoLater />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import VideoCardList from '@/components/VideoCardList.vue'
import VideoLater from '@/components/VideoLater.vue'

const query = ref('')
const searchResults = ref([])

const API_URL = 'https://www.googleapis.com/youtube/v3/search'
const API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY

const fetchVideos = async () => {
  try {
    const response = await axios.get(API_URL, {
      params: {
        key: API_KEY,
        part: 'snippet',
        type: 'video',
        maxResults: 8,
        q: query.value
      }
    })
    searchResults.value = response.data.items
  } catch (error) {
    console.error('영상 불러오기 실패:', error)
  }
}
</script>

<style>

</style>