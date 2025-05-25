<template>
  <div class="max-w-6xl mx-auto p-4 pt-20">
    <div class="grid grid-cols-1 md:grid-cols-3">
      <BankCard
        v-for="(data, name) in banks"
        :key="name"
        :name="name"
        :logo="data.logo"
        :products="data.products"
        :has-profile="true"
        :card-back-gradient="getCardGradient(name)"
      />
    </div>
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
    <div v-if="profileLoaded">
      <div class="text-center mt-10">
        <button
          @click="fetchAIRecommendations"
          class="bg-purple-600 text-white px-6 py-3 rounded-full text-lg hover:bg-purple-700 transition"
        >
          AI 맞춤 상품 찾아보기
        </button>
      </div>
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
import BankCard from '@/components/recommend/BankCard.vue'
import kbLogo from '@/assets/bank_logos/kb.png'
import nhLogo from '@/assets/bank_logos/nh.png'
import shinhanLogo from '@/assets/bank_logos/shinhan.png'
import wooriLogo from '@/assets/bank_logos/woori.png'
import hanaLogo from '@/assets/bank_logos/hana.png'

const banks = ref({})
// ✅ 은행명과 로고 경로 매핑
const bankLogos = {
  국민은행: kbLogo,
  농협은행주식회사: nhLogo,
  신한은행: shinhanLogo,
  우리은행: wooriLogo,
  하나은행: hanaLogo
}
const getCardGradient = (bankName) => {
  switch (bankName) {
    case '국민은행':
      return 'linear-gradient(135deg, #f7971e, #ffd200)'
    case '농협은행주식회사':
      return 'linear-gradient(135deg, #EFBE00 50%, #035BAF 50%)'
    case '신한은행':
      return 'linear-gradient(135deg, #0046FF 50%, #0046FF 50%)'
    case '우리은행':
      return 'linear-gradient(135deg, #3AB9FF 29%, #007BC7 75%)'
    case '하나은행':
      return 'linear-gradient(135deg, #D8241C 25%, #009178 75%)'
    default:
      return 'linear-gradient(135deg, #999, #ccc)'
  }
}

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
    console.log('profile:', JSON.stringify(res.data))
    profileLoaded.value = !!res.data.user.profile.age
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
onMounted(async () => {
  await fetchProfileStatus()
  try {
    const res = await api.get('/finance/banks/products/')
    const rawData = res.data

    // 로고 경로 병합
    for (const bankName in rawData) {
      rawData[bankName].logo = bankLogos[bankName] || ''
    }

    banks.value = rawData
    console.log('banks:', banks.value)
  } catch (e) {
    console.error('은행 상품 로딩 실패:', e)
  }
})
</script>

<style scoped></style>
