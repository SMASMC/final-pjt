<script setup>
import { RouterView } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import { useRoute } from 'vue-router'

const route = useRoute()

// 로그인/회원가입 페이지에서는 NavBar 숨김
const hideNav = ['/login', '/signup']
</script>

<template>
  <div class="min-h-screen bg-[#f5f3f7]">
    <NavBar v-if="!hideNav.includes(route.path)" />
    <RouterView />
  </div>
</template>

<style>
/* 전역 스타일은 제거하고 Tailwind에 맡기는 것이 좋습니다. */
</style>
