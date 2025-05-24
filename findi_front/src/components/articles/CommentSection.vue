<template>
  <div class="mt-10">
    <h2 class="text-xl font-semibold mb-2">댓글</h2>
    <ul>
      <li v-for="comment in comments" :key="comment.id" class="border-b py-2">
        <p class="text-sm"><strong>{{ comment.user.userName }}</strong> {{ comment.content }}</p>
        <p class="text-xs text-gray-400">{{ formatDate(comment.created_at) }}</p>
        <button
          v-if="comment.is_author"
          @click="deleteComment(comment.id)"
          class="text-red-500 text-xs mt-1 hover:underline"
        >
          삭제
        </button>
      </li>
    </ul>

    <form @submit.prevent="submitComment" class="mt-6">
      <textarea
        v-model="newComment"
        placeholder="댓글을 입력하세요"
        class="w-full border rounded p-2"
        rows="3"
        required
      ></textarea>
      <div class="flex justify-end mt-2">
        <button type="submit" class="bg-purple-500 text-white px-4 py-2 rounded hover:bg-purple-600">
          댓글 작성
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/api/axios'
import { useRoute } from 'vue-router'

const route = useRoute()
const emit = defineEmits(['comment-added'])

const comments = ref([])
const newComment = ref('')

const loadComments = async () => {
  const { data } = await api.get(`/articles/${route.params.id}/`)
  comments.value = data.comments
}

const submitComment = async () => {
  try {
    const { data } = await api.post(`/articles/${route.params.id}/comments/`, {
      content: newComment.value
    })
    comments.value.push(data)
    newComment.value = ''
    emit('comment-added', data) // 이벤트 emit
  } catch (err) {
    alert('댓글 등록 실패')
  }
}

const deleteComment = async (id) => {
  try {
    await api.delete(`/articles/${route.params.id}/comments/${id}/`)
    comments.value = comments.value.filter(c => c.id !== id)
  } catch (err) {
    alert('댓글 삭제 실패')
  }
}

const formatDate = (iso) => {
  if (!iso) return ''
  const date = new Date(iso)
  return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`
}

defineExpose({ loadComments })
</script>
