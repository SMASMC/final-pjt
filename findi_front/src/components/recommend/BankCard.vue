<template>
  <div class="p-4 pt-20 relative">
    <div class="scene" @mouseenter="hover = true" @mouseleave="hover = false">
      <!-- 앞면 카드 -->
      <div class="card">
        <img :src="logo" :alt="name" class="h-16 object-contain" />
      </div>

      <!-- 뒷면 카드 -->
      <div class="card-back" :style="{ background: cardBackGradient }">
        <span class="font-bold">{{ name }}</span>
        <div v-if="hasProfile && products.length">
          <ul class="text-sm mt-2 text-black text-left relative">
            <li v-for="(item, index) in visibleProducts" :key="index">
              • {{ item.productName || '상품명 없음' }}
              <span v-if="item.interestRate">({{ item.interestRate }}%)</span>
              <span v-else class="text-gray-400">(금리 정보 없음)</span>
            </li>

            <!-- 초과 상품 팝오버 트리거 -->
            <li
              v-if="hover && extraCount > 0"
              class="text-xs font-bold text-white mt-1 cursor-pointer underline relative"
              @mouseenter="setPopover(true)"
              @mouseleave="setPopover(false)"
              ref="popoverTrigger"
            >
              +{{ extraCount }}개 상품 더 있음
            </li>
          </ul>
        </div>

        <div v-else-if="hasProfile">
          <p class="text-xs">아직 추천 항목이 없습니다.</p>
        </div>
      </div>
    </div>

    <!-- 팝오버 -->
    <div
      v-if="popoverVisible"
      :style="popoverStyle"
      class="fixed bg-white text-black text-xs rounded-lg shadow-xl z-[9999] w-72 p-4 max-h-[300px] overflow-y-auto transition-all"
      @mouseenter="setPopover(true)"
      @mouseleave="setPopover(false)"
    >
      <p class="font-semibold mb-2">{{ name }}의 전체 상품</p>
      <ul class="list-disc list-inside space-y-1">
        <li v-for="(item, idx) in products" :key="idx">
          {{ item.productName || '상품명 없음' }}
          <span v-if="item.interestRate">({{ item.interestRate }}%)</span>
          <span v-else class="text-gray-400">(금리 없음)</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'

const props = defineProps({
  logo: String,
  name: String,
  hasProfile: Boolean,
  products: Array,
  cardBackGradient: String
})

const hover = ref(false)
const popoverVisible = ref(false)
const popoverTrigger = ref(null)
const popoverStyle = ref({})
const popoverTimer = ref(null)

const visibleProducts = computed(() => props.products.slice(0, 3))
const extraCount = computed(() => props.products.length - 3)

// 마우스 진입 유지 제어
const setPopover = (val) => {
  clearTimeout(popoverTimer.value)
  if (val) {
    popoverVisible.value = true
  } else {
    // 마우스가 잠깐 벗어날 경우 닫힘 딜레이
    popoverTimer.value = setTimeout(() => {
      popoverVisible.value = false
    }, 300)
  }
}

// 팝오버 위치 계산
watch(popoverVisible, async (visible) => {
  if (visible) {
    await nextTick()
    const rect = popoverTrigger.value?.getBoundingClientRect()
    if (rect) {
      popoverStyle.value = {
        top: `${rect.bottom + 8}px`,
        left: `${rect.left + rect.width / 2}px`,
        transform: 'translateX(-50%)'
      }
    }
  }
})
</script>

<style scoped>
.scene {
  width: 100%;
  height: 240px;
  perspective: 1000px;
  position: relative;
}

.card,
.card-back {
  position: absolute;
  top: 0;
  width: 100%;
  height: 100%;
  border-radius: 12px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: sans-serif;
  font-size: 1.5rem;
  color: white;
  backface-visibility: hidden;
  transition: transform 0.6s ease;
}

.card {
  background: rgba(255, 255, 255, 1);
  transform-origin: bottom center;
  z-index: 2;
  transform: rotateX(0deg);
  pointer-events: none;
}

.scene:hover .card {
  transform: rotateX(90deg);
  z-index: 1;
}

.card-back {
  transform: rotateX(0deg);
  z-index: 0;
  flex-direction: column;
  padding: 1rem;
}
</style>
