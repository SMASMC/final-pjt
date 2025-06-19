import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from '@/api/axios'

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref(null)
  const user = ref(null)
  const profileImage = ref(null)

  const isAuthenticated = computed(() => !!accessToken.value)

  // 앱 시작 시 localStorage에서 복구
  const initAuth = () => {
    try {
      const saved = JSON.parse(localStorage.getItem('auth'))
      if (saved) {
        accessToken.value = saved.accessToken
        user.value = saved.user
        profileImage.value = saved.profileImage || null
      }
    } catch (e) {
      console.warn('auth 복구 실패:', e)
    }
  }

  // 로그인 성공 시 상태 업데이트 + localStorage 저장
  const loginSuccess = ({ access, user: userData }) => {
    accessToken.value = access
    user.value = userData
    profileImage.value = userData?.profile?.profileImage || null

    localStorage.setItem('auth', JSON.stringify({
      accessToken: access,
      user: userData,
      profileImage: userData?.profile?.profileImage || null
    }))
  }

  // 로그아웃 처리 (백엔드에 로그아웃 요청 시 함께 사용 가능)
  const logout = async () => {
    try {
      // 서버에 refresh_token 쿠키 제거 요청
      await axios.post(`${import.meta.env.VITE_BACKEND_URL}/accounts/auth/logout/`, {}, {
        withCredentials: true
      })
    } catch (e) {
      console.warn('서버 로그아웃 실패:', e)
    }
  
    // 클라이언트 상태 초기화
    accessToken.value = null
    user.value = null
    profileImage.value = null
    localStorage.removeItem('auth')
  }

  return {
    accessToken,
    user,
    profileImage,
    isAuthenticated,
    initAuth,
    loginSuccess,
    logout
  }
})
