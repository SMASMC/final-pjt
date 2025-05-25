<template>
  <canvas ref="canvasRef"></canvas>
</template>

<script setup>
import { ref, watch, onMounted, nextTick } from 'vue'
import {
  Chart,
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  Title,
  CategoryScale
} from 'chart.js'

Chart.register(LineController, LineElement, PointElement, LinearScale, Title, CategoryScale)

const props = defineProps({
  chartData: Object,
  chartOptions: Object
})

const canvasRef = ref(null)
let chartInstance = null

const createChart = () => {
  if (chartInstance) {
    chartInstance.destroy()
  }

  const ctx = canvasRef.value?.getContext('2d')
  if (!ctx) {
    console.error('Chart.js: canvas context 가져오기 실패')
    return
  }

  chartInstance = new Chart(ctx, {
    type: 'line',
    data: props.chartData,
    options: props.chartOptions || {
      responsive: true,
      plugins: {
        legend: {
          display: true
        }
      }
    }
  })
}

// props.chartData가 변경될 때마다 차트를 다시 생성 (렌더 후 실행 보장)
watch(
  () => props.chartData,
  async (newData) => {
    if (newData) {
      await nextTick() // DOM 업데이트 이후 실행
      createChart()
    }
  },
  { immediate: true }
)
</script>
