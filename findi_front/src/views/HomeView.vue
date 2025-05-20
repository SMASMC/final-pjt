<template>
  <section
    ref="section1"
    class="min-h-screen flex flex-col items-center justify-center text-center px-6 py-20 bg-gradient-to-b from-white via-[#f6fbea] to-[#CBADF7] relative"
  >
    <!-- 타이틀 -->
    <div class="mb-12">
      <h1 class="text-4xl md:text-5xl font-bold leading-snug">
        <span class="text-[#302770] font-bmjua">금융 상품의 모든 것,</span><br />
        <span class="text-[#8A69E1]">Findi</span> <span class="font-bmjua">에서</span><br />
        <span class="font-bmjua">쉽고 간편하게</span>
      </h1>
    </div>
    <!-- 일러스트 영역 -->
    <div class="flex flex-col md:flex-row items-center justify-center gap-12 mt-10">
      <img src="@/assets/main_page/bank_illustration.png" alt="은행 이미지" class="w-56 md:w-72" />
      <img src="@/assets/main_page/dog_illustration.png" alt="강아지 이미지" class="w-52 md:w-64" />
    </div>

    <!-- 스크롤 유도 아이콘 -->
    <div class="absolute bottom-8 animate-bounce cursor-pointer" @click="scrollToSection(1)">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="w-6 h-6 text-[#8A69E1]"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </div>
  </section>
  <!-- Section 2: 지도 소개 -->
  <section
    ref="section2"
    class="min-h-screen bg-gradient-to-b from-[#ffffff] via-[#f6fbea] to-[#9BAA59] flex flex-col md:flex-row items-center justify-center gap-10 md:gap-80 relative"
  >
    <!-- 왼쪽 텍스트 및 버튼 -->
    <div class="text-center md:text-left items-center flex flex-col">
      <h2 class="text-2xl md:text-3xl font-bold mb-6 font-bmjua text-center">
        상품과 은행을<br />주변에서 찾아보세요
      </h2>
      <button
        class="bg-[#9BAA59] text-white px-6 py-3 rounded-full font-semibold text-sm cursor-pointer hover:bg-[#8a9959] transition duration-200"
        @click="goToBanks"
      >
        지도로 찾기
      </button>
    </div>
    <!-- 오른쪽 이미지 -->
    <img src="@/assets/main_page/mapicon.png" alt="지도" class="w-[400px] mt-12" />

    <!-- 스크롤 유도 아이콘 -->
    <div class="absolute bottom-8 animate-bounce cursor-pointer" @click="scrollToSection(2)">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="w-6 h-6 text-[#8A69E1]"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </div>
  </section>
  <!-- Section 3: 상품 소개 -->
  <section
    ref="section3"
    class="min-h-screen bg-gradient-to-b from-[#ffffff] via-[#f6fbea] to-[#FFDECE] flex flex-col md:flex-row items-center justify-center gap-10 md:gap-80 relative"
  >
    <!-- 왼쪽 이미지 -->
    <img src="@/assets/main_page/piggy.png" alt="피그" class="w-[400px] mt-12" />

    <!-- 오른쪽 텍스트 및 버튼 -->
    <div class="text-center md:text-left items-center flex flex-col">
      <h2 class="text-2xl md:text-3xl font-bold mb-6 font-bmjua text-center">
        다양한 예적금 상품을<br />조회해보세요
      </h2>
      <button
        class="bg-[#D9876C] text-white px-6 py-3 rounded-full font-semibold text-sm cursor-pointer hover:bg-[#c2725c] transition duration-200"
        @click="goToProducts"
      >
        금융 상품 조회
      </button>
    </div>

    <!-- 스크롤 유도 아이콘 -->
    <div class="absolute bottom-8 animate-bounce cursor-pointer" @click="scrollToSection(3)">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="w-6 h-6 text-[#8A69E1]"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </div>
  </section>
  <!-- Section 4: 상품 -->
  <section
    ref="section4"
    class="min-h-screen bg-gradient-to-b from-[#ffffff] via-[#f6fbea] to-[#BDE4F6] flex flex-col md:flex-row items-center justify-center gap-10 md:gap-80 relative"
  >
    <!-- 왼쪽 텍스트 및 버튼 -->
    <div class="text-center md:text-left items-center flex flex-col">
      <h2 class="text-2xl md:text-3xl font-bold mb-6 font-bmjua text-center">
        자신만의 적금 플랜을<br />한눈에 파악해 보세요
      </h2>
      <button
        class="bg-[#486FAA] text-white px-6 py-3 rounded-full font-semibold text-sm cursor-pointer hover:bg-[#3c578a] transition duration-200"
        @click="goToCalendar"
      >
        자신만의 플랜 조회
      </button>
    </div>
    <!-- 오른쪽 이미지 -->
    <img src="@/assets/main_page/schedule.png" alt="스케줄" class="w-[300px] md:w-[400px]" />

    <!-- 스크롤 유도 아이콘 -->
    <div class="absolute bottom-8 animate-bounce cursor-pointer" @click="scrollToSection(4)">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="w-6 h-6 text-[#8A69E1]"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </div>
  </section>
  <!-- Section 5: 상품 소개 -->
  <section
    ref="section5"
    class="min-h-screen bg-gradient-to-b from-[#ffffff] via-[#f6fbea] to-[#A9FFF2] flex flex-col md:flex-row items-center justify-center gap-10 md:gap-80"
  >
    <!-- 왼쪽 이미지 -->
    <img
      src="@/assets/main_page/custom_products.png"
      alt="맞춤 상품"
      class="w-[300px] md:w-[400px]"
    />

    <!-- 오른쪽 텍스트 및 버튼 -->
    <div class="text-center md:text-left items-center flex flex-col">
      <h2 class="text-2xl md:text-3xl font-bold mb-6 font-bmjua text-center">
        당신에게 딱 맞는 상품을 조회하세요
      </h2>
      <button
        class="bg-[#00B299] text-white px-6 py-3 rounded-full font-semibold text-sm cursor-pointer hover:bg-[#009a88] transition duration-200"
        @click="goToRecommend"
      >
        맞춤 상품 조회
      </button>
    </div>
  </section>
  <!-- Floating ChatBot -->
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const section1 = ref(null)
const section2 = ref(null)
const section3 = ref(null)
const section4 = ref(null)
const section5 = ref(null)

const sectionRefs = [section1, section2, section3, section4, section5]

const scrollToSection = (num) => {
  sectionRefs[num]?.value?.scrollIntoView({ behavior: 'smooth' })
}

const goToBanks = () => {
  router.push('/banks')
}
const goToProducts = () => {
  router.push('/products')
}
const goToCalendar = () => {
  router.push('/calendar')
}
const goToRecommend = () => {
  router.push('/recommend')
}
</script>
