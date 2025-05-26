<!-- src/components/products/ProductJoined.vue -->
<template>
    <div class="w-full mt-10 bg-white shadow-md rounded-xl overflow-hidden">
        <table class="w-full text-sm text-left">
            <thead class="bg-purple-100 text-purple-800">
                <tr>
                    <th class="py-3 px-5">은행</th>
                    <th class="py-3 px-5">상품명</th>
                    <th class="py-3 px-5">유형</th>
                    <th class="py-3 px-5">기본 금리</th>
                    <th class="py-3 px-5">우대 금리</th>
                    <th class="py-3 px-5">가입일</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="product in portfolios" :key="product.id"
                    class="hover:bg-purple-50 transition-colors duration-200">
                    <td class="py-3 px-5 border-t border-gray-100">{{ product.bank_name }}</td>
                    <td class="py-3 px-5 border-t border-gray-100 text-purple-700 font-medium hover:text-purple-900 cursor-pointer"
                        @click="$emit('product-click', product.deposit_product || product.saving_product)">
                        {{ product.product_name }}
                    </td>
                    <td class="py-3 px-5 border-t border-gray-100">{{ product.product_type === 'deposit' ? '예금' : '적금'
                        }}</td>
                    <td class="py-3 px-5 border-t border-gray-100">{{ product.interest_rate ? product.interest_rate +
                        '%' : '-' }}</td>
                    <td class="py-3 px-5 border-t border-gray-100">{{ product.special_rate ? product.special_rate + '%'
                        : '-' }}</td>
                    <td class="py-3 px-5 border-t border-gray-100">{{ formatDate(product.joined_at) }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup>
defineProps({ portfolios: Array })
defineEmits(['product-click'])

const formatDate = (date) => {
    if (!date) return '-'
    const d = new Date(date)
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}
</script>
