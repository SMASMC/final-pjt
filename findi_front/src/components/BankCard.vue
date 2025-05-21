<template>
  <div class="scene">
    <!-- 앞면 -->
    <div class="card">
      <img :src="logo" :alt="name" class="h-16 object-contain" />
    </div>

    <!-- 뒷면 -->
    <div class="card-back">
      <span>{{ name }}</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  logo: String,
  name: String
})
</script>

<style scoped>
.scene {
  width: 500px;
  height: 300px;
  perspective: 1000px;
  position: relative;
}

.card,
.card-back {
  position: absolute;
  top: 100px;
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
}
</style>
