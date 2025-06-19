<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/axios'

const router = useRouter()
const store = useAuthStore()

onMounted(async () => {
  try {
    const params = new URLSearchParams(window.location.search)
    const access_token = params.get('access_token')

    if (!access_token) {
      router.replace({ name: 'login' })
      return
    }

    // 사용자 정보 요청
    const res = await api.get('/accounts/profile/', {
      headers: {
        Authorization: `Bearer ${access_token}`
      }
    })

    const { user } = res.data

    if (!user?.id) {
      throw new Error('사용자 정보 누락')
    }

    // JWT 저장 및 유저 정보 저장
    store.loginSuccess({
      access: access_token,
      user
    })

    router.replace({ name: 'home' })
  } catch (error) {
    console.error('OAuth Callback Error:', error)
    store.logout()
    router.replace({ name: 'login' })
  }
})
</script>
