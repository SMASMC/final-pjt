import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSearchStore = defineStore('search', () => {
    // 검색 결과를 담아낼 store
  const query = ref('')
  const videos = ref([])

  return { query, videos }
})
