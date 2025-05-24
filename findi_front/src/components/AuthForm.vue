<template>
  <form @submit.prevent="handleSubmit">
    <div class="w-full mb-3">
      <label class="w-full">이메일</label><br />
      <input type="email" v-model="form.email" required class="form-control w-full rounded-xl" />
    </div>

    <div v-if="mode === 'signup'" class="mb-3">
      <label class="w-full">이름</label><br />
      <input type="text" v-model="form.userName" required class="form-control w-full rounded-xl" />
    </div>

    <div class="w-full mb-3">
      <label>비밀번호</label><br />
      <input
        type="password"
        v-model="form.password"
        required
        class="form-control w-full rounded-xl"
        style="font-family: sans-serif"
      />
    </div>

    <div v-if="mode === 'signup'" class="mb-3">
      <label>비밀번호 확인</label>
      <input
        type="password"
        v-model="form.password2"
        required
        class="form-control w-full rounded-xl"
        style="font-family: sans-serif"
      />
    </div>

    <button
      type="submit"
      class="w-full btn btn-primary border rounded-lg p-2 text-white bg-[#a98dff] cursor-pointer"
    >
      {{ mode === 'signup' ? '회원가입' : '로그인' }}
    </button>
  </form>
</template>

<script setup>
import { reactive } from 'vue'
import api from '@/api/axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()
const props = defineProps({
  mode: { type: String, default: 'login' } // or 'signup'
})

const form = reactive({
  email: '',
  userName: '',
  password: '',
  password2: ''
})

const handleSubmit = async () => {
  try {
    const url = props.mode === 'signup' ? '/accounts/auth/registration/' : '/accounts/auth/login/'

    const payload =
      props.mode === 'signup'
        ? {
            email: form.email,
            userName: form.userName,
            password1: form.password,
            password2: form.password2
          }
        : {
            email: form.email,
            password: form.password
          }

    const res = await api.post(url, payload)
    console.log(`✅ Success: ${JSON.stringify(res.data)}`)
    const { access_token, refresh_token, user } = res.data
    authStore.loginSuccess({ access: access_token, refresh: refresh_token, user })

    router.replace({ name: 'home' })
  } catch (err) {
    console.error('❌ Error:', err.response?.data || err.message)
  }
}
</script>
