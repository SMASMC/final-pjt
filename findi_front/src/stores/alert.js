import { defineStore } from 'pinia'

export const useAlertStore = defineStore('alert', {
  state: () => ({
    message: '',
    type: 'info', // 'success' | 'danger' | 'warning' | 'info'
    visible: false
  }),
  actions: {
    show(message, type = 'info', timeout = 3000) {
      this.message = message
      this.type = type
      this.visible = true

      setTimeout(() => {
        this.visible = false
        this.message = ''
      }, timeout)
    }
  }
})
