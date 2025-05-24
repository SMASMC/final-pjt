import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref(null)
  const refreshToken = ref(null)
  const user = ref(null)
  const profileImage = ref(null)
  const isAuthenticated = computed(() => !!accessToken.value)
  // 앱 시작 시 localStorage에서 복구
  const initAuth = () => {
    const saved = JSON.parse(localStorage.getItem('auth'))
    if (saved) {
      accessToken.value = saved.accessToken
      refreshToken.value = saved.refreshToken
      user.value = saved.user
    }
  }
  const loginSuccess = ({ access, refresh, user: userData }) => {
    accessToken.value = access
    refreshToken.value = refresh
    user.value = userData
    profileImage.value = userData?.profile?.profileImage || null 
  }

  const logout = () => {
    accessToken.value = null
    refreshToken.value = null
    user.value = null
    profileImage.value = null
    localStorage.removeItem('auth') // auth 키 직접 삭제
  }

  return {
    accessToken,
    refreshToken,
    user,
    profileImage,
    isAuthenticated,
    loginSuccess,
    logout,
    initAuth
  }
}, {
  persist: {
    storage: localStorage,
    paths: ['accessToken', 'refreshToken', 'user', 'profileImage']
  }
})
