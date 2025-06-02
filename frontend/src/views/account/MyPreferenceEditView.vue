<template>
  <div class="container py-5" style="max-width: 700px">
    <div class="card shadow p-4">
      <h4 class="mb-4 text-center">📘 설문 정보 수정</h4>

      <form @submit.prevent="submit">
        <!-- 라이프스타일 -->
        <div class="mb-3">
          <label class="form-label">라이프스타일</label>
          <div class="d-flex flex-wrap gap-2">
            <label v-for="item in lifestyles" :key="item.id"
              class="badge rounded-pill bg-light text-dark border px-3 py-2">
              <input type="checkbox" v-model="form.lifestyles" :value="item.id" hidden />
              {{ item.name }}
            </label>
          </div>
        </div>

        <!-- 독서 스타일 -->
        <div class="mb-3">
          <label class="form-label">독서 스타일</label>
          <div class="d-flex flex-wrap gap-2">
            <label v-for="item in readingStyles" :key="item.id"
              class="badge rounded-pill bg-light text-dark border px-3 py-2">
              <input type="checkbox" v-model="form.preferred_reading_styles" :value="item.id" hidden />
              {{ item.name }}
            </label>
          </div>
        </div>

        <!-- 관심 장르 -->
        <div class="mb-3">
          <label class="form-label">관심 장르</label>
          <div class="d-flex flex-wrap gap-2">
            <label v-for="item in categories" :key="item.id"
              class="badge rounded-pill bg-primary-subtle text-primary-emphasis border px-3 py-2">
              <input type="checkbox" v-model="form.interested_genres" :value="item.id" hidden />
              {{ item.name }}
            </label>
          </div>
        </div>

        <!-- 비선호 장르 -->
        <div class="mb-3">
          <label class="form-label">비선호 장르</label>
          <div class="d-flex flex-wrap gap-2">
            <label v-for="item in categories" :key="item.id"
              class="badge rounded-pill bg-danger-subtle text-danger-emphasis border px-3 py-2">
              <input type="checkbox" v-model="form.avoided_genres" :value="item.id" hidden />
              {{ item.name }}
            </label>
          </div>
        </div>

        <!-- 기피 키워드 -->
        <div class="mb-3">
          <label class="form-label">기피 키워드</label>
          <div class="d-flex flex-wrap gap-2">
            <label v-for="item in avoidedKeywords" :key="item.id"
              class="badge rounded-pill bg-warning-subtle text-dark border px-3 py-2">
              <input type="checkbox" v-model="form.avoided_keywords" :value="item.id" hidden />
              {{ item.name }}
            </label>
          </div>
        </div>

        <!-- 숫자 입력 -->
        <div class="row">
          <div class="col-md-6 mb-3">
            <label class="form-label">주간 평균 독서 시간 (시간)</label>
            <input type="number" class="form-control" v-model.number="form.weekly_avg_reading_time" />
          </div>
          <div class="col-md-6 mb-3">
            <label class="form-label">연간 목표 독서량 (권)</label>
            <input type="number" class="form-control" v-model.number="form.annual_reading_amount" />
          </div>
        </div>

        <button type="submit" class="btn btn-primary w-100 mt-3">수정 완료</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const API_URL = 'http://13.124.181.201:8000/api/v1/accounts'

const lifestyles = ref([])
const readingStyles = ref([])
const categories = ref([])
const avoidedKeywords = ref([])

const form = ref({
  lifestyles: [],
  preferred_reading_styles: [],
  interested_genres: [],
  avoided_genres: [],
  avoided_keywords: [],
  weekly_avg_reading_time: 0,
  annual_reading_amount: 0,
})

onMounted(async () => {
  const headers = { Authorization: `Token ${localStorage.getItem('token')}` }
  const [life, read, cat, avoid, user] = await Promise.all([
    axios.get(`${API_URL}/lifestyles/`, { headers }),
    axios.get(`${API_URL}/readingstyles/`, { headers }),
    axios.get('http://13.124.181.201:8000/api/v1/categories/', { headers }),
    axios.get(`${API_URL}/avoided-keywords/`, { headers }),
    axios.get(`${API_URL}/mypage/`, { headers })
  ])
  lifestyles.value = life.data
  readingStyles.value = read.data
  categories.value = cat.data
  avoidedKeywords.value = avoid.data

  const pref = user.data.preference
  if (pref) {
    form.value.lifestyles = pref.lifestyles.map(x => x.id)
    form.value.preferred_reading_styles = pref.preferred_reading_styles.map(x => x.id)
    form.value.interested_genres = pref.interested_genres.map(x => x.id)
    form.value.avoided_genres = pref.avoided_genres.map(x => x.id)
    form.value.avoided_keywords = pref.avoided_keywords.map(x => x.id)
    form.value.weekly_avg_reading_time = pref.weekly_avg_reading_time
    form.value.annual_reading_amount = pref.annual_reading_amount
  }
})

const submit = async () => {
  try {
    await axios.put(`${API_URL}/preference/`, form.value, {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`
      }
    })
    alert('설문 정보가 수정되었습니다.')
    router.push({ name: 'mypage' })
  } catch (err) {
    alert('수정 실패')
  }
}
</script>

<style scoped>
.badge input[type='checkbox']+span {
  cursor: pointer;
}

.badge input[type='checkbox']:checked+span {
  background-color: #ffc107 !important;
  color: white;
}
</style>
