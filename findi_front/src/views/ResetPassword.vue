<template>
  <div class="min-h-screen flex flex-col items-center justify-center px-4 bg-gray-50">
    <div class="bg-white p-8 rounded shadow-md w-full max-w-md text-center">
      <h2 class="text-2xl font-bold mb-6">비밀번호 재설정</h2>

      <!-- 이메일 입력 -->
      <label class="block text-left mb-2 font-medium">이메일</label>
      <input
        type="email"
        v-model="email"
        placeholder="가입하신 이메일을 입력하세요"
        class="w-full border border-[#d1d5db] px-3 py-2 rounded mb-4"
      />
      <button
        @click="sendCode"
        class="w-full bg-[#8A69E1] hover:bg-[#7a56d9] text-white font-bold py-2 px-4 rounded transition"
      >
        인증번호 발송
      </button>

      <!-- 인증번호 입력 -->
      <div v-if="codeSent" class="mt-6">
        <label class="block text-left mb-2 font-medium">인증번호</label>
        <input
          v-model="code"
          placeholder="인증번호 입력"
          class="w-full border border-[#d1d5db] px-3 py-2 rounded mb-2"
        />
        <button
          @click="verifyCode"
          class="w-full bg-[#8A69E1] hover:bg-[#7a56d9] text-white font-bold py-2 px-4 rounded transition"
        >
          확인
        </button>
      </div>

      <!-- 새 비밀번호 입력 -->
      <div v-if="verified" class="mt-6">
        <label class="block text-left mb-2 font-medium">새 비밀번호</label>
        <input
          v-model="newPassword"
          type="password"
          class="w-full border border-[#d1d5db] px-3 py-2 rounded mb-2"
        />
        <button
          @click="resetPassword"
          class="w-full bg-[#8A69E1] hover:bg-[#7a56d9] text-white font-bold py-2 px-4 rounded transition"
        >
          비밀번호 변경
        </button>
      </div>
    </div>
    <!-- Toast 메시지 -->
    <ToastMessage v-if="toast.show" :type="toast.type" :message="toast.message" />
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue'
import api from '@/api/axios'
import { useRouter } from 'vue-router'
import ToastMessage from '@/components/ToastMessage.vue'

const router = useRouter()

const email = ref('')
const code = ref('')
const newPassword = ref('')
const codeSent = ref(false)
const verified = ref(false)

const timer = ref(0)
let interval = null

const toast = ref({ show: false, type: 'success', message: '' })
const showToast = (type, message) => {
  toast.value = { type, message, show: true }
  setTimeout(() => (toast.value.show = false), 3000)
}

const sendCode = async () => {
  try {
    await api.post('/accounts/send-code/', { email: email.value })
    codeSent.value = true
    timer.value = 300
    startTimer()
    showToast('success', '인증번호가 발송되었습니다.')
  } catch (err) {
    console.error(err)
    showToast('danger', '인증번호 발송에 실패했습니다.')
  }
}

const startTimer = () => {
  clearInterval(interval)
  interval = setInterval(() => {
    if (timer.value > 0) {
      timer.value--
    } else {
      clearInterval(interval)
    }
  }, 1000)
}

const formattedTime = computed(() => {
  const m = String(Math.floor(timer.value / 60)).padStart(2, '0')
  const s = String(timer.value % 60).padStart(2, '0')
  return `${m}:${s}`
})

const verifyCode = async () => {
  try {
    const res = await api.post('/accounts/verify-code/', {
      email: email.value,
      code: code.value
    })
    verified.value = res.data.verified
    if (verified.value) {
      showToast('success', '인증되었습니다.')
    } else {
      showToast('danger', '인증에 실패했습니다.')
    }
  } catch (err) {
    showToast('danger', '인증에 실패했습니다.')
  }
}

const resetPassword = async () => {
  try {
    await api.post('/accounts/reset-password/', {
      email: email.value,
      password: newPassword.value
    })
    showToast('success', '비밀번호가 변경되었습니다.')
    setTimeout(() => router.push('/login'), 1500)
  } catch (err) {
    showToast(
      'danger',
      err.response?.data?.non_field_errors?.[0] || '비밀번호 변경에 실패했습니다.'
    )
  }
}

onUnmounted(() => clearInterval(interval))
</script>
