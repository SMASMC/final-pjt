<!-- src/views/OAuthCallback.vue -->
<template>
  <div>구글 로그인 처리 중입니다...</div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
const router = useRouter()
const store = useAuthStore()
onMounted(async () => {
  try {
    const params = new URLSearchParams(window.location.search)

    const access_token = params.get('access_token')
    const refresh_token = params.get('refresh_token')
    const email = params.get('email')
    const userName = params.get('userName')
    const profileImage = params.get('profileImage')

    if (!access_token || !refresh_token) {
      router.replace({ name: 'login' })
      return
    }

    const user = { email, userName, profileImage }

    // localStorage에 저장
    localStorage.setItem('access_token', access_token)
    localStorage.setItem('refresh_token', refresh_token)
    localStorage.setItem('user', JSON.stringify(user))

    // store에 저장
    store.loginSuccess({ access: access_token, refresh: refresh_token, user })

    // 홈으로 이동
    router.replace({ name: 'home' })
  } catch (error) {
    console.error('OAuth Callback Error:', error)
    router.replace({ name: 'login' })
  }
})
</script>
