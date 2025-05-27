<template>
  <div class="flex w-[90%] h-[90vh] mx-auto p-4 gap-4">
    <!-- 좌측 드롭다운 패널 -->
    <div
      class="w-[340px] shrink-0 space-y-3 bg-white rounded-xl border border-purple-300 p-4 shadow-md"
    >
      <div class="flex flex-col">
        <h1 class="text-2xl">은행 검색</h1>
        <br />

        <label class="text-sm text-purple-800 mb-1">시/도</label>
        <select
          v-model="sido"
          @change="updateGugunList"
          class="border border-purple-300 p-2 rounded focus:outline-purple-400"
        >
          <option value="">시/도 선택</option>
          <option v-for="s in dataStore.mapInfo" :key="s.name" :value="s.name">{{ s.name }}</option>
        </select>
      </div>

      <div class="flex flex-col">
        <label class="text-sm text-purple-800 mb-1">시/군/구</label>
        <select
          v-model="gugun"
          class="border border-purple-300 p-2 rounded focus:outline-purple-400"
        >
          <option value="">시/군/구 선택</option>
          <option v-for="g in dataStore.gugunList" :key="g">{{ g }}</option>
        </select>
      </div>

      <div class="flex flex-col">
        <label class="text-sm text-purple-800 mb-1">은행</label>
        <select
          v-model="bank"
          class="border border-purple-300 p-2 rounded focus:outline-purple-400"
        >
          <option value="">은행 선택</option>
          <option v-for="b in dataStore.bankInfo" :key="b">{{ b }}</option>
        </select>
      </div>

      <div class="flex gap-2">
        <button
          @click="search"
          class="bg-[#8A69E1]/90 text-white px-4 py-2 rounded hover:bg-[#8A69E1]/80 w-full"
        >
          검색
        </button>
        <button
          @click="goToMyLocation"
          class="bg-white border border-[#8A69E1]/90 text-[#8A69E1]/90 px-4 py-2 rounded hover:bg-[#8A69E1]/80 w-full"
        >
          📍현위치
        </button>
      </div>
    </div>

    <!-- 지도 및 상세 정보 카드 -->
    <div class="relative flex-1 h-full rounded-xl border border-purple-200 shadow bg-white">
      <div id="map" class="absolute inset-0 rounded-xl z-0"></div>

      <!-- 마커 클릭 시 상세 정보 카드 -->
      <BankInfoCard v-if="selectedPlace" :place="selectedPlace" />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import axios from 'axios'
import BankInfoCard from './BankInfoCard.vue'

const sido = ref('')
const gugun = ref('')
const bank = ref('')
const selectedPlace = ref(null)

// 반응형으로
const dataStore = reactive({
  mapInfo: [],
  bankInfo: [],
  gugunList: []
})

let map = null
let markers = []
let selectedMarker = null

function loadKakaoScript(key) {
  return new Promise((resolve) => {
    if (window.kakao && window.kakao.maps) return resolve()

    const script = document.createElement('script')
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${key}&libraries=services`
    script.onload = () => window.kakao.maps.load(resolve)
    document.head.appendChild(script)
  })
}

// 맵 띄우기. axios로 django 연결
onMounted(async () => {
  const { data: keyRes } = await axios.get('/kakaomap/kakao-key/')
  const kakaoKey = keyRes.kakao_key
  await loadKakaoScript(kakaoKey)
  await nextTick()

  // 사용자 위치를 중심으로 지도 초기화
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(async (pos) => {
      const loc = new kakao.maps.LatLng(pos.coords.latitude, pos.coords.longitude)
      map = new kakao.maps.Map(document.getElementById('map'), {
        center: loc,
        level: 4
      })
      new kakao.maps.Marker({ map, position: loc })
    })
  } else {
    map = new kakao.maps.Map(document.getElementById('map'), {
      center: new kakao.maps.LatLng(37.49818, 127.027386),
      level: 3
    })
  }

  // 드롭다운의 구성 json파일로 부터
  const { data } = await axios.get('/static/kakaomap/data.json')
  dataStore.mapInfo = data.mapInfo || []
  dataStore.bankInfo = data.bankInfo || []
})

function updateGugunList() {
  const selected = dataStore.mapInfo.find((region) => region.name === sido.value)
  dataStore.gugunList = selected?.countries || []
}

// 수동 현위치 이동 버튼
function goToMyLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition((pos) => {
      const loc = new kakao.maps.LatLng(pos.coords.latitude, pos.coords.longitude)
      new kakao.maps.Marker({ map, position: loc })
      map.setCenter(loc)
      map.setLevel(4)
    })
  } else {
    alert('위치 정보를 사용할 수 없습니다.')
  }
}

function search() {
  const query = `${sido.value} ${gugun.value} ${bank.value}`
  const ps = new kakao.maps.services.Places()
  const bounds = new kakao.maps.LatLngBounds()

  // 기존 마커 제거
  markers.forEach((m) => m.setMap(null))
  markers = []
  selectedPlace.value = null

  ps.keywordSearch(query, (result, status) => {
    if (status === kakao.maps.services.Status.OK) {
      result.forEach((place) => {
        const latlng = new kakao.maps.LatLng(place.y, place.x)

        const marker = new kakao.maps.Marker({
          map,
          position: latlng
        })

        // 마커 클릭 시 인포윈도우 + 줌
        kakao.maps.event.addListener(marker, 'click', () => {
          // 이전 선택 마커 원복
          if (selectedMarker && selectedMarker.setImage) {
            selectedMarker.setImage(null)
          }

          // 현재 선택 마커 강조
          const imageSrc = 'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png'
          const imageSize = new kakao.maps.Size(24, 35)
          const markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize)
          marker.setImage(markerImage)
          selectedMarker = marker

          // 상세 정보 카드에 표시
          selectedPlace.value = place

          map.setCenter(marker.getPosition())
          map.setLevel(3)
        })

        markers.push(marker)
        bounds.extend(latlng)
      })
      map.setBounds(bounds)
    } else {
      alert('장소를 찾을 수 없습니다.')
    }
  })
}
</script>
