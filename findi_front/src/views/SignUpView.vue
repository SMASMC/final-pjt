<template>
  <div class="auth-container">
    <div class="auth-left">
      <h2 class="mb-4">회원가입</h2>
      <div class="d-flex justify-content-between mb-3">
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
  flex: 1;
  padding: 60px;
}
.auth-right {
  flex: 1;
  background-color: #2c266a;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 36px;
  font-weight: bold;
}
</style>
