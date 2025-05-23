import { defineStore } from 'pinia'

// Auth Store 선언 login, logout, loadFromLocalStorage
export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: localStorage.getItem('access_token'),
    refreshToken: localStorage.getItem('refresh_token'),
    user: JSON.parse(localStorage.getItem('user') || 'null')
  }),
      getters: {
    //  accessToken 유무로 로그인 상태 판단
    isAuthenticated: (state) => !!state.accessToken
  },

  actions: {
    // 로그인 성공시
    loginSuccess({ access, refresh, user }) {
      this.accessToken = access
      this.refreshToken = refresh
      this.user = user

      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', refresh)
      localStorage.setItem('user', JSON.stringify(user))
    },
    // 로그아웃
    logout() {
      this.accessToken = null
      this.refreshToken = null
      this.user = null
      localStorage.clear()
    },
    // 로컬스토리지에서 로그인 정보 로드
    // 보통 앱 시작 시점에서 새로고침으로 인한 로그인 정보 초기화를 방지하기 위해 사용
    loadFromLocalStorage() {
      this.accessToken = localStorage.getItem('access_token')
      this.refreshToken = localStorage.getItem('refresh_token')
      this.user = JSON.parse(localStorage.getItem('user') || 'null')
    }
  }
})
