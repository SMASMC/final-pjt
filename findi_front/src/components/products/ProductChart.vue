<!-- src/components/products/ProductChart.vue -->
<template>
  <div class="w-full flex justify-center mt-4">
    <Bar v-if="chartData" :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const props = defineProps({
  portfolios: Array
})

const chartData = computed(() => {
  if (!props.portfolios || props.portfolios.length === 0) return null

  const labels = ['평균 금리']
  const basicRates = []
  const specialRates = []

  let sumBasic = 0
  let sumSpecial = 0
  let countBasic = 0
  let countSpecial = 0

  props.portfolios.forEach((p) => {
    labels.push(p.product_name)

    // Decimal 타입으로 들어오는 값은 toNumber 필요 없음
    if (p.interest_rate !== null) {
      sumBasic += parseFloat(p.interest_rate)
      countBasic++
      basicRates.push(parseFloat(p.interest_rate))
    } else {
      basicRates.push(0)
    }

    if (p.special_rate !== null) {
      sumSpecial += parseFloat(p.special_rate)
      countSpecial++
      specialRates.push(parseFloat(p.special_rate))
    } else {
      specialRates.push(0)
    }
  })

  const avgBasic = countBasic > 0 ? +(sumBasic / countBasic).toFixed(2) : 0
  const avgSpecial = countSpecial > 0 ? +(sumSpecial / countSpecial).toFixed(2) : 0

  basicRates.unshift(avgBasic)
  specialRates.unshift(avgSpecial)

  return {
    labels,
    datasets: [
      {
        label: '저축 금리',
        backgroundColor: [
          '#FFB84C', // 평균 금리 색상
          ...Array(props.portfolios.length).fill('#9691B5') // 나머지
        ],
        data: basicRates
      },
      {
        label: '최고 우대금리 금리',
        backgroundColor: [
          '#EBD04F', // 평균 우대 금리 색상
          ...Array(props.portfolios.length).fill('#D298FA')
        ],
        data: specialRates
      }
    ]
  }
})

const chartOptions = {
  responsive: true,
  plugins: {
    legend: { position: 'top' },
    title: { display: true, text: '가입한 상품 금리', font: { size: 25 } }
  },
  scales: {
    y: {
      beginAtZero: true
    }
  }
}
</script>
