<template>
  <section
    ref="section1"
    class="min-h-screen flex flex-col items-center justify-center text-center px-6 py-20 bg-gradient-to-b from-white to-[#d4b7ff] relative"
  >
    <!-- 타이틀 -->
    <transition v-show="showMainContent" name="slide-fade-down" appear>
      <div class="mb-12">
        <h1 class="text-4xl md:text-5xl font-bold leading-snug">
          <span class="text-[#302770] font-bmjua">금융 상품의 모든 것,</span><br />
          <span class="text-[#8A69E1] font-symbol">Findi</span> <span class="font-bmjua">에서</span
          ><br />
          <span class="font-bmjua">쉽고 간편하게</span>
        </h1>
      </div>
    </transition>
    <!-- 일러스트 영역 -->
    <transition v-show="showMainContent" name="fade" appear>
      <div class="flex flex-col md:flex-row items-center justify-center gap-12 mt-10">
        <img
          src="@/assets/main_page/bank_illustration.png"
          alt="은행 이미지"
          class="w-56 md:w-72"
        />
        <img
          src="@/assets/main_page/dog_illustration.png"
          alt="강아지 이미지"
          class="w-52 md:w-64"
        />
      </div>
    </transition>
    <!-- 안내 텍스트 -->
    <transition v-show="showMainContent" name="fade" appear>
      <div
        class="absolute bottom-20 font-bold text-gray-500 text-xl text-center w-full animate-bounce cursor-pointer"
        @click="scrollToSection(1)"
      >
        Findi의 기능들을 함께 둘러보세요
      </div>
    </transition>
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
    class="min-h-screen bg-gradient-to-b from-[#ffffff] to-[#d7e599] flex flex-col md:flex-row items-center justify-center gap-10 md:gap-80 relative"
  >
    <!-- 왼쪽 텍스트 및 버튼 -->
    <transition name="fade-slide">
      <div
        v-if="sectionAnimations[1]"
        class="text-center md:text-left items-center font-bmjua flex flex-col"
      >
        <h2 class="text-2xl md:text-4xl font-normal mb-6 font-bmjua text-center">
          상품과 은행을<br />주변에서 찾아보세요
        </h2>
        <button
          class="bg-[#9BAA59] text-white px-6 py-3 rounded-full font-normal text-base cursor-pointer hover:bg-[#8a9959] transition duration-200"
          @click="goToBanks"
        >
          지도로 찾기
        </button>
      </div>
    </transition>
    <!-- 오른쪽 이미지 -->
    <transition name="fade-slide">
      <img
        v-if="sectionAnimations[1]"
        src="@/assets/main_page/mapicon.png"
        alt="지도"
        class="w-[400px] mt-12"
      />
    </transition>

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
    class="min-h-screen bg-gradient-to-b from-[#ffffff] to-[#ffcdb4] flex flex-col md:flex-row items-center justify-center gap-10 md:gap-80 relative"
  >
    <!-- 왼쪽 이미지 -->
    <transition name="fade-slide">
      <img
        v-if="sectionAnimations[2]"
        src="@/assets/main_page/piggy.png"
        alt="피그"
        class="w-[400px] mt-12"
      />
    </transition>

    <!-- 오른쪽 텍스트 및 버튼 -->
    <transition name="fade-slide">
      <div v-if="sectionAnimations[2]" class="text-center md:text-left items-center flex flex-col">
        <h2 class="text-2xl md:text-4xl font-normal mb-6 font-bmjua text-center">
          다양한 예적금 상품을<br />조회해보세요
        </h2>
        <button
          class="bg-[#D9876C] text-white px-6 py-3 rounded-full font-normal text-base cursor-pointer hover:bg-[#c2725c] transition duration-200"
          @click="goToProducts"
        >
          금융 상품 조회
        </button>
      </div>
    </transition>
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
  <!-- Section 4: 주식정보 영상 -->
  <section
    ref="section4"
    class="min-h-screen bg-gradient-to-b from-[#ffffff] to-[#FFB2B3] flex flex-col md:flex-row items-center justify-center gap-10 md:gap-80 relative"
  >
    <!-- 왼쪽 텍스트 및 버튼 -->
    <transition name="fade-slide">
      <div v-if="sectionAnimations[3]" class="text-center md:text-left items-center flex flex-col">
        <h2 class="text-2xl md:text-4xl font-normal mb-6 font-bmjua text-center">
          주식 정보를 영상으로<br />확인 후 저장하세요
        </h2>
        <button
          class="bg-[#DB766C] text-white px-6 py-3 rounded-full font-normal text-base cursor-pointer hover:bg-[#FF5C8A] transition duration-200"
          @click="goToVideos"
        >
          주식 정보 영상 보기
        </button>
      </div>
    </transition>
    <!-- 오른쪽 이미지 -->
    <transition name="fade-slide">
      <img
        v-if="sectionAnimations[3]"
        src="@/assets/main_page/video_icon.png"
        alt="스케줄"
        class="w-[300px] md:w-[400px]"
      />
    </transition>

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

  <!-- Section 5: 게시판 -->
  <section
    ref="section5"
    class="min-h-screen bg-gradient-to-b from-[#ffffff] to-[#FDB676] flex flex-col md:flex-row items-center justify-center gap-10 md:gap-80 relative"
  >
    <!-- 왼쪽 이미지 -->
    <transition name="fade-slide">
      <img
        v-if="sectionAnimations[4]"
        src="@/assets/main_page/board.png"
        alt="게시판"
        class="w-[400px] mt-12"
      />
    </transition>

    <!-- 오른쪽 텍스트 및 버튼 -->
    <transition name="fade-slide">
      <div v-if="sectionAnimations[4]" class="text-center md:text-left items-center flex flex-col">
        <h2 class="text-2xl md:text-4xl font-normal mb-6 font-bmjua text-center">
          사용자들과 게시판에서<br />의사소통하세요
        </h2>
        <button
          class="bg-[#CE6910] text-white px-6 py-3 rounded-full font-normal text-base cursor-pointer hover:bg-[#c2725c] transition duration-200"
          @click="goToarticles"
        >
          게시판 가기
        </button>
      </div>
    </transition>
    <!-- 스크롤 유도 아이콘 -->
    <div class="absolute bottom-8 animate-bounce cursor-pointer" @click="scrollToSection(5)">
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

  <!-- Section 6: 현물 -->
  <section
    ref="section6"
    class="min-h-screen bg-gradient-to-b from-[#ffffff] to-[#FBE398] flex flex-col md:flex-row items-center justify-center gap-10 md:gap-80 relative"
  >
    <!-- 왼쪽 텍스트 및 버튼 -->
    <transition name="fade-slide">
      <div v-if="sectionAnimations[5]" class="text-center md:text-left items-center flex flex-col">
        <h2 class="text-2xl md:text-4xl font-normal mb-6 font-bmjua text-center">
          현물 상품의 가격을<br />알아보세요
        </h2>
        <button
          class="bg-[#CE8510] text-white px-6 py-3 rounded-full font-normal text-base cursor-pointer hover:bg-[#CE6910] transition duration-200"
          @click="goTocommodities"
        >
          현물 가격 조회
        </button>
      </div>
    </transition>
    <!-- 오른쪽 이미지 -->
    <transition name="fade-slide">
      <img
        v-if="sectionAnimations[5]"
        src="@/assets/main_page/gold.png"
        alt="금고"
        class="w-[300px] md:w-[400px]"
      />
    </transition>

    <!-- 스크롤 유도 아이콘 -->
    <div class="absolute bottom-8 animate-bounce cursor-pointer" @click="scrollToSection(6)">
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

  <!-- Section 7: 5대 은행 맞춤상품 조회 -->
  <section
    ref="section7"
    class="min-h-screen bg-gradient-to-b from-[#ffffff] to-[#c6fff6] flex flex-col md:flex-row items-center justify-center gap-10 md:gap-80"
  >
    <!-- 왼쪽: 회전하는 로고 -->
    <transition name="fade-slide">
      <div v-if="sectionAnimations[6]" class="w-[300px] h-[300px] relative perspective-1000">
        <div class="bank_logos-rotator">
          <img
            v-for="(bank_logo, index) in bank_logos"
            :key="index"
            :src="bank_logo"
            class="bank_logos-img"
          />
        </div>
      </div>
    </transition>

    <!-- 오른쪽 텍스트 및 버튼 -->
    <transition name="fade-slide">
      <div v-if="sectionAnimations[6]" class="text-center md:text-left items-center flex flex-col">
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
    </transition>
  </section>

  <!-- Floating ChatBot -->
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'

// 챗봇이 열려있는지 확인
const isChatbotOpen = () => {
  return !!document.querySelector('.chat-box')
}

const router = useRouter()

// Section refs
const section1 = ref(null)
const section2 = ref(null)
const section3 = ref(null)
const section4 = ref(null)
const section5 = ref(null)
const section6 = ref(null)
const section7 = ref(null)

const sectionRefs = [section1, section2, section3, section4, section5, section6, section7]
const currentSection = ref(0)

// 각 섹션의 애니메이션 상태
const sectionAnimations = ref([false, false, false, false, false, false, false])

// 스크롤로 섹션 이동
const scrollToSection = (num) => {
  if (num >= 0 && num < sectionRefs.length) {
    sectionRefs[num]?.value?.scrollIntoView({ behavior: 'smooth' })
    currentSection.value = num
  }
}

// 페이지 이동용 버튼
const goToBanks = () => router.push('/bankmaps')
const goToProducts = () => router.push('/products')
const goToVideos = () => router.push('/videosearch')
const goToarticles = () => router.push('/articles')
const goTocommodities = () => router.push('/commodities')
const goToRecommend = () => router.push('/recommend')

// 인트로 효과
const showMainContent = ref(false)
const showIntro = ref(true)
const colors = ['#8A69E1', '#CBADF7', '#F6FBEA', '#CBADF7', '#8A69E1']

// 휠 스크롤 이벤트 처리
let scrollTimeout = null
const handleWheel = (event) => {
  if (isChatbotOpen()) return
  if (scrollTimeout) return

  scrollTimeout = setTimeout(() => {
    scrollTimeout = null
  }, 800)

  const delta = event.deltaY
  if (delta > 0 && currentSection.value < sectionRefs.length - 1) {
    scrollToSection(currentSection.value + 1)
  } else if (delta < 0 && currentSection.value > 0) {
    scrollToSection(currentSection.value - 1)
  }
}

// 클릭 위치 기반 스크롤 이동
const handleClickPosition = (event) => {
  if (isChatbotOpen()) return
  // 클릭한 요소가 버튼 또는 버튼 내부일 경우 무시
  const tag = event.target.tagName.toLowerCase()
  if (tag === 'button' || event.target.closest('button')) return

  const screenHeight = window.innerHeight
  const clickY = event.clientY

  if (clickY < screenHeight / 2 && currentSection.value > 0) {
    scrollToSection(currentSection.value - 1)
  } else if (clickY >= screenHeight / 2 && currentSection.value < sectionRefs.length - 1) {
    scrollToSection(currentSection.value + 1)
  }
}

onMounted(() => {
  // 인트로 애니메이션 시작
  setTimeout(
    () => {
      showIntro.value = false
      setTimeout(() => {
        showMainContent.value = true
      }, 1000)
    },
    colors.length * 300 + 1000
  )
  // 섹션 애니메이션 트리거
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const index = sectionRefs.findIndex((ref) => ref.value === entry.target)
          if (index !== -1) {
            sectionAnimations.value[index] = true
          }
        }
      })
    },
    { threshold: 0.6 }
  )
  sectionRefs.forEach((section) => {
    if (section.value) observer.observe(section.value)
  })
  // 휠 스크롤 + 클릭 위치 기반 추가
  window.addEventListener('wheel', handleWheel)
  window.addEventListener('mousedown', handleClickPosition)
})

onBeforeUnmount(() => {
  window.removeEventListener('wheel', handleWheel)
  window.removeEventListener('mousedown', handleClickPosition)
})

// 은행 회전로고 경로

const bank_logos = [
  new URL('@/assets/banks_mainlogo/sinhan3d.png', import.meta.url).href,
  new URL('@/assets/banks_mainlogo/kb3d.png', import.meta.url).href,
  new URL('@/assets/banks_mainlogo/hana3d.png', import.meta.url).href,
  new URL('@/assets/banks_mainlogo/woori3d.png', import.meta.url).href,
  new URL('@/assets/banks_mainlogo/nh3d.png', import.meta.url).href
]
</script>

<style>
/* 기존 fade 애니메이션 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 1s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.fade-enter-to,
.fade-leave-from {
  opacity: 1;
}

/* slide-fade-down: 위에서 아래로 내려오며 페이드인 */
.slide-fade-down-enter-active {
  transition: all 1s ease;
}

.slide-fade-down-enter-from {
  opacity: 0;
  transform: translateY(-30px);
}

.slide-fade-down-enter-to {
  opacity: 1;
  transform: translateY(0);
}

/* slide-fade-up: 슬라이드 + 페이드인 */
.fade-slide-enter-active {
  transition: all 0.8s ease;
  transition-delay: 0.8s;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(30px);
}

.fade-slide-enter-to {
  opacity: 1;
  transform: translateY(0);
}

/* 로고 회전 애니메이션 */
.perspective-1000 {
  perspective: 1000px;
}

.bank_logos-rotator {
  width: 100%;
  height: 100%;
  position: relative;
  transform-style: preserve-3d;
  animation: rotateY 12s linear infinite;
}

/* 로고 애니메이션 */
.bank_logos-img {
  position: absolute;
  width: 175px;
  height: 150px;
  object-fit: contain;
  top: 75px;
  /* 부모 높이에서 중앙 배치 */
  left: 75px;
  transform-origin: center center;
}

.bank_logos-img:nth-child(1) {
  transform: rotateY(0deg) translateZ(250px);
}

.bank_logos-img:nth-child(2) {
  transform: rotateY(72deg) translateZ(250px);
}

.bank_logos-img:nth-child(3) {
  transform: rotateY(144deg) translateZ(250px);
}

.bank_logos-img:nth-child(4) {
  transform: rotateY(216deg) translateZ(250px);
}

.bank_logos-img:nth-child(5) {
  transform: rotateY(288deg) translateZ(250px);
}

.bank_logos-img:nth-child(1) {
  animation-delay: 0s;
}

.bank_logos-img:nth-child(2) {
  animation-delay: 2.4s;
}

.bank_logos-img:nth-child(3) {
  animation-delay: 4.8s;
}

.bank_logos-img:nth-child(4) {
  animation-delay: 7.2s;
}

.bank_logos-img:nth-child(5) {
  animation-delay: 9.6s;
}

.bank_logos-rotator {
  width: 100%;
  height: 100%;
  position: relative;
  transform-style: preserve-3d;
  animation: rotateY 15s linear infinite;
}

@keyframes rotateY {
  from {
    transform: rotateY(0deg);
  }

  to {
    transform: rotateY(360deg);
  }
}
</style>
