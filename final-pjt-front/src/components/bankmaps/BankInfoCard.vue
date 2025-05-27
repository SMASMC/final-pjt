<!-- src/components/BankInfoCard.vue -->
<template>
  <div class="absolute bottom-4 left-4 bg-white border border-gray-300 shadow-lg p-6 rounded-xl w-1/2 z-10">
    <h3 class="text-lg font-semibold text-purple-800 mb-3">
      {{ place.place_name }}
    </h3>
    <p class="text-sm text-gray-600 mb-1">
      {{ place.road_address_name || place.address_name }}
    </p>
    <a
      class="block mt-3 text-sm text-purple-600 hover:underline"
      :href="place.place_url"
      target="_blank"
    >
      자세히 보기 →
    </a>
  </div>
</template>

<script setup>
defineProps({
  place: Object,
})
</script>
