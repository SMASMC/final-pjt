<template>
  <div class="auth-container">
    <div class="auth-left">
      <h2 class="mb-4">회원가입</h2>
      <div class="d-flex justify-between mb-3">
        <OAuthButton provider="google" signType="signup" />
        <OAuthButton provider="kakao" signType="signup" />
      </div>
      <AuthForm mode="signup" />
    </div>
    <div class="auth-right">
      <!-- findi_logo -->
      <img src="@/assets/findi_logo.png" alt="findi_logo" />
    </div>
  </div>
</template>

<script setup>
import OAuthButton from '@/components/OAuthButton.vue'
import AuthForm from '@/components/AuthForm.vue'
</script>

<style scoped>
.auth-container {
  display: flex;
  height: 100vh;
}

.auth-left {
  width: 50%;
  height: 100%;
  padding: 60px;
  background-color: #ffffff; /* 왼쪽 배경 흰색 */
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.auth-right {
  width: 50%;
  height: 100%;
  background-color: #2e2466;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
  font-family: 'BMJUA', sans-serif;
}
</style>
