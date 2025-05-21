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

        <Alerts v-if="showAlert" :type="alertType" :message="alertMessage" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue'
import api from '@/api/axios'
import { useRouter } from 'vue-router'
import Alerts from '@/components/Alerts.vue'

const router = useRouter()

const email = ref('')
const code = ref('')
const newPassword = ref('')
const codeSent = ref(false)
const verified = ref(false)

const timer = ref(0)
let interval = null

// Alert를 위한 선언
const showAlert = ref(false)
const alertType = ref('success')
const alertMessage = ref('')

const showSuccess = (msg) => {
  alertType.value = 'success'
  alertMessage.value = msg
  showAlert.value = true
  setTimeout(() => (showAlert.value = false), 3000)
}

const sendCode = async () => {
  try {
    await api.post('/accounts/send-code/', { email: email.value })
    codeSent.value = true
    timer.value = 300
    startTimer()
  } catch (err) {
    console.error(err)
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
  const res = await api.post('/accounts/verify-code/', {
    email: email.value,
    code: code.value
  })
  verified.value = res.data.verified
}

const resetPassword = async () => {
  try {
    await api.post('/accounts/reset-password/', {
      email: email.value,
      new_password: newPassword.value
    })
    showAlert.value = true
    alertType.value = 'success'
    alertMessage.value = '비밀번호가 변경되었습니다.'
    router.push('/login')
  } catch (err) {
    alertType.value = 'danger'
    alertMessage.value = '비밀번호 변경에 실패했습니다.'
    showAlert.value = true
  }
}
// 인터벌 정리 onUnmounted는 컴포넌트가 제거될 때 인터벌을 정리하는 역할을 합니다.
onUnmounted(() => clearInterval(interval))
</script>
