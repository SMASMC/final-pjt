<!-- src/components/products/ProductModal.vue -->

<template>
  <div class="fixed inset-0 flex justify-center items-center z-50">
    <div class="bg-white p-6 rounded-lg shadow-lg w-[400px] border border-gray-300">
      <h3 class="text-xl font-semibold mb-4">{{ product.fin_prdt_nm }}</h3>
      <p><strong>은행:</strong> {{ product.kor_co_nm }}</p>
      <p><strong>기간:</strong> {{ product.save_trm }}개월</p>
      <p><strong>기본 금리:</strong> {{ product.intr_rate ? product.intr_rate + '%' : '-' }}</p>
      <p><strong>우대 금리:</strong> {{ product.intr_rate2 ? product.intr_rate2 + '%' : '-' }}</p>
      <p class="mt-2 whitespace-pre-line"><strong>우대조건:</strong> {{ product.spcl_cnd }}</p>
      <div class="flex justify-end mt-4">
        <button class="px-4 py-1 bg-purple-500 text-white rounded hover:bg-purple-600" @click="$emit('close')">닫기</button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  product: Object
})
</script>
