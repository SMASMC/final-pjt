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
      <div class="button-group">
        <button class="btn-signup font-bmjua" @click="goToSignup">회원 가입</button>
        <button class="btn-login font-bmjua" @click="goToLogin">로그인</button>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goToLogin = () => router.push('/login')
const goToSignup = () => router.push('/signup')

const menuItems = [
  { label: 'HOME', to: '/' },
  { label: '은행 찾기', to: '/banks' },
  { label: '예/적금 상품 조회', to: '/products' },
  { label: '달력으로 일정 조회', to: '/calendar' },
  { label: '맞춤 상품 조회', to: '/recommend' }
]
</script>

<style src="@/styles/navbar.css"></style>
