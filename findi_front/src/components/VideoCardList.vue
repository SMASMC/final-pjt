<!-- src/components/VideoCardList.vue -->
<template>
  <div
    v-if="videos && videos.length"
    class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6"
  >
    <VideoCard
      v-for="video in videos"
      :key="video.id?.videoId || video.id"
      :video="video"
    />
  </div>
  <p v-else class="text-sm text-gray-400 pt-2">
    검색하여 영상을 찾아보세요
  </p>
</template>

<script setup>
import VideoCard from './VideoCard.vue'
defineProps({ 
  videos: Array 
  })
</script>