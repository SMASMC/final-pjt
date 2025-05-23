// tailwindcss 적용
import './assets/main.css'
import 'flowbite';

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { useAuthStore } from '@/stores/auth'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

import App from './App.vue'
import router from './router'

const app = createApp(App)
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

app.use(pinia)
app.use(router)
app.mount('#app')

// 웹 시작 시점에서 AuthStore 로컬스토리지 로드
const authStore = useAuthStore()
authStore.loadFromLocalStorage()