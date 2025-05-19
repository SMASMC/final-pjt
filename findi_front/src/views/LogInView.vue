<template>
  <div class="auth-container">
    <div class="auth-left">
      <h2 class="mb-4">로그인</h2>
      <div class="d-flex justify-content-between mb-3">
        <OAuthButton provider="google" />
        <OAuthButton provider="kakao" />
      </div>
      <AuthForm mode="login" />
    </div>
    <div class="auth-right">
      <h1>Findi</h1>
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
  background-color: #2e2466;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 36px;
  font-weight: bold;
}
</style>
