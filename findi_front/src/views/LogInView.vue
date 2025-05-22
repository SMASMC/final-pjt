<template>
  <div class="auth-container">
    <div class="auth-left">
      <h2 class="mb-4 !items-start text-3xl">로그인</h2>
      <p class="font-normal text-[14px] mb-5 text-[#555555]">
        Findi에 오신것을 환영합니다! <br />
        이메일과 비밀번호를 입력하여 로그인하세요!
      </p>
      <div class="w-full flex gap-4 justify-between mb-3">
        <OAuthButton class="rounded-lg cursor-pointer" provider="google" />
        <OAuthButton class="rounded-lg cursor-pointer" provider="kakao" />
      </div>
      <AuthForm class="w-full" mode="login" />
      <div class="text-right mt-2">
        <button class="forgot-btn" @click="goToPasswordReset">비밀번호를 잊으셨나요?</button>
      </div>
    </div>
    <div class="auth-right">
      <img src="@/assets/findi_logo.png" alt="findi_logo" />
    </div>
  </div>
</template>

<script setup>
import OAuthButton from '@/components/OAuthButton.vue'
import AuthForm from '@/components/AuthForm.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const goToPasswordReset = () => {
  router.push('/password-reset') // 비밀번호 재설정 페이지로 이동
}
</script>

<style scoped>
.auth-container {
  display: flex;
  height: 100vh;
}

.auth-left {
  width: 50%;
  height: 100%;
  background-color: #2e2466;
  /* color: white; */
  /* font-size: 48px; */
  font-weight: bold;
  font-family: 'BMJUA', sans-serif;
}

.auth-right {
  width: 50%;
  height: 100%;
  background-color: #2e2466;
  /* color: white; */
  display: flex;
  justify-content: center;
  align-items: center;
  /* font-size: 48px; */
  font-weight: bold;
  font-family: 'BMJUA', sans-serif;
}

.forgot-btn {
  color: #dc2626; /* tailwind red-600 */
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  background: none;
  border: none;
  padding: 0;
}

.auth-left {
  padding: 60px 100px;
  background-color: #ffffff; /* 왼쪽 배경 흰색 */
  display: flex;
  flex-direction: column;
  justify-content: center;
}
</style>
