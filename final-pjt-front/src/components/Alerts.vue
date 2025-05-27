<template>
  <fwb-alert class="border-t-4 rounded-none" :icon="icon" :type="type">
    {{ message }}
  </fwb-alert>
</template>

<script setup>
import { FwbAlert } from 'flowbite-vue'

const props = defineProps({
  type: {
    type: String,
    required: true,
    validator: (value) => ['info', 'warning', 'danger', 'dark', 'success'].includes(value)
  },
  message: {
    type: String,
    required: true
  },
  icon: {
    type: Boolean,
    default: true
  }
})
</script>
<!-- ExampleView.vue or App.vue -->
<!-- <template>
    <div class="vp-raw grid gap-2">
      <AlertMessage
        v-for="alert in alerts"
        :key="alert.type"
        :type="alert.type"
        :message="alert.message"
      />
    </div>
  </template>
  
  <script setup>
  import AlertMessage from '@/components/AlertMessage.vue'
  
  const alerts = [
    { type: 'info', message: 'Info alert! Change a few things up and try submitting again.' },
    { type: 'warning', message: 'Warning alert! Change a few things up and try submitting again.' },
    { type: 'danger', message: 'Danger alert! Change a few things up and try submitting again.' },
    { type: 'dark', message: 'Dark alert! Change a few things up and try submitting again.' },
    { type: 'success', message: 'Success alert! Change a few things up and try submitting again.' }
  ]
  </script>   -->
