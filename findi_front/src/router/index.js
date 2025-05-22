import { createRouter, createWebHistory } from 'vue-router'

// Views
import HomeView from '@/views/HomeView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import OAuthCallback from '@/views/OAuthCallback.vue'
import ResetPassword from '@/views/ResetPassword.vue'
import Recommend from '@/views/Recommend.vue'
import Logout from '@/components/Logout.vue'
import VideoSearchView from '@/views/VideoSearchView.vue'
import VideoDetailView from '@/views/VideoDetailView.vue'

// 인증 없이 접근 가능한 라우트
const publicRoutes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { public: true }
  },
  {
    path: '/login',
    name: 'login',
    component: LogInView,
    meta: { public: true }
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignUpView,
    meta: { public: true }
  },
  {
    path: '/oauth/callback',
    name: 'OAuthCallback',
    component: OAuthCallback,
    meta: { public: true } // 이건 로그인 없이 리디렉션 받아야 하므로 public 처리
  },
  // 동영상 주식 정보 검색
    {
    path: '/videosearch',
    name: 'videosearch',
    component: VideoSearchView,
    meta: { public: true } // 이건 로그인 없이 리디렉션 받아야 하므로 public 처리
  },
  // 동영상 디테일
  {
    path: '/video/:videoId',
    name: 'videodetail',
    component: VideoDetailView,
    meta: { public: true }
  },
  {
    path: '/password-reset',
    name: 'password-reset',
    component: ResetPassword,
    meta: { public: true }
  },

]

// 로그인한 사용자만 접근 가능한 라우트
const protectedRoutes = [
  {
    path: '/logout',
    name: 'logout',
    component: Logout,
    meta: { requiresAuth: true },
  },
  // 맞춤 상품 조회
  {
    path: '/recommend',
    name: 'recommend',
    component: Recommend,
    meta: { requiresAuth: true },
  },
  // {
  //   path: '/profile',
  //   name: 'profile',
  //   component: () => import('@/views/ProfileView.vue'),
  //   meta: { requiresAuth: true },
  // },
  // {
  //   path: '/edit-profile',
  //   name: 'edit-profile',
  //   component: () => import('@/views/EditProfileView.vue'),
  //   meta: { requiresAuth: true },
  // },
  //   {
  //   path: '/calendar',
  //   name: 'calendar',
  //   component: CalendarView,
  //   meta: { requiresAuth: true },
  // }
]

// 전체 라우트 합치기
const routes = [...publicRoutes, ...protectedRoutes]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// 전역 라우터 가드
router.beforeEach((to, from, next) => {
  const accessToken = localStorage.getItem('access_token')

  // meta.public이 true면 무조건 허용
  if (to.meta.public) {
    return next()
  }

  // 그 외는 토큰이 없으면 로그인으로 리다이렉트
  if (!accessToken) {
    return next({ name: 'login' })
  }

  return next()
})

export default router