import { defineStore } from 'pinia'

export const useToastStore = defineStore('toast', {
  state: () => ({
    show: false,
    type: 'success',
    message: ''
  }),
  actions: {
    showToast(type, message) {
      this.type = type
      this.message = message
      this.show = true

      setTimeout(() => {
        this.show = false
      }, 3000)
    }
  }
})
