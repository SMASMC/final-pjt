<!-- src/views/products/ProductsView.vue -->

<template>
  <div class="w-full max-w-6xl mx-auto pt-25 px-4">
    <!-- 탭 선택 -->
    <div class="flex gap-4 mb-6">
      <button class="cursor-pointer" @click="selectTab('deposit')" :class="tabClass('deposit')">정기예금</button>
      <button class="cursor-pointer" @click="selectTab('saving')" :class="tabClass('saving')">정기적금</button>
    </div>

    <!-- 필터 + 테이블 -->
    <div class="flex gap-6">
      <div class="w-64 shrink-0 bg-purple-50 border border-purple-200 p-4 rounded-lg shadow">
        <ProductFilter :selectedTab="selectedTab" @filter-changed="onFilterChanged" />
      </div>

      <div class="flex-1">
        <ProductTable :products="products" @row-click="openModal" @sort-changed="onSortChanged" />

        <!-- 페이지네이션 -->
        <div v-if="pagination.count > pagination.page_size" class="flex justify-between mt-4">
          <button @click="prevPage" :disabled="!pagination.previous"
            class="px-4 py-2 bg-gray-200 rounded disabled:opacity-50 cursor-pointer">이전</button>
          <span class="text-sm text-gray-600">{{ pagination.page }} / {{ totalPages }} 페이지</span>
          <button @click="nextPage" :disabled="!pagination.next"
            class="px-4 py-2 bg-gray-200 rounded disabled:opacity-50 cursor-pointer">다음</button>
        </div>
      </div>
    </div>

    <!-- 모달 -->
    <ProductModal v-if="selectedProduct" :product="selectedProduct" :productType="selectedTab" @updated="handleUpdated"
      @close="selectedProduct = null" />
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import ProductFilter from '@/components/products/ProductFilter.vue'
import ProductTable from '@/components/products/ProductTable.vue'
import ProductModal from '@/components/products/ProductModal.vue'
import api from '@/api/axios'

const selectedTab = ref('deposit')
const products = ref([])
const selectedProduct = ref(null)
const filters = ref({})

const pagination = ref({
  page: 1,
  count: 0,
  page_size: 15,
  next: null,
  previous: null,
})

const sort = ref({
  field: 'intr_rate2',
  order: 'desc'
})

const totalPages = computed(() => Math.ceil(pagination.value.count / pagination.value.page_size))

const tabClass = (type) =>
  selectedTab.value === type
    ? 'bg-purple-600 text-white px-4 py-2 rounded'
    : 'bg-gray-100 px-4 py-2 rounded'

// API 호출 함수
const fetchProducts = async () => {
  const endpoint = selectedTab.value === 'deposit' ? '/finance/deposit/' : '/finance/saving/'

  // 정렬 파라미터 준비
  const ordering =
    sort.value.order === 'asc' ? sort.value.field : `-${sort.value.field}`

  try {
    const res = await api.get(endpoint, {
      params: {
        ...filters.value,
        ordering,
        page: pagination.value.page,
      }
    })
    products.value = res.data.results || []
    pagination.value.count = res.data.count || 0
    pagination.value.next = res.data.next
    pagination.value.previous = res.data.previous
  } catch (err) {
    console.error('상품 조회 실패:', err)
    products.value = []
    pagination.value.count = 0
    pagination.value.next = null
    pagination.value.previous = null
  }
}

// 탭 변경
const selectTab = (tab) => {
  selectedTab.value = tab
  pagination.value.page = 1
  filters.value = {}
  fetchProducts()
}

// 필터 변경 시
const onFilterChanged = (newFilters) => {
  filters.value = newFilters
  pagination.value.page = 1
  fetchProducts()
}

// 정렬 기준 변경 시
const onSortChanged = (newSort) => {
  sort.value = newSort
  pagination.value.page = 1
  fetchProducts()
}

// 모달 열기
const openModal = (product) => {
  selectedProduct.value = product
}

// 페이지 이동
const nextPage = () => {
  if (pagination.value.next) {
    pagination.value.page++
    fetchProducts()
  }
}

const prevPage = () => {
  if (pagination.value.previous) {
    pagination.value.page--
    fetchProducts()
  }
}

onMounted(fetchProducts)
</script>