<template>
  <div class="max-w-6xl mx-auto p-4 pt-20">
    <!-- 사용자 프로필 상태 확인 -->
    <div v-if="!profileLoaded">
      <p class="text-center text-red-600 font-semibold">
        더 정확한 맞춤 상품을 찾기 위해<br />
        <span class="text-purple-700">프로필에서 {{ userName }}님의 정보를 입력하세요!</span>
      </p>
    </div>

    <!-- AI 추천 카드 출력 -->
    <div v-if="aiProducts" class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
      <div v-for="(product, key) in aiProducts" :key="key" class="border rounded-lg p-6 shadow">
        <h3 class="text-lg font-bold mb-2">{{ categoryToLabel(key) }} 상품 추천</h3>
        <p><strong>상품명:</strong> {{ product.name }}</p>
        <p><strong>금리:</strong> {{ product.rate }}%</p>
        <!-- <p>
          <strong>상품 바로가기:</strong>
          <a :href="product.url" target="_blank">{{ product.url }}</a>
        </p> -->
        <p class="text-sm text-gray-600 mt-2">
          {{ product.details || '설명 없음' }}
        </p>
      </div>
    </div>

    <!-- AI 설명 -->
    <div v-if="aiMessage" class="mt-6 p-4 border border-purple-300 bg-purple-50 rounded">
      <div class="text-sm text-gray-700" v-html="renderedMarkdown"></div>
    </div>

    <!-- AI 맞춤 추천 버튼 -->
    <div class="text-center mt-10">
      <button
        @click="fetchAIRecommendations"
        class="bg-purple-600 text-white px-6 py-3 rounded-full text-lg hover:bg-purple-700 transition"
      >
        AI 맞춤 상품 찾아보기
      </button>
    </div>
  </div>

  <ToastMessage v-if="toast.show" :type="toast.type" :message="toast.message" />
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '@/api/axios'
import { useAuthStore } from '@/stores/auth'
import ToastMessage from '@/components/ToastMessage.vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify' // 보안용 (선택적 권장)

const renderedMarkdown = computed(() => {
  return DOMPurify.sanitize(marked.parse(aiMessage.value || ''))
})

const authStore = useAuthStore()
const userName = authStore.user?.userName || '사용자'
const profileLoaded = ref(false)
const aiProducts = ref(null)
aiProducts.value = null
const aiMessage = ref('')

const toast = ref({ show: false, type: 'success', message: '' })
const showToast = (type, message) => {
  toast.value = { type, message, show: true }
  setTimeout(() => (toast.value.show = false), 3000)
}

const fetchProfileStatus = async () => {
  try {
    const res = await api.get('/accounts/profile/')
    profileLoaded.value = !!res.data.age
  } catch (e) {
    profileLoaded.value = false
  }
}

const fetchAIRecommendations = async () => {
  try {
    const res = await api.get('/finance/find-ai-fit-products/')
    aiProducts.value = res.data.products
    aiMessage.value = res.data.ai_recommendation
    showToast('success', 'AI 추천 결과를 불러왔습니다.')
  } catch (e) {
    showToast('danger', 'AI 추천 호출 실패')
  }
}

const categoryToLabel = (category) => {
  switch (category) {
    case 'deposit':
      return '정기예금'
    case 'saving':
      return '적금'
    default:
      return category
  }
}

onMounted(fetchProfileStatus)
</script>

<style scoped></style>
