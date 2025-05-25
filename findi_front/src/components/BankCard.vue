<!-- BankCard.vue 수정 필요 -->
<template>
  <div class="p-4 pt-20">
    <div class="scene">
      <div class="card">
        <img :src="logo" :alt="name" class="h-16 object-contain" />
      </div>

      <div class="card-back">
        <span class="font-bold">{{ name }}</span>
        <div v-if="hasProfile && products.length">
          <ul class="text-sm mt-2 text-black text-left">
            <li v-for="(item, index) in products" :key="index">
              • {{ item.productName || '상품명 없음' }} ({{ item.interestRate }}%)
            </li>
          </ul>
        </div>
        <div v-else-if="hasProfile">
          <p class="text-xs">아직 추천 항목이 없습니다.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  logo: String,
  name: String,
  hasProfile: Boolean,
  products: Array
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
  background: linear-gradient(135deg, #4b6cb7, #182848);
  transform-origin: bottom center;
  z-index: 2;
  transform: rotateX(0deg);
}

.scene:hover .card {
  transform: rotateX(90deg);
  z-index: 1;
}

.card-back {
  background: linear-gradient(135deg, #f7971e, #ffd200);
  transform: rotateX(0deg);
  z-index: 0;
  flex-direction: column;
  padding: 1rem;
}
</style>
