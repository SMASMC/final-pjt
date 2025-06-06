<template>
  <header class="navbar-header">
    <nav class="navbar-container">
      <!-- 로고 -->
      <router-link to="/" class="logo-container">
        <img src="@/assets/findi_logo.png" alt="Findi Logo" class="logo-img" />
      </router-link>

      <!-- 메뉴 -->
      <ul class="menu-list font-bmjua">
        <li v-for="(item, index) in menuItems" :key="index">
          <router-link
            :to="item.to"
            class="menu-link"
            :class="
              router.currentRoute.value.path === item.to ? 'menu-link-active' : 'menu-link-inactive'
            "
          >
            {{ item.label }}
          </router-link>
        </li>
      </ul>

      <!-- 버튼 -->
      <!-- 로그인이 안 된 경우 -->
      <div v-if="!isLoggedIn" class="button-group">
        <button class="btn-signup font-bmjua cursor-pointer" @click="goToSignup">회원 가입</button>
        <button class="btn-login font-bmjua cursor-pointer" @click="goToLogin">로그인</button>
      </div>
      <!-- 로그인이 된 경우 -->
      <div v-else class="flex items-center gap-3">
        <!-- 프로필 버튼 -->
        <button
          @click="goToProfile"
          class="flex items-center bg-[#8A69E1] text-white hover:bg-[#8A69E1]/90 transition rounded-full space-x-1 pr-4 cursor-pointer"
        >
          <img :src="profileImage" alt="프로필" class="w-10 h-10 rounded-full object-cover" />
          <span class="w-full text-sm font-light font-bmjua">{{ userName }} 님</span>
        </button>

        <!-- 로그아웃 버튼 -->
        <button class="btn-logout font-bmjua cursor-pointer" @click="goToLogout">로그아웃</button>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
// 의존값이 바뀔 때마다 다시 계산 computed
import { computed } from 'vue'
import defaultProfile from '@/assets/profile.png'

const router = useRouter()
const authStore = useAuthStore()

// User 로그인 정보
const isLoggedIn = computed(() => !!authStore.accessToken)
const userName = computed(() => authStore.user?.userName || '사용자') // userName이 없으면, 사용자라고 띄움
// user객체에없으면, user.profile로 찾고, 없으면 assets/profile.png로 설정
const profileImage = computed(() => {
  const src = authStore.profileImage
  if (!src) return defaultProfile
  return src.startsWith('http') ? src : import.meta.env.VITE_BACKEND_URL + src
})

const goToLogin = () => router.push('/login')
const goToSignup = () => router.push('/signup')
// 로그아웃하고, 메인메뉴로 돌아가기
const goToLogout = () => {
  authStore.logout()
  router.replace('/')
}

const goToProfile = () => router.push('/profile')

const menuItems = [
  { label: '은행 찾기', to: '/bankmaps' },
  { label: '예/적금 상품 조회', to: '/products' },
  { label: '주식 정보 영상 조회', to: '/videosearch' },
  { label: '자유 게시판', to: '/articles' },
  { label: '금/은 가격 조회', to: '/commodities' },
  { label: '5대 금융 상품 & 맞춤 조회', to: '/recommend' }
]
</script>

<style src="@/styles/navbar.css"></style>
