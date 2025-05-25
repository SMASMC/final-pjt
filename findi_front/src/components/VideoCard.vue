<!-- src/components/VideoCard.vue -->
<template>
  <div
    v-if="video && video.snippet"
    class="card shadow rounded overflow-hidden cursor-pointer hover:shadow-lg transition h-[380px]"
    @click="goToDetail"
  >
    <img
      :src="video.snippet.thumbnails.medium.url"
      class="w-full h-48 object-cover"
      alt="thumbnail"
    />
    <div class="p-4">
      <h5 class="text-lg font-semibold mb-1 truncate-title">
        {{ video.snippet.title }}
      </h5>
      <p class="text-sm text-gray-600 truncate-description">
        {{ video.snippet.description }}
      </p>
    </div>
    <div class="px-4 pb-4 text-sm text-gray-500">
      업로드: {{ formatDate(video.snippet.publishedAt) }}
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  video: Object
})
const router = useRouter()

const formatDate = (d) => d?.split('T')[0] || ''

const goToDetail = () => {
  const id = props.video.id?.videoId || props.video.id
  if (id) router.push(`/video/${id}`)
}
</script>

<style scoped>
.truncate-title {
  display: -webkit-box;
  -webkit-line-clamp: 2;  /* 최대 2줄 */
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.truncate-description {
  display: -webkit-box;
  -webkit-line-clamp: 3;  /* 최대 3줄 */
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>