<template>
  <div class="survey-form">
    <h3>📘 추천을 위한 정보를 입력해주세요</h3>

    <form @submit.prevent="submitSurvey">
      <!-- 라이프스타일 -->
      <div class="form-group">
        <label for="lifestyle">당신의 라이프스타일은?</label>
        <select id="lifestyle" v-model="lifestyle" required>
          <!-- 여기! -->
          <option v-for="item in lifestyles" :key="item.id" :value="item.id">
            {{ item.name }}
          </option>
        </select>
      </div>

      <!-- 독서 스타일 -->
      <div class="form-group">
        <label for="readingStyle">당신의 독서 스타일은?</label>
        <select id="readingStyle" v-model="readingStyle" required>
          <option v-for="item in readingStyles" :key="item.id" :value="item.id">
            {{ item.name }}
          </option>
        </select>
      </div>

      <!-- 관심 장르 -->
      <div class="form-group">
        <label>관심 있는 장르를 선택하세요 (중복 가능)</label>
        <div class="checkbox-row">
          <label v-for="category in categories" :key="category.id" class="checkbox">
            <input type="checkbox" :value="category.id" v-model="interestedGenres" />
            {{ category.name }}
          </label>
        </div>
      </div>

      <!-- 주간 독서 시간 -->
      <div class="form-group">
        <label for="weeklyReadingTime">주간 평균 독서 시간 (시간)</label>
        <input type="number" id="weeklyReadingTime" v-model.number="weeklyReadingTime" min="0" required />
      </div>

      <!-- 연간 목표 권수 -->
      <div class="form-group">
        <label for="annualReadingAmount">올해 목표 독서량 (권)</label>
        <input type="number" id="annualReadingAmount" v-model.number="annualReadingAmount" min="0" required />
      </div>

      <button type="submit">제출하기</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

const lifestyle = ref('')
const readingStyle = ref('')
const interestedGenres = ref([])
const weeklyReadingTime = ref(0)
const annualReadingAmount = ref(0)
const categories = ref([])

const lifestyles = ref([])
const readingStyles = ref([])

onMounted(async () => {
  const [catRes, lifeRes, styleRes] = await Promise.all([
    axios.get('http://127.0.0.1:8000/api/v1/categories/'),
    axios.get('http://127.0.0.1:8000/api/v1/accounts/lifestyles/'),
    axios.get('http://127.0.0.1:8000/api/v1/accounts/readingstyles/'),
  ])

  categories.value = catRes.data
  lifestyles.value = lifeRes.data
  readingStyles.value = styleRes.data
})


const submitSurvey = async () => {
  const token = localStorage.getItem('access_token')

  const payload = {
    lifestyle: lifestyle.value,
    preferred_reading_style: readingStyle.value,
    interested_genres: interestedGenres.value,
    weekly_avg_reading_time: weeklyReadingTime.value,
    annual_reading_amount: annualReadingAmount.value,
  }

  try {
    await axios.put('http://127.0.0.1:8000/api/v1/accounts/preference/', payload, {

      headers: {
        Authorization: `Token ${token}`
      }
    })

    alert('🎉 설문이 완료되었습니다! 메인 페이지로 이동합니다.')
    router.push({ name: 'login' })
  } catch (err) {
    console.error('❌ 오류 응답 내용:', err.response?.data)
    alert('❌ 제출에 실패했습니다. 입력값을 다시 확인해주세요.')
  }

}
</script>

<style scoped>
.survey-form {
  max-width: 600px;
  margin: 3rem auto;
  padding: 2rem;
  background: #ffffff;
  border-radius: 1rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

h3 {
  text-align: center;
  font-size: 1.6rem;
  margin-bottom: 2rem;
  color: #333;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  font-weight: 600;
  display: block;
  margin-bottom: 0.6rem;
  color: #444;
}

input,
select {
  width: 100%;
  padding: 0.7rem;
  border: 1px solid #ccc;
  border-radius: 0.5rem;
  font-size: 1rem;
}

.checkbox-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem 1rem;
  margin-top: 0.5rem;
}

.checkbox {
  display: flex;
  align-items: center;
  font-size: 0.95rem;
  color: #333;
}

.checkbox input {
  margin-right: 0.4rem;
}

button[type="submit"] {
  width: 100%;
  padding: 0.8rem;
  background-color: #4caf50;
  color: white;
  font-size: 1.1rem;
  font-weight: bold;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button[type="submit"]:hover {
  background-color: #388e3c;
}
</style>
