import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { useAuthStore } from '@/stores/auth'

import App from './App.vue'
import router from './router'

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
// 웹 시작 시점에서 AuthStore 로컬스토리지 로드
const authStore = useAuthStore()
authStore.loadFromLocalStorage()

app.use(router)
app.mount('#app')
