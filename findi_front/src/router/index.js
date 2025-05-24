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
import { useAuthStore } from '@/stores/auth'
import ArticleView from '@/views/articles/ArticleView.vue'
import ArticleDetailView from '@/views/articles/ArticleDetailView.vue'
import ProfileView from '@/views/ProfileView.vue'

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
  // 게시판
  {
    path: '/articles',
    name: 'articles',
    component: ArticleView,
    meta: { public: true }
  },
  {
    path: '/articles/:id',
    name: 'articlesdetail',
    component: ArticleDetailView,
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
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView,
    meta: { requiresAuth: true },
  },
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
  const authStore = useAuthStore()
  const accessToken = authStore.accessToken
  const rawAuth = localStorage.getItem('auth')

  let isLoggedIn = false

  if (accessToken) {
    isLoggedIn = true
  } else if (rawAuth) {
    try {
      const auth = JSON.parse(rawAuth)

      // 내부 키들이 모두 존재하는지 확인
      const hasValidAuth = auth.accessToken && auth.refreshToken && auth.user
      isLoggedIn = !!hasValidAuth
    } catch (e) {
      console.warn('localStorage auth 파싱 실패:', e)
      isLoggedIn = false
    }
  }

  // 로그인된 사용자가 login/signup 페이지 접근 시 홈으로 이동
  if ((to.name === 'login' || to.name === 'signup') && isLoggedIn) {
    return next({ name: 'home' })
  }

  // 공개 라우트는 항상 허용
  if (to.meta.public) {
    return next()
  }

  // 보호 라우트는 로그인되어야 허용
  if (!isLoggedIn) {
    return next({ name: 'login' })
  }

  return next()
})


export default router