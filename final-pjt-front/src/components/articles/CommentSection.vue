<template>
  <div class="mt-10">
    <h2 class="text-xl font-semibold mb-4">댓글</h2>

    <!-- 댓글 작성 폼 -->
    <form @submit.prevent="submitComment" class="mb-6">
      <textarea
        v-model="newComment"
        placeholder="댓글을 입력하세요"
        class="w-full border rounded p-2"
        rows="3"
        required
      ></textarea>
      <div class="flex justify-end mt-2">
        <button
          type="submit"
          class="bg-[#8A69E1] text-white px-4 py-2 rounded hover:bg-[#8A69E1]/90 cursor-pointer"
        >
          댓글 작성
        </button>
      </div>
    </form>

    <!-- 댓글 목록 -->
    <ul>
      <li v-if="comments.length === 0" class="text-gray-400">아직 댓글이 없습니다.</li>
      <li v-for="comment in visibleComments" :key="comment.id" class="border-b py-2">
        <div class="text-sm">
          <strong class="block mb-1">{{ comment.user?.userName || '알 수 없음' }}</strong>
          <template v-if="editingCommentId === comment.id">
            <textarea v-model="editedContent" class="w-full border rounded p-1" rows="2" />
          </template>
          <template v-else>
            <p class="whitespace-pre-wrap">{{ comment.content }}</p>
          </template>
        </div>

        <p class="text-xs text-gray-400">{{ formatDate(comment.created_at) }}</p>
        <div class="text-xs mt-1 flex gap-2">
          <button
            v-if="comment.is_author && editingCommentId !== comment.id"
            @click="startEditing(comment)"
            class="text-blue-500 hover:underline cursor-pointer"
          >
            수정
          </button>
          <button
            v-if="comment.is_author && editingCommentId === comment.id"
            @click="submitEdit(comment.id)"
            class="text-green-500 hover:underline cursor-pointer"
          >
            저장
          </button>
          <button
            v-if="comment.is_author"
            @click="deleteComment(comment.id)"
            class="text-red-500 hover:underline cursor-pointer"
          >
            삭제
          </button>
        </div>
      </li>
    </ul>

    <!-- 더보기/접기 -->
    <div v-if="comments.length > visibleCount" class="text-right mt-2">
      <button @click="toggleComments" class="text-sm text-[#8A69E1] hover:underline cursor-pointer">
        {{ isExpanded ? '접기' : '더보기' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import api from '@/api/axios'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  articleId: String
})
const emit = defineEmits(['comment-added', 'comment-deleted'])

const authStore = useAuthStore()
const comments = ref([])
const newComment = ref('')
const editingCommentId = ref(null)
const editedContent = ref('')
const visibleCount = ref(5)
const isExpanded = ref(false)

const visibleComments = computed(() => {
  return isExpanded.value ? comments.value : comments.value.slice(0, visibleCount.value)
})

const toggleComments = () => {
  isExpanded.value = !isExpanded.value
}

const loadComments = async () => {
  if (!props.articleId) return
  try {
    const { data } = await api.get(`/articles/${props.articleId}/comments/`)
    comments.value = data
    isExpanded.value = false // 초기화 시 접힌 상태로
  } catch (err) {
    console.error('댓글 로드 실패:', err)
  }
}

const submitComment = async () => {
  try {
    const payload = { content: newComment.value }
    const { data } = await api.post(`/articles/${props.articleId}/comments/`, payload, {
      headers: { Authorization: `Bearer ${authStore.accessToken}` }
    })
    comments.value.push(data)
    newComment.value = ''
    emit('comment-added', data)
  } catch (err) {
    alert('댓글 등록 실패')
  }
}

const deleteComment = async (id) => {
  try {
    await api.delete(`/articles/${props.articleId}/comments/${id}/`, {
      headers: { Authorization: `Bearer ${authStore.accessToken}` }
    })
    comments.value = comments.value.filter((c) => c.id !== id)
    emit('comment-deleted', id)
  } catch (err) {
    alert('댓글 삭제 실패')
  }
}

const startEditing = (comment) => {
  editingCommentId.value = comment.id
  editedContent.value = comment.content
}

const submitEdit = async (commentId) => {
  try {
    const payload = { content: editedContent.value }
    const { data } = await api.put(`/articles/${props.articleId}/comments/${commentId}/`, payload, {
      headers: { Authorization: `Bearer ${authStore.accessToken}` }
    })
    const idx = comments.value.findIndex((c) => c.id === commentId)
    if (idx !== -1) comments.value[idx] = data
    editingCommentId.value = null
    editedContent.value = ''
  } catch (err) {
    alert('댓글 수정 실패')
  }
}

const formatDate = (iso) => {
  if (!iso) return ''
  const date = new Date(iso)
  return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`
}

onMounted(() => {
  loadComments()
})

watch(
  () => props.articleId,
  (newId) => {
    if (newId) loadComments()
  }
)
</script>
