// main.js
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
// 자동으로 localStorage 또는 sessionStorage에 저장된 상태를 Pinia store에 복원함.
pinia.use(piniaPluginPersistedstate)
app.use(pinia)  
app.use(router)
app.mount('#app')

app.config.errorHandler = (err, instance, info) => {
    console.error('Vue error:', err, info)
}

// 앱 시작 시 localStorage에서 복구
const authStore = useAuthStore()
authStore.initAuth()