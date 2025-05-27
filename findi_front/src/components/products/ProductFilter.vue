<!-- src/components/products/ProductFilter.vue -->

<template>
  <div class="flex flex-col gap-4">
    <!-- 은행 선택 필터 -->
    <div>
      <label class="text-sm text-gray-700 mb-1">은행</label>
      <select v-model="selectedBank" class="border border-gray-300 rounded px-3 py-2 w-full">
        <option value="">전체 은행</option>
        <option v-for="bank in bankList" :key="bank" :value="bank">{{ bank }}</option>
      </select>
    </div>

    <!-- 가입 기간 선택 필터 -->
    <div>
      <label class="text-sm text-gray-700 mb-1">가입 기간</label>
      <select v-model="selectedPeriod" class="border border-gray-300 rounded px-3 py-2 w-full">
        <option value="">전체</option>
        <option v-for="month in periodList" :key="month" :value="month">{{ month }}개월</option>
      </select>
    </div>

    <!-- 필터 적용 버튼 -->
    <button
      @click="applyFilter"
      class="bg-[#8A69E1] text-white px-5 py-2 rounded hover:bg-[#8A69E1]/90 transition w-full cursor-pointer"
    >
      확인
    </button>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

// JSON 캐시 데이터 불러오기 (프론트 캐싱용)
import finance_cache_deposit from '../../../../findi_back/finance/data_cache/finance_cache_deposit.json'
import finance_cache_saving from '../../../../findi_back/finance/data_cache/finance_cache_saving.json'

// 부모 컴포넌트로부터 전달되는 현재 탭 정보 ('deposit' 또는 'saving')
const props = defineProps({
  selectedTab: {
    type: String,
    default: 'deposit'
  }
})

// 선택된 은행과 가입 기간 상태 관리
const selectedBank = ref('')
const selectedPeriod = ref('')

// 부모 컴포넌트에 필터 변경 이벤트 전달
const emit = defineEmits(['filter-changed'])

// 은행명 리스트와 기간 리스트 상태 관리
const bankList = ref([])
const periodList = ref([])

// 중복 제거된 은행 목록 추출 함수
const extractBankList = (data) => Array.from(new Set(data.map((item) => item.kor_co_nm)))

// 상품 기간 리스트 추출 함수 (중복 제거 및 오름차순 정렬)
const extractPeriodList = (data) => {
  const terms = new Set()
  data.forEach((item) => {
    const term = parseInt(item.save_trm)
    if (!isNaN(term)) terms.add(term)
  })
  return Array.from(terms).sort((a, b) => a - b)
}

// 선택된 탭(deposit/saving)에 따라 JSON에서 은행/기간 리스트 로드
const loadFilterData = () => {
  const data = props.selectedTab === 'deposit' ? finance_cache_deposit : finance_cache_saving
  bankList.value = extractBankList(data)
  periodList.value = extractPeriodList(data)
}

// '확인' 버튼 클릭 시, 부모로 필터 전달
const applyFilter = () => {
  const filter = {}
  if (selectedBank.value) filter.bank = selectedBank.value
  if (selectedPeriod.value) filter.save_trm = Number(selectedPeriod.value) // 문자열 → 숫자 변환
  emit('filter-changed', filter)
}

// 탭이 변경될 때마다 필터 데이터 새로 로드
watch(() => props.selectedTab, loadFilterData, { immediate: true })
</script>
