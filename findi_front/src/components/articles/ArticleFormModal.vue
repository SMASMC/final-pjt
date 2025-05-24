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
        <textarea
          v-model="content"
          class="w-full border border-gray-300 rounded px-3 py-2 mb-4 h-40 resize-none"
          placeholder="내용을 입력해 주세요"
          required
        ></textarea>

        <div class="mt-6 flex justify-end gap-2">
          <button
            type="button"
            @click="$emit('close')"
            class="px-4 py-2 border rounded hover:bg-gray-100"
          >
            취소
          </button>
          <button
            type="submit"
            class="px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600"
          >
            생성
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/api/axios'

const emit = defineEmits(['close', 'created'])

const title = ref('')
const content = ref('')

const handleSubmit = async () => {
  try {
    await api.post('/articles/', {
      title: title.value,
      content: content.value
    })
    emit('created')
  } catch (err) {
    alert('게시글 등록 실패')
  }
}
</script>

<style scoped>
</style>
