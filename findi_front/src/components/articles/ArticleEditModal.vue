<!-- src/components/articles/ArticleEditModal.vue -->
<template>
  <div class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center">
    <div class="bg-white rounded-lg shadow-md p-6 w-full max-w-3xl relative">
      <h2 class="text-xl font-bold mb-4">게시글 수정</h2>

      <form @submit.prevent="handleSubmit">
        <label class="block mb-2 text-sm font-medium">제목</label>
        <input
          v-model="editedTitle"
          type="text"
          class="w-full border border-gray-300 rounded px-3 py-2 mb-4"
          required
        />

        <label class="block mb-2 text-sm font-medium">내용</label>
        <QuillEditor
          v-model:content="editedContent"
          toolbar="full"
          contentType="html"
          :style="{ height: '200px' }"
        />

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
            수정 완료
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import api from '@/api/axios'
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css'

const props = defineProps({
  articleId: String,
  initialTitle: String,
  initialContent: String
})
const emit = defineEmits(['close', 'updated'])

const editedTitle = ref(props.initialTitle)
const editedContent = ref(props.initialContent)

watch(
  () => props.initialTitle,
  (val) => (editedTitle.value = val)
)
watch(
  () => props.initialContent,
  (val) => (editedContent.value = val)
)

const handleSubmit = async () => {
  try {
    await api.put(`/articles/${props.articleId}/`, {
      title: editedTitle.value,
      content: editedContent.value
    })
    emit('updated')
    emit('close')
  } catch (error) {
    alert('수정 실패')
  }
}
</script>
