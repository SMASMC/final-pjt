<!-- src/components/products/ProductTable.vue -->

<template>
  <div class="overflow-x-auto flex-1 shadow-xl">
    <table class="min-w-full table-fixed border border-gray-200 text-sm">
      <thead class="bg-blue-50 text-gray-700">
        <tr>
          <th class="p-2">공시월</th>
          <th class="p-2">은행명</th>
          <th class="p-2">상품명</th>
          <th class="p-2">기간</th>
          <th class="p-2 cursor-pointer" @click="sortBy('intr_rate')">
            기본금리
            <SortIcon field="intr_rate" />
          </th>
          <th class="p-2 cursor-pointer" @click="sortBy('intr_rate2')">
            우대금리
            <SortIcon field="intr_rate2" />
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="product in sortedProducts"
          :key="product.fin_prdt_cd + '-' + product.save_trm"
          @click="$emit('row-click', product)"
          class="hover:bg-gray-100 cursor-pointer text-center hover:scale-105 duration-400"
        >
          <td class="p-2">{{ product.dcls_month }}</td>
          <td class="p-2">{{ product.kor_co_nm }}</td>
          <td class="p-2 text-left">{{ product.fin_prdt_nm }}</td>
          <td class="p-2">{{ product.save_trm }}개월</td>
          <td class="p-2">
            {{
              product.intr_rate != null && product.intr_rate !== ''
                ? Number(product.intr_rate).toFixed(2) + '%'
                : '-'
            }}
          </td>
          <td class="p-2">
            {{
              product.intr_rate2 != null && product.intr_rate2 !== ''
                ? Number(product.intr_rate2).toFixed(2) + '%'
                : '-'
            }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, defineComponent, h, computed } from 'vue'

// Props
const props = defineProps({
  products: {
    type: Array,
    default: () => []
  }
})

// Emit 이벤트
const emit = defineEmits(['row-click', 'sort-changed'])

// 현재 정렬 상태
const sortField = ref('intr_rate2')
const sortOrder = ref('desc')

// 정렬된 products 계산
const sortedProducts = computed(() => {
  const sorted = [...props.products]
  const field = sortField.value
  const order = sortOrder.value

  return sorted.sort((a, b) => {
    const valA = Number(a[field])
    const valB = Number(b[field])
    if (isNaN(valA)) return 1
    if (isNaN(valB)) return -1
    return order === 'asc' ? valA - valB : valB - valA
  })
})

// 정렬 클릭 시 부모로 전달
const sortBy = (field) => {
  if (sortField.value === field) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortField.value = field
    sortOrder.value = 'asc'
  }

  // 정렬된 결과를 직접 계산하지 않음
  emit('sort-changed', {
    field: sortField.value,
    order: sortOrder.value
  })
}

// SortIcon 컴포넌트
const SortIcon = defineComponent({
  props: {
    field: String
  },
  setup(props) {
    const arrowClass = (dir) => {
      return sortField.value === props.field && sortOrder.value === dir
        ? 'text-purple-600 font-bold font-symbol'
        : 'text-gray-300 font-symbol'
    }

    return () =>
      h('span', { class: 'ml-1 text-xs' }, [
        h('span', { class: arrowClass('asc') }, '▲'),
        h('span', { class: arrowClass('desc') }, '▼')
      ])
  }
})
</script>
