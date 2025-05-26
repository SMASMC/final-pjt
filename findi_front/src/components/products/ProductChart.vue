<!-- src/components/products/ProductChart.vue -->
<template>
  <Bar v-if="chartData" :data="chartData" :options="chartOptions" />
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
  portfolios: Array,
})

const chartData = computed(() => {
  if (!props.portfolios || props.portfolios.length === 0) return null

  const labels = ['평균 금리']
  const basicRates = []
  const specialRates = []

  let sumBasic = 0
  let sumSpecial = 0

  props.portfolios.forEach(p => {
    labels.push(p.product_name)
    basicRates.push(p.interest_rate || 0)
    specialRates.push(p.special_rate || 0)
    sumBasic += p.interest_rate || 0
    sumSpecial += p.special_rate || 0
  })

  const avgBasic = +(sumBasic / props.portfolios.length).toFixed(2)
  const avgSpecial = +(sumSpecial / props.portfolios.length).toFixed(2)

  basicRates.unshift(avgBasic)
  specialRates.unshift(avgSpecial)

  return {
    labels,
    datasets: [
      {
        label: '저축 금리',
        backgroundColor: '#9691B5',
        data: basicRates,
      },
      {
        label: '최고 우대금리 금리',
        backgroundColor: '#D298FA',
        data: specialRates,
      },
    ]
  }
})

const chartOptions = {
  responsive: true,
  plugins: {
    legend: { position: 'top' },
    title: { display: true, text: '가입한 상품 금리', font:{size:25} },
  },
  scales: {
    y: {
      beginAtZero: true,
      max: 5
    }
  }
}
</script>
