<template>
  <div class="fixed bottom-10 right-10 z-[9999] chatbot-wrapper">
    <!-- 토글 버튼 -->
    <button @click="toggleChat" class="bg-purple-600 text-white rounded-full p-4 shadow-lg">
      <img v-if="!showChat" src="@/assets/chatbot.png" alt="chatbot" class="w-8 h-8" />
      <img v-else src="@/assets/chatbot.png" alt="chatbot-open" class="w-8 h-8 animate-bounce" />
    </button>

    <!-- 챗봇 UI -->
    <div
      v-if="showChat"
      class="chat-box bg-white w-80 h-[500px] rounded-2xl shadow-xl mt-3 flex flex-col"
      @click.stop
      @wheel.stop
    >
      <!-- 헤더 -->
      <div class="chat-header bg-[#8A69E1] text-white p-3 font-bold rounded-t-2xl">
        무엇이 궁금하신가요?
      </div>

      <!-- 예상 질문 -->
      <div class="p-2 flex flex-wrap gap-2 bg-gray-100">
        <button
          v-for="(example, i) in exampleQuestions"
          :key="i"
          class="text-sm bg-white px-3 py-1 border border-purple-400 rounded-2xl hover:bg-purple-100"
          @click.stop="selectExample(example)"
        >
          {{ example }}
        </button>
      </div>

      <!-- 메시지 + 로딩 -->
      <div ref="chatContainer" class="chat-messages p-3 overflow-y-auto flex-1">
        <div v-for="msg in messages" :key="msg.id" :class="msg.isUser ? 'text-right' : 'text-left'">
          <div v-if="msg.isUser" class="rounded-2xl px-2 py-1 inline-block my-1 bg-blue-100">
            {{ msg.text }}
          </div>
          <div
            v-else
            class="rounded-2xl px-2 py-1 inline-block my-1 bg-gray-100 prose prose-sm max-w-full"
            v-html="renderMarkdown(msg.text)"
          ></div>
        </div>

        <!-- 로딩 표시 -->
        <div v-if="isLoading" class="text-left">
          <p class="bg-gray-100 rounded-2xl px-2 py-1 inline-block my-1 text-sm">
            <span class="dot-flashing"></span>
          </p>
        </div>
      </div>

      <!-- 입력창 -->
      <div class="chat-input p-2 flex gap-2">
        <input
          v-model="newMessage"
          @keyup.enter="sendMessage"
          type="text"
          class="w-full border rounded-2xl px-2 py-1"
          placeholder="Findi에 관해 무엇이든 물어보세요."
          :disabled="isLoading"
        />
        <button
          @click="sendMessage"
          class="bg-purple-500 text-white px-3 rounded-2xl whitespace-nowrap"
          :disabled="isLoading || !newMessage.trim()"
        >
          전송
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick, onMounted } from 'vue'
import api from '@/api/axios'
import { useAuthStore } from '@/stores/auth'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const authStore = useAuthStore()

const showChat = ref(false)
const newMessage = ref('')
const messages = ref([])
const isLoading = ref(false)

const exampleQuestions = ref([
  'Findi는 무엇인가요?',
  '어떤 기능들이 있나요?',
  'Findi는 어떻게 금융상품을 추천하나요?',
  'AI 맞춤 상품 추천을 받으려면 어떻게 해야하나요?',
  'Findi를 통해 대출 정보를 볼 수 있나요?'
])

const toggleChat = () => {
  showChat.value = !showChat.value
  if (!showChat.value) {
    document.activeElement.blur()
  }
}

const chatContainer = ref(null)

const scrollToBottom = () => {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    }
  })
}

watch(messages, () => {
  scrollToBottom()
})

const sendMessage = async () => {
  if (!newMessage.value.trim() || isLoading.value) return

  const userMsg = { text: newMessage.value, isUser: true, id: Date.now() }
  messages.value.push(userMsg)
  isLoading.value = true

  try {
    const res = await api.post('/faq/ask/', { question: newMessage.value })
    messages.value.push({
      text: res.data.answer,
      isUser: false,
      id: Date.now() + 1
    })
  } catch (e) {
    messages.value.push({
      text: '답변을 불러오는 데 실패했습니다.',
      isUser: false,
      id: Date.now() + 2
    })
  } finally {
    isLoading.value = false
    newMessage.value = ''
    scrollToBottom()
  }
}

const selectExample = (question) => {
  if (isLoading.value) return
  newMessage.value = question
  sendMessage()
}

const renderMarkdown = (text) => {
  return DOMPurify.sanitize(marked.parse(text || ''))
}
</script>

<style scoped>
.chat-box {
  z-index: 9999;
}

.dot-flashing::after {
  content: '';
  display: inline-block;
  width: 1em;
  animation: dots 1.2s steps(4, end) infinite;
}

@keyframes dots {
  0% {
    content: '';
  }
  25% {
    content: '.';
  }
  50% {
    content: '..';
  }
  75% {
    content: '...';
  }
  100% {
    content: '';
  }
}
</style>
