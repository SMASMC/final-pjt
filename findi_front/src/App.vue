<template>
  <!-- Intro Overlay -->
  <div v-if="showIntro" class="fixed inset-0 z-[9999] overflow-hidden">
    <!-- 첫 번째 전체 배경색 (가장 밑바닥) -->
    <div class="absolute inset-0" :style="{ backgroundColor: colors[0], zIndex: 1 }"></div>

    <!-- 나머지 색상들이 아래에서 올라오며 첫 레이어를 덮음 -->
    <div
      v-for="(color, index) in colors.slice(0)"
      :key="index"
      class="absolute w-full h-full animate-slideUpLayer"
      :style="{
        backgroundColor: color,
        animationDelay: `${index * 0.3}s`,
        zIndex: index + 2
      }"
    ></div>
  </div>
  <!-- Main Content -->
  <div class="min-h-screen bg-[#f5f3f7]">
    <NavBar v-if="!hideNav.includes(route.path)" />
    <RouterView />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import { useRoute } from 'vue-router'
import { ref, onMounted } from 'vue'

const route = useRoute()

// 로그인/회원가입 페이지에서는 NavBar 숨김
const hideNav = ['/login', '/signup']

// Intro Overlay
const showIntro = ref(true)

// Intro Overlay Colors
// 색상 배열: 첫 색상은 초기 화면 전체를 덮음
const colors = ['#CBADF7', '#9BAA59', '#FFDECE', '#BDE4F6', '#A9FFF2', '#CBADF7']

onMounted(() => {
  // 전체 애니메이션 시간 고려 후 제거 (0.3s * 4개 + 여유 시간)
  setTimeout(
    () => {
      showIntro.value = false
    },
    colors.length * 300 + 1000
  )
})
</script>

<style>
@keyframes slideUpLayer {
  0% {
    transform: translateY(100%);
  }
  100% {
    transform: translateY(0%);
  }
}
.animate-slideUpLayer {
  animation: slideUpLayer 1s ease-in-out forwards;
}
</style>
