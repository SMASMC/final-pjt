<template>
  <form @submit.prevent="handleSubmit">
    <div class="w-full mb-3">
      <label class="w-full">이메일</label><br/>
      <input type="email" v-model="form.email" required class="form-control w-full rounded-xl" />
    </div>

    <div class="w-full mb-3">
      <label>비밀번호</label><br/>
      <input type="password" v-model="form.password" required class="form-control w-full rounded-xl" />
    </div>

    <div v-if="mode === 'signup'" class="mb-3">
      <label>비밀번호 확인</label>
      <input type="password" v-model="form.password2" required class="form-control" />
    </div>

    <div class="mb-3" v-if="mode === 'signup'">
      <label>성별</label>
      <div class="d-flex gap-2">
        <button class="btn btn-outline-primary" type="button" @click="form.gender = 'male'">
          남자
        </button>
        <button class="btn btn-outline-danger" type="button" @click="form.gender = 'female'">
          여자
        </button>
      </div>
    </div>

    <button type="submit" class="w-full btn btn-primary w-100 border rounded-lg p-2 text-white bg-[#a98dff] cursor-pointer">
      {{ mode === 'signup' ? '회원가입' : '로그인' }}
    </button>
  </form>
</template>

<script setup>
import { reactive } from 'vue'
import axios from 'axios'

const props = defineProps({
  mode: { type: String, default: 'login' } // or 'signup'
})

const form = reactive({
  email: '',
  password: '',
  password2: '',
  gender: ''
})

const handleSubmit = async () => {
  try {
    const url =
      props.mode === 'signup'
        ? 'http://localhost:8000/accounts/signup/'
        : 'http://localhost:8000/accounts/login/'

    const payload =
      props.mode === 'signup'
        ? {
            email: form.email,
            password1: form.password,
            password2: form.password2,
            gender: form.gender
          }
        : { email: form.email, password: form.password }

    const res = await axios.post(url, payload)
    console.log('✅ Success:', res.data)
  } catch (err) {
    console.error('❌ Error:', err.response.data)
  }
}
</script>
