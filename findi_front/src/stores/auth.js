import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref(null)
  const refreshToken = ref(null)
  const user = ref(null)

  const isAuthenticated = computed(() => !!accessToken.value)

  const loginSuccess = ({ access, refresh, user: userData }) => {
    accessToken.value = access
    refreshToken.value = refresh
    user.value = userData
  }

  const logout = () => {
    accessToken.value = null
    refreshToken.value = null
    user.value = null
    localStorage.removeItem('auth') // auth 키 직접 삭제
  }

  return {
    accessToken,
    refreshToken,
    user,
    isAuthenticated,
    loginSuccess,
    logout
  }
}, {
  persist: {
    storage: localStorage,
    paths: ['accessToken', 'refreshToken', 'user']
  }
})
