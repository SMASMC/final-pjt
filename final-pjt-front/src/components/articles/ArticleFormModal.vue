<template>
  <div class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center">
    <div class="bg-white rounded-lg shadow-md p-6 w-full max-w-3xl relative">
      <h2 class="text-xl font-bold mb-4">게시글 작성</h2>

      <form @submit.prevent="handleSubmit">
        <label class="block mb-2 text-sm font-medium">제목</label>
        <input
          v-model="title"
          type="text"
          class="w-full border border-gray-300 rounded px-3 py-2 mb-4"
          required
        />

        <label class="block mb-2 text-sm font-medium">내용</label>
        <QuillEditor
          v-model:content="content"
          toolbar="full"
          contentType="html"
          :style="{ height: '200px' }"
        />

        <div class="mt-6 flex justify-end gap-2">
          <button
            type="button"
            @click="$emit('close')"
            class="px-4 py-2 border rounded hover:bg-gray-100 cursor-pointer"
          >
            취소
          </button>
          <button
            type="submit"
            class="px-4 py-2 bg-[#8A69E1] text-white rounded hover:bg-[#8A69E1]/90 cursor-pointer"
          >
            생성
          </button>
        </div>
      </form>
    </div>
  </div>
  <ToastMessage v-if="toast.show" :type="toast.type" :message="toast.message" />
</template>

<script setup>
import { ref } from 'vue'
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css'
import api from '@/api/axios'
import ToastMessage from '../ToastMessage.vue'

const emit = defineEmits(['close', 'created'])

const title = ref('')
const content = ref('')

const toast = ref({ show: false, type: 'success', message: '' })
const showToast = (type, message) => {
  toast.value = { type, message, show: true }
  setTimeout(() => (toast.value.show = false), 3000)
}

const handleSubmit = async () => {
  try {
    await api.post('/articles/', {
      title: title.value,
      content: content.value
    })
    emit('created')
  } catch (err) {
    showToast('danger', '내용을 채워주세요')
  }
}
</script>
