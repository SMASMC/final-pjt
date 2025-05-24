<template>
  <div
    v-if="visible"
    class="fixed top-4 left-4 z-50 flex items-center w-full max-w-xs p-4 mb-4 text-sm text-gray-700 bg-white border border-gray-200 rounded-lg shadow-lg"
    role="alert"
  >
    <div
      :class="iconClass"
      class="inline-flex items-center justify-center shrink-0 w-8 h-8 rounded-lg"
    >
      <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
        <path :d="iconPath" />
      </svg>
    </div>
    <div class="ms-3 text-sm font-normal" v-html="message"></div>
  </div>
</template>

<script setup>
import { ref, watchEffect } from 'vue'

const props = defineProps({
  type: { type: String, default: 'success' },
  message: { type: String, required: true }
})

const visible = ref(true)

watchEffect(() => {
  setTimeout(() => {
    visible.value = false
  }, 3000)
})

const iconClass =
  {
    success: 'text-green-500 bg-green-100',
    danger: 'text-red-500 bg-red-100',
    warning: 'text-orange-500 bg-orange-100'
  }[props.type] || 'text-gray-500 bg-gray-100'

const iconPath =
  {
    success:
      'M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z',
    danger:
      'M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 11.793a1 1 0 1 1-1.414 1.414L10 11.414l-2.293 2.293a1 1 0 0 1-1.414-1.414L8.586 10 6.293 7.707a1 1 0 0 1 1.414-1.414L10 8.586l2.293-2.293a1 1 0 0 1 1.414 1.414L11.414 10l2.293 2.293Z',
    warning:
      'M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM10 15a1 1 0 1 1 0-2 1 1 0 0 1 0 2Zm1-4a1 1 0 0 1-2 0V6a1 1 0 0 1 2 0v5Z'
  }[props.type] || ''
</script>
