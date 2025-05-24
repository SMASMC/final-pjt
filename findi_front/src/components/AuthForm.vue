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
  <ToastMessage v-if="toast.show" :type="toast.type" :message="toast.message" />
</template>

<script setup>
import { reactive, ref } from 'vue'
import api from '@/api/axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import ToastMessage from '@/components/ToastMessage.vue'

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
const toast = ref({ type: '', message: '', show: false })

const showToast = (type, message) => {
  toast.value = { type, message, show: true }
  setTimeout(() => {
    toast.value.show = false
  }, 3000)
}
const handleSubmit = async () => {
  // 회원가입 시 추가 검증
  if (props.mode === 'signup') {
    const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*()_+|~=`{}\[\]:";'<>?,.\/\\]).{8,}$/

    if (!passwordRegex.test(form.password)) {
      showToast('warning', '비밀번호는 8자 이상, 문자/숫자/특수문자를 포함해야 합니다.')
      return
    }

    if (form.password !== form.password2) {
      showToast('danger', '비밀번호가 일치하지 않습니다.')
      return
    }
  }

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
    const { access_token, refresh_token, user } = res.data
    authStore.loginSuccess({ access: access_token, refresh: refresh_token, user })

    showToast('success', '로그인 성공!')
    router.replace({ name: 'home' })
  } catch (err) {
    console.error('❌ Error:', err.response?.data || err.message)

    const msg =
      err.response?.data?.non_field_errors?.[0] ||
      err.response?.data?.email?.[0] ||
      err.response?.data?.password?.[0] ||
      '서버 오류 또는 잘못된 입력입니다.'

    showToast('danger', msg)
  }
}
</script>
