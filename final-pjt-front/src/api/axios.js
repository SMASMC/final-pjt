// src/api/axios.js
import axios from 'axios'
import router from '@/router'
import { isTokenExpired } from '@/utils/jwt'
import { useAuthStore } from '@/stores/auth'

const api = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_URL,
  withCredentials: true // 쿠키 자동 포함
})

// Content-Type 기본 설정
api.defaults.headers.common['Content-Type'] = 'application/json'

// 요청 인터셉터
api.interceptors.request.use(
  async (config) => {
    const authStore = useAuthStore()
    let access = authStore.accessToken

    // access_token 만료 시 -> 쿠키로 refresh 요청
    if (access && isTokenExpired(access)) {
      try {
        const res = await axios.post(
          `${import.meta.env.VITE_BACKEND_URL}/accounts/auth/refresh/`,
          {},
          { withCredentials: true }
        )
        const newAccess = res.data.access_token

        authStore.loginSuccess({
          access: newAccess,
          user: authStore.user
        })

        access = newAccess
      } catch (err) {
        authStore.logout()
        router.replace({ name: 'login' })
        return Promise.reject(err)
      }
    }

    if (access) {
      config.headers.Authorization = `Bearer ${access}`
    }

    return config
  },
  (error) => Promise.reject(error)
)

// 응답 인터셉터
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const authStore = useAuthStore()
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const res = await axios.post(
          `${import.meta.env.VITE_BACKEND_URL}/accounts/auth/refresh/`,
          {},
          { withCredentials: true }
        )

        const newAccess = res.data.access_token

        authStore.loginSuccess({
          access: newAccess,
          user: authStore.user
        })

        originalRequest.headers.Authorization = `Bearer ${newAccess}`
        return api(originalRequest)
      } catch (refreshError) {
        authStore.logout()
        router.replace({ name: 'login' })
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export default api


/*
📌 사용 예시

 GET 요청 (사용자 정보 가져오기)
await api.get('/users/1')

 POST 요청 (게시글 생성)
await api.post('/posts/', {
  title: '새 글 제목',
  content: '본문 내용',
})

 PUT 요청 (게시글 수정)
await api.put('/posts/1/', {
  title: '수정된 제목',
  content: '수정된 내용',
})

 DELETE 요청 (게시글 삭제)
await api.delete('/posts/1/')

 인증 토큰 자동 갱신 포함
- access_token이 만료되면 refresh_token으로 자동 갱신 후 요청 재시도됨
- 실패 시 localStorage 비우고 로그인 페이지로 이동
*/
