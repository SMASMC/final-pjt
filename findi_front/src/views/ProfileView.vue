<!-- 여기에 들어왔을 때, /accounts/profile/user_id로 요청을 보내서 사용자의 개인 정보를 표시 -->
<!-- src/views/ProfileView.vue -->
<template>
  <form @submit.prevent="submitProfile">
    <label>나이: <input v-model="age" type="number" required /></label>

    <label
      >수입 수준:
      <select v-model="income_level">
        <option value="low">저소득</option>
        <option value="middle">중간</option>
        <option value="high">고소득</option>
      </select>
    </label>

    <label
      >위험 선호도:
      <select v-model="risk_tolerance">
        <option value="low">낮음</option>
        <option value="medium">중간</option>
        <option value="high">높음</option>
      </select>
    </label>

    <label
      >재무 목표:
      <select v-model="financial_goal">
        <option value="saving">저축</option>
        <option value="investment">투자</option>
        <option value="retirement">은퇴 준비</option>
      </select>
    </label>

    <label
      >관심 금융 상품:
      <div>
        <input type="checkbox" value="deposit" v-model="interested_products" /> 예금
        <input type="checkbox" value="loan" v-model="interested_products" /> 대출
        <input type="checkbox" value="insurance" v-model="interested_products" /> 보험
        <input type="checkbox" value="fund" v-model="interested_products" /> 펀드
      </div>
    </label>

    <button type="submit">저장</button>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import axios from '@/api/axios'

const age = ref(null)
const income_level = ref('middle')
const risk_tolerance = ref('medium')
const financial_goal = ref('saving')
const interested_products = ref([])

const submitProfile = async () => {
  try {
    await axios.put('/accounts/profile/', {
      age: age.value,
      income_level: income_level.value,
      risk_tolerance: risk_tolerance.value,
      financial_goal: financial_goal.value,
      interested_products: interested_products.value
    })
    alert('저장 완료')
  } catch (error) {
    console.error(error)
    alert('저장 실패')
  }
}
</script>
