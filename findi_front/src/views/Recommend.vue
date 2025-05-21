<!-- 맞춤 상품 조회 페이지-->

<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 px-4 py-8">
    <BankCard v-for="bank in banks" :key="bank.name" :logo="bank.logo" :name="bank.name" />
  </div>
</template>

<script setup>
import BankCard from '@/components/BankCard.vue'
import shinhan from '@/assets/bank_logos/shinhan.png'
import woori from '@/assets/bank_logos/woori.png'
import kb from '@/assets/bank_logos/kb.png'
import hana from '@/assets/bank_logos/hana.png'
import nh from '@/assets/bank_logos/nh.png'

const banks = [
  { name: '우리은행', logo: woori },
  { name: '신한은행', logo: shinhan },
  { name: 'KB국민은행', logo: kb },
  { name: '하나은행', logo: hana },
  { name: 'NH농협은행', logo: nh }
]
</script>
