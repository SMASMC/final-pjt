<template>
  <form @submit.prevent="submitProfile" class="max-w-5xl mx-auto px-6 pt-28 pb-12">
    <h2 class="text-xl font-bold mb-4">내 프로필</h2>

    <!-- 프로필 이미지 업로드 -->
    <div class="flex items-center mb-4">
      <img
        v-if="previewImage"
        :src="previewImage"
        alt="Profile"
        class="w-24 h-24 rounded-full object-cover border mr-4"
      />
      <input type="file" @change="handleImageUpload" accept="image/*" />
    </div>

    <label class="block mb-2">
      나이:
      <input v-model="age" type="number" required class="w-full p-2 border rounded" />
    </label>

    <label class="block mb-2">
      월 수입 (만원):
      <input v-model="monthly_income" type="number" required class="w-full p-2 border rounded" />
    </label>

    <label class="block mb-4">
      모아둔 돈 (만원):
      <input v-model="savings" type="number" required class="w-full p-2 border rounded" />
    </label>

    <label class="block mb-2">
      위험 선호도:
      <select v-model="risk_tolerance" class="w-full p-2 border rounded">
        <option value="low">낮음</option>
        <option value="medium">중간</option>
        <option value="high">높음</option>
      </select>
    </label>

    <label class="block mb-2">
      재무 목표:
      <select v-model="financial_goal" class="w-full p-2 border rounded">
        <option value="saving">저축</option>
        <option value="investment">투자</option>
        <option value="retirement">은퇴 준비</option>
      </select>
    </label>

    <label class="block mb-4">
      관심 금융 상품:
      <div class="flex gap-2 mt-1">
        <label><input type="checkbox" value="deposit" v-model="interested_products" /> 예금</label>
        <label><input type="checkbox" value="loan" v-model="interested_products" /> 대출</label>
        <label
          ><input type="checkbox" value="insurance" v-model="interested_products" /> 보험</label
        >
        <label><input type="checkbox" value="fund" v-model="interested_products" /> 펀드</label>
      </div>
    </label>

    <button type="submit" class="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700">
      저장
    </button>

    <button
      type="button"
      @click="showModal = true"
      class="mt-4 w-full text-sm text-red-500 underline"
    >
      회원 탈퇴
    </button>
  </form>

  <!-- 가입한 금융 상품 리스트 -->
  <div class="max-w-5xl mx-auto px-6 pb-12">
    <h3 class="text-lg font-bold mt-10 mb-4">📌 가입한 금융 상품</h3>
    <table class="w-full border text-sm">
      <thead class="bg-gray-100">
        <tr>
          <th class="p-2 border">은행</th>
          <th class="p-2 border">상품명</th>
          <th class="p-2 border">유형</th>
          <th class="p-2 border">금리(%)</th>
          <th class="p-2 border">중도상환수수료(%)</th>
          <th class="p-2 border">가입일</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in portfolios" :key="product.id">
          <td class="p-2 border">{{ product.bankName }}</td>
          <td class="p-2 border">{{ product.productName }}</td>
          <td class="p-2 border">{{ product.productType }}</td>
          <td class="p-2 border">{{ product.interestRate }}</td>
          <td class="p-2 border">{{ product.prePaymentPenalty }}</td>
          <td class="p-2 border">{{ formatDate(product.joinedAt) }}</td>
        </tr>
      </tbody>
    </table>
  </div>

  <ConfirmModal
    :show="showModal"
    title="회원 탈퇴 확인"
    content="정말로 회원 탈퇴하시겠습니까? 이 작업은 되돌릴 수 없습니다."
    confirmText="탈퇴하기"
    cancelText="취소"
    @confirm="deleteAccount"
    @cancel="showModal = false"
  />

  <ToastMessage v-if="toast.show" :type="toast.type" :message="toast.message" />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/axios'
import ConfirmModal from '@/components/ConfirmModal.vue'
import ToastMessage from '@/components/ToastMessage.vue'
import { useAuthStore } from '@/stores/auth'

const age = ref('')
const risk_tolerance = ref('medium')
const financial_goal = ref('saving')
const interested_products = ref([])
const monthly_income = ref('')
const savings = ref('')
const profileImage = ref(null)
const previewImage = ref(null)
const portfolios = ref([])

const showModal = ref(false)
const toast = ref({ show: false, type: 'success', message: '' })

const showToast = (type, message) => {
  toast.value = { type, message, show: true }
  setTimeout(() => (toast.value.show = false), 3000)
}

const handleImageUpload = (e) => {
  const file = e.target.files[0]
  if (file) {
    profileImage.value = file
    previewImage.value = URL.createObjectURL(file)
  }
}

const formatDate = (date) => {
  if (!date) return '-'
  const d = new Date(date)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

const loadProfile = async () => {
  try {
    const res = await api.get('/accounts/profile/')
    const profile = res.data
    age.value = profile.age
    risk_tolerance.value = profile.risk_tolerance
    financial_goal.value = profile.financial_goal
    interested_products.value = profile.interested_products
    monthly_income.value = profile.monthly_income
    savings.value = profile.savings
    previewImage.value = profile.profileImage
      ? import.meta.env.VITE_BACKEND_URL + profile.profileImage
      : null

    portfolios.value = profile.portfolio || []
  } catch (error) {
    console.error('프로필 로딩 실패:', error)
    showToast('danger', '프로필 정보가 아직 없습니다. <br/>정보를 입력해주세요.')
  }
}

const submitProfile = async () => {
  try {
    const formData = new FormData()
    formData.append('age', age.value)
    formData.append('risk_tolerance', risk_tolerance.value)
    formData.append('financial_goal', financial_goal.value)
    formData.append('interested_products', JSON.stringify(interested_products.value))
    formData.append('monthly_income', monthly_income.value)
    formData.append('savings', savings.value)
    if (profileImage.value) {
      formData.append('profileImage', profileImage.value)
    }

    const response = await api.put('/accounts/profile/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    const updatedProfileImage = response.data.profileImage
    const authStore = useAuthStore()
    if (authStore.user && authStore.user.profile) {
      authStore.profileImage = updatedProfileImage

      const saved = JSON.parse(localStorage.getItem('auth'))
      if (saved && saved.user?.profile) {
        saved.user.profile.profileImage = updatedProfileImage
        localStorage.setItem('auth', JSON.stringify(saved))
      }
    }

    showToast('success', '프로필이 저장되었습니다.')
  } catch (error) {
    console.error(error)
    showToast('danger', '프로필 저장에 실패했습니다.')
  }
}

const deleteAccount = async () => {
  try {
    await api.delete('/accounts/delete-account/')
    localStorage.clear()
    showToast('success', '회원 탈퇴가 완료되었습니다.')
    setTimeout(() => {
      window.location.href = '/'
    }, 1500)
  } catch (error) {
    console.error(error)
    showToast('danger', '회원 탈퇴에 실패했습니다.')
  }
}

onMounted(loadProfile)
</script>

<style scoped>
input[type='file']::-webkit-file-upload-button {
  margin-right: 1rem;
}
</style>
