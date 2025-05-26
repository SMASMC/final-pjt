<template>
  <div class="fixed inset-0 flex justify-center items-center z-50">
    <div class="bg-white p-6 rounded-lg shadow-lg w-[400px] border border-gray-300">
      <h3 class="text-xl font-semibold mb-4">{{ product.fin_prdt_nm }}</h3>
      <p><strong>은행:</strong> {{ product.kor_co_nm }}</p>
      <p><strong>기간:</strong> {{ product.save_trm }}개월</p>

      <template v-if="!editMode">
        <p><strong>기본 금리:</strong> {{ product.intr_rate }}%</p>
        <p><strong>우대 금리:</strong> {{ product.intr_rate2 }}%</p>
      </template>

      <template v-else>
        <label class="block mt-2 text-sm text-gray-600">기본 금리</label>
        <input v-model="editForm.intr_rate" type="number" step="0.01" class="w-full border p-2 rounded" />
        <label class="block mt-2 text-sm text-gray-600">우대 금리</label>
        <input v-model="editForm.intr_rate2" type="number" step="0.01" class="w-full border p-2 rounded" />
      </template>

      <p class="mt-2 whitespace-pre-line"><strong>우대조건:</strong> {{ product.spcl_cnd }}</p>

      <!-- 하단 버튼 영역 -->
      <div class="flex justify-end mt-4 flex-wrap gap-2">
        <!-- 가입 or 취소 -->
        <template v-if="isAuthenticated">
          <button v-if="!isJoined" class="px-4 py-1 bg-sky-500 text-white rounded hover:bg-slate-600"
            @click="joinProduct">상품 가입</button>
          <button v-else class="px-4 py-1 bg-pink-500 text-white rounded hover:bg-pink-600" @click="cancelProduct">가입
            취소</button>
        </template>

        <!-- 관리자 금리 수정 -->
        <template v-if="authStore.user?.role === 'admin'">
          <button v-if="!editMode" @click="enableEdit"
            class="px-4 py-1 bg-amber-500 text-white rounded hover:bg-amber-600">금리 수정</button>
          <div v-else class="flex gap-2">
            <button @click="submitEdit" class="px-4 py-1 bg-blue-600 text-white rounded hover:bg-blue-700">저장</button>
            <button @click="cancelEdit" class="px-4 py-1 bg-gray-300 rounded hover:bg-gray-400">취소</button>
          </div>
        </template>

        <!-- 닫기 -->
        <button class="px-4 py-1 bg-violet-500 text-white rounded hover:bg-violet-600"
          @click="$emit('close')">닫기</button>
      </div>
    </div>

    <ToastMessage v-if="toast.show" :type="toast.type" :message="toast.message" />
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import api from '@/api/axios'
import { useRouter } from 'vue-router'
import { ref, onMounted, watchEffect } from 'vue'
import ToastMessage from '../ToastMessage.vue'

const props = defineProps({ product: Object })
const emit = defineEmits(['close'])

const authStore = useAuthStore()
const router = useRouter()
const isAuthenticated = ref(!!authStore.accessToken)

const editMode = ref(false)
const isJoined = ref(false)
const portfolioId = ref(null)
const editForm = ref({
  intr_rate: props.product.intr_rate,
  intr_rate2: props.product.intr_rate2,
})

const toast = ref({ show: false, type: 'success', message: '' })
const showToast = (type, message) => {
  toast.value = { type, message, show: true }
  setTimeout(() => (toast.value.show = false), 3000)
}

// 가입 여부 확인 함수
const checkPortfolio = async () => {
  if (!isAuthenticated.value) return

  const productType = props.product.intr_rate !== undefined ? 'deposit' : 'saving'
  const productCode = props.product.fin_prdt_cd

  try {
    const res = await api.get('/accounts/portfolio/')
    const matched = res.data.find(p =>
      p.product_type === productType &&
      (
        (productType === 'deposit' && p.deposit_product?.fin_prdt_cd === productCode) ||
        (productType === 'saving' && p.saving_product?.fin_prdt_cd === productCode)
      )
    )
    isJoined.value = !!matched
    portfolioId.value = matched?.id || null
  } catch (err) {
    console.error('포트폴리오 조회 실패:', err)
  }
}


// 모달 열리거나 상품 변경될 때마다 실행
onMounted(() => checkPortfolio())

watchEffect(() => {
  props.product?.id // 의존성 등록
  checkPortfolio()
})

// 가입 요청
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

    if (res.status === 201) {
      showToast('success', '상품 가입 완료!')
      await checkPortfolio()
      emit('updated')
    } else {
      showToast('danger', '예상치 못한 응답입니다.')
    }
  } catch (err) {
    showToast('danger', '오류가 발생했습니다.')
    console.error(err)
  }
}

// 가입 취소 요청
const cancelProduct = async () => {
  if (!portfolioId.value) return
  try {
    await api.delete(`/accounts/portfolio/${portfolioId.value}/delete/`)
    showToast('success', '가입이 취소되었습니다.')
    emit('updated')   //부모에게 갱신 요청
    emit('close')
  } catch (err) {
    showToast('danger', '가입 취소 중 오류가 발생했습니다.')
    console.error(err)
  }
}


// 금리 수정 로직
const enableEdit = () => {
  editForm.value.intr_rate = props.product.intr_rate
  editForm.value.intr_rate2 = props.product.intr_rate2
  editMode.value = true
}
const cancelEdit = () => { editMode.value = false }

const submitEdit = async () => {
  try {
    const productType = props.product.intr_rate !== undefined ? 'deposit' : 'saving'
    await api.put(`/finance/${productType}/${props.product.id}/update/`, {
      intr_rate: parseFloat(editForm.value.intr_rate),
      intr_rate2: parseFloat(editForm.value.intr_rate2),
    })
    props.product.intr_rate = parseFloat(editForm.value.intr_rate)
    props.product.intr_rate2 = parseFloat(editForm.value.intr_rate2)
    showToast('success', '금리가 수정되었습니다.')
    emit('updated')
    emit('close')
    editMode.value = false
  } catch (err) {
    showToast('danger', '금리 수정 실패')
    console.error(err)
  }
}
</script>