<!-- src/components/ConfirmModal.vue -->
<template>
  <div
    v-if="show"
    class="fixed inset-0 z-50 flex items-center justify-center backdrop-blur-sm bg-black/20"
  >
    <div class="bg-white rounded-lg shadow p-6 w-full max-w-md">
      <h3 class="text-lg font-semibold mb-2">{{ title }}</h3>
      <p class="text-sm text-gray-700 mb-4">{{ content }}</p>
      <div class="flex justify-end gap-2">
        <button
          @click="onCancel"
          class="px-4 py-2 rounded bg-gray-300 hover:bg-gray-400 cursor-pointer"
        >
          {{ cancelText }}
        </button>
        <button
          @click="onConfirm"
          class="px-4 py-2 rounded bg-red-600 text-white hover:bg-red-700 cursor-pointer"
        >
          {{ confirmText }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  show: Boolean,
  title: String,
  content: String,
  confirmText: { type: String, default: '확인' },
  cancelText: { type: String, default: '취소' }
})

const emit = defineEmits(['confirm', 'cancel'])

const onConfirm = () => emit('confirm')
const onCancel = () => emit('cancel')
</script>

<style scoped></style>
