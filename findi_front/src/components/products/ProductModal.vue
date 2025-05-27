<!-- src/components/products/ProductModal.vue -->
<template>
  <!-- 바깥 클릭 시 모달 닫기 -->
  <div class="fixed inset-0 flex justify-center items-center z-50" @click.self="$emit('close')">
    <div class="bg-white p-6 rounded-lg shadow-lg w-[400px] border border-gray-300">
      <h3 class="text-xl font-semibold mb-4">{{ productDetail.fin_prdt_nm }}</h3>
      <p><strong>은행:</strong> {{ productDetail.kor_co_nm }}</p>
      <p><strong>기간:</strong> {{ productDetail.save_trm }}개월</p>

      <template v-if="!editMode">
        <p><strong>기본 금리:</strong> {{ productDetail.intr_rate }}%</p>
        <p><strong>우대 금리:</strong> {{ productDetail.intr_rate2 }}%</p>
      </template>

      <template v-else>
        <label class="block mt-2 text-sm text-gray-600">기본 금리</label>
        <input
          v-model="editForm.intr_rate"
          type="number"
          step="0.01"
          class="w-full border p-2 rounded"
        />
        <label class="block mt-2 text-sm text-gray-600">우대 금리</label>
        <input
          v-model="editForm.intr_rate2"
          type="number"
          step="0.01"
          class="w-full border p-2 rounded"
        />
      </template>

      <p class="mt-2 whitespace-pre-line">
        <strong>우대조건:</strong> {{ productDetail.spcl_cnd }}
      </p>

      <div class="flex justify-end mt-4 flex-wrap gap-2">
        <template v-if="isAuthenticated">
          <button
            v-if="!isJoined"
            class="px-4 py-1 bg-sky-500 text-white rounded hover:bg-slate-600"
            @click="joinProduct"
          >
            상품 가입
          </button>
          <button
            v-else
            class="px-4 py-1 bg-pink-500 text-white rounded hover:bg-pink-600"
            @click="cancelProduct"
          >
            가입 취소
          </button>
        </template>

        <template v-if="authStore.user?.role === 'admin'">
          <button
            v-if="!editMode"
            @click="enableEdit"
            class="px-4 py-1 bg-amber-500 text-white rounded hover:bg-amber-600"
          >
            금리 수정
          </button>
          <div v-else class="flex gap-2">
            <button
              @click="submitEdit"
              class="px-4 py-1 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              저장
            </button>
            <button @click="cancelEdit" class="px-4 py-1 bg-gray-300 rounded hover:bg-gray-400">
              취소
            </button>
          </div>
        </template>

        <button
          class="px-4 py-1 bg-violet-500 text-white rounded hover:bg-violet-600"
          @click="$emit('close')"
        >
          닫기
        </button>
      </div>
    </div>

    <ToastMessage v-if="toast.show" :type="toast.type" :message="toast.message" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import api from '@/api/axios'
import ToastMessage from '../ToastMessage.vue'

const props = defineProps({ product: Object })
const emit = defineEmits(['close', 'updated'])

const authStore = useAuthStore()
const router = useRouter()

const isAuthenticated = ref(!!authStore.accessToken)
const isJoined = ref(!!props.product?.portfolio_id)
const portfolioId = ref(props.product?.portfolio_id || null)
const editMode = ref(false)
const toast = ref({ show: false, type: 'success', message: '' })

watch(
  () => props.product?.portfolio_id,
  (newId) => {
    portfolioId.value = newId
    isJoined.value = !!newId
  }
)

const productDetail = computed(() => {
  return props.product?.deposit_product || props.product?.saving_product || props.product || {}
})

const productType = computed(() => {
  return productDetail.value?.intr_rate !== undefined ? 'deposit' : 'saving'
})

const showToast = (type, message) => {
  toast.value = { type, message, show: true }
  setTimeout(() => (toast.value.show = false), 3000)
}

const editForm = ref({
  intr_rate: productDetail.value.intr_rate,
  intr_rate2: productDetail.value.intr_rate2
})

const joinProduct = async () => {
  try {
    const payload = {
      product_type: productType.value,
      product_id: productDetail.value.id,
      save_trm: parseInt(productDetail.value.save_trm),
      interest_rate: productDetail.value.intr_rate,
      special_rate: productDetail.value.intr_rate2
    }
    const res = await api.post('/accounts/portfolio/', payload)
    if (res.status === 201) {
      const newPortfolio = res.data
      showToast('success', '상품 가입 완료!')
      portfolioId.value = newPortfolio.id
      isJoined.value = true
      emit('updated')
    } else {
      showToast('danger', '예상치 못한 응답입니다.')
    }
  } catch (err) {
    console.error(err)
    showToast('danger', '가입 중 오류가 발생했습니다.')
  }
}

const cancelProduct = async () => {
  if (!portfolioId.value) return
  try {
    await api.delete(`/accounts/portfolio/${portfolioId.value}/delete/`)
    showToast('success', '가입이 취소되었습니다.')
    portfolioId.value = null
    isJoined.value = false
    emit('updated')
    emit('close')
  } catch (err) {
    console.error(err)
    showToast('danger', '가입 취소 중 오류가 발생했습니다.')
  }
}

const enableEdit = () => {
  editForm.value.intr_rate = productDetail.value.intr_rate
  editForm.value.intr_rate2 = productDetail.value.intr_rate2
  editMode.value = true
}
const cancelEdit = () => {
  editMode.value = false
}

const submitEdit = async () => {
  try {
    await api.put(`/finance/${productType.value}/${productDetail.value.id}/update/`, {
      intr_rate: parseFloat(editForm.value.intr_rate),
      intr_rate2: parseFloat(editForm.value.intr_rate2)
    })
    productDetail.value.intr_rate = parseFloat(editForm.value.intr_rate)
    productDetail.value.intr_rate2 = parseFloat(editForm.value.intr_rate2)
    showToast('success', '금리가 수정되었습니다.')
    emit('updated')
    emit('close')
    editMode.value = false
  } catch (err) {
    console.error(err)
    showToast('danger', '금리 수정 실패')
  }
}
</script>
