<!-- Google, Kakao OAuth 로그인 Button -->
<!-- OAuthButton.vue -->
<template>
  <button :class="['btn', provider]" @click="handleLogin">
    <img :src="icon" alt="icon" width="20" class="me-2" />
    <span>{{ label }}</span>
  </button>
</template>

<script setup>
import googleIcon from '@/assets/google.png'
import kakaoIcon from '@/assets/kakao.png'

const props = defineProps({
  provider: { type: String, required: true }, // 'google' | 'kakao'
  signType: { type: String, required: true } // 'signin' | 'signup'
})

const icon = props.provider === 'google' ? googleIcon : kakaoIcon
let label = props.provider === 'google' ? '구글로 로그인' : '카카오로 로그인'
// signType이 signup이면 label을 회원가입으로 변경
if (props.signType === 'signup') {
  label = props.provider === 'google' ? '구글로 회원가입' : '카카오로 회원가입'
}

const handleLogin = () => {
  if (props.provider === 'google') {
    window.location.href = import.meta.env.VITE_BACKEND_URL + '/accounts/google/login/'
  } else if (props.provider === 'kakao') {
    window.location.href = import.meta.env.VITE_BACKEND_URL + '/accounts/kakao/login/'
  }
}
</script>

<style scoped>
.google {
  background-color: white;
  border: 1px solid #ddd;
  color: black;
}
.kakao {
  background-color: #f7e600;
  border: none;
  color: #3c1e1e;
}
.btn {
  width: 100%;
  padding: 10px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
