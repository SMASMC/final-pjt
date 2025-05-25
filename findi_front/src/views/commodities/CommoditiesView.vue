<template>
  <div class="max-w-6xl mx-auto p-4 pt-20">
    <div class="mb-4 flex gap-4 items-center">
      <input type="date" v-model="start" />
      <input type="date" v-model="end" />
      <button
        class="px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600"
        @click="() => fetchData('gold')"
      >
        금
      </button>
      <button
        class="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
        @click="() => fetchData('silver')"
      >
        은
      </button>
    </div>

    <div class="text-sm text-gray-500 mb-2">
      ⚠️ 데이터는 <span class="font-semibold text-black">2023-01-09</span>부터
      <span class="font-semibold text-black">2024-12-01</span>까지만 제공됩니다.
    </div>

    <div v-if="errorMsg" class="text-red-600 mb-2">{{ errorMsg }}</div>
    <LineChart v-if="chartData" :chart-data="chartData" />

    <ToastMessage v-if="toast.show" :type="toast.type" :message="toast.message" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/axios'
import LineChart from '@/components/commodities/LineChart.vue'
import ToastMessage from '@/components/ToastMessage.vue'

const start = ref('')
const end = ref('')
const chartData = ref(null)
const errorMsg = ref('')
const toast = ref({ show: false, type: 'success', message: '' })

const showToast = (type, message) => {
  toast.value = { type, message, show: true }
  setTimeout(() => (toast.value.show = false), 3000)
}

// ✅ 금/은 버튼 클릭 또는 onMounted에서 호출
const fetchData = async (metalType) => {
  errorMsg.value = ''
  chartData.value = null

  // 날짜 유효성 기준
  const minDateStr = '2023-01-09'
  const maxDateStr = '2024-12-01'
  const minDate = new Date(minDateStr)
  const maxDate = new Date(maxDateStr)

  // ✅ 실제 요청에 사용할 날짜 (비어 있으면 기본값으로 대체)
  const effectiveStart = start.value || minDateStr
  const effectiveEnd = end.value || maxDateStr

  const startDate = new Date(effectiveStart)
  const endDate = new Date(effectiveEnd)

  // 날짜 순서 및 범위 검증
  if (startDate > endDate) {
    showToast('danger', '시작일은 종료일보다 앞서야 합니다.')
    return
  }
  if (startDate < minDate || endDate > maxDate) {
    showToast('danger', '날짜는 2023-01-09 ~ 2024-12-01 사이로 선택해주세요.')
    return
  }

  try {
    const res = await api.get('/commodities/', {
      params: {
        metal: metalType,
        start: effectiveStart,
        end: effectiveEnd
      }
    })

    if (res.data.length === 0) {
      showToast('danger', '선택한 조건에 해당하는 데이터가 없습니다.')
    } else {
      chartData.value = {
        labels: res.data.map((e) => e.date),
        datasets: [
          {
            label: `${metalType.toUpperCase()} 가격`,
            data: res.data.map((e) => e.close),
            borderColor: metalType === 'gold' ? 'gold' : 'gray',
            fill: false
          }
        ]
      }
    }
  } catch (err) {
    errorMsg.value = err.response?.data?.error || '조회 중 오류가 발생했습니다.'
    showToast('danger', errorMsg.value)
  }
}

// 최초 컴포넌트 로드시 전체 금 데이터 자동 조회
onMounted(() => {
  fetchData('gold')
})
</script>
