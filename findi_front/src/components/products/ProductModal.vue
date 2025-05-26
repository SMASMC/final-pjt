<!-- src/components/products/ProductModal.vue -->

<template>
  <div class="fixed inset-0 flex justify-center items-center z-50">
    <div class="bg-white p-6 rounded-lg shadow-lg w-[400px] border border-gray-300">
      <h3 class="text-xl font-semibold mb-4">{{ product.fin_prdt_nm }}</h3>
      <p><strong>은행:</strong> {{ product.kor_co_nm }}</p>
      <p><strong>기간:</strong> {{ product.save_trm }}개월</p>
      <p><strong>기본 금리:</strong> {{ product.intr_rate ? product.intr_rate + '%' : '-' }}</p>
      <p><strong>우대 금리:</strong> {{ product.intr_rate2 ? product.intr_rate2 + '%' : '-' }}</p>
      <p class="mt-2 whitespace-pre-line"><strong>우대조건:</strong> {{ product.spcl_cnd }}</p>
      
      <div class="flex justify-end mt-4">
        <button
            v-if="isAuthenticated"
            class="px-4 py-1 bg-green-500 text-white rounded hover:bg-green-600 mr-2"
            @click="joinProduct">
            상품 가입
        </button>

        <button class="px-4 py-1 bg-purple-500 text-white rounded hover:bg-purple-600" 
        @click="$emit('close')">닫기</button>
      </div>
    </div>
  </div>
    <ToastMessage v-if="toast.show" :type="toast.type" :message="toast.message" />

</template>


<script setup>
  import { useAuthStore } from '@/stores/auth'
  import api from '@/api/axios'
  import { useRouter } from 'vue-router'
  import { ref } from 'vue'
  import ToastMessage from '../ToastMessage.vue'

  const props = defineProps({ product: Object })
  const emit = defineEmits(['close'])

  const authStore = useAuthStore()
  const router = useRouter()
  const isAuthenticated = ref(!!authStore.accessToken)


  const toast = ref({ show: false, type: 'success', message: '' })
  const showToast = (type, message) => {
    toast.value = { type, message, show: true }
    setTimeout(() => (toast.value.show = false), 3000)
  }

const joinProduct = async () => {
  try {
    const payload = {
      product_type: props.product.intr_rate !== undefined ? 'deposit' : 'saving',
      product_id: props.product.id,
      save_trm: parseInt(props.product.save_trm),
      interest_rate: props.product.intr_rate,
      special_rate: props.product.intr_rate2,
    }

    const res = await api.post('/accounts/portfolio/', payload)
    console.log('가입 응답:', res.data)

    if (res.status === 201) {
      showToast('success', '상품 가입 완료!')
      setTimeout(() => {
        emit('close')
        router.push('/profile')
      }, 1000)
    } else if (res.status === 200 && res.data.message?.includes('이미 가입')) {
      showToast('warning', '이미 가입한 상품입니다.')
    } else {
      showToast('danger', '예상치 못한 응답입니다.')
    }

  } catch (err) {
    showToast('danger', '오류가 발생했습니다.')
    console.error(err)
  }
}

</script>
