<template>
  <div class="survey-wrapper">
    <!-- 엔딩 화면 -->
    <div v-if="isComplete" class="end-screen">
      <h2>설문이 완료되었습니다! 🎉</h2>
      <p>회원가입이 완료되었습니다. 로그인 후 다양한 서비스를 이용해보세요!</p>
      <button @click="goToLogin">로그인하러 가기</button>
    </div>

    <div v-else>
      <!-- 상단 진행률 바 -->
      <div class="progress-bar">
        <div class="fill" :style="{ width: `${(currentStep - 1) / 6 * 100}%` }"></div>
      </div>

      <section class="question-box">
        <h3>{{ stepTitles[currentStep - 1] }}</h3>

        <!-- 선택지: 공통 렌더링 방식 -->
        <transition name="fade-slide" mode="out-in">
          <div v-if="currentStep <= 5" :key="currentStep" class="choice-list">
            <label v-for="item in getCurrentOptions()" :key="item.id" :class="{
              'option-chip': true,
              selected: form[stepKeys[currentStep - 1]].includes(item.id),
            }">
              <input type="checkbox" :value="item.id" v-model="form[stepKeys[currentStep - 1]]" hidden />
              {{ item.name }}
            </label>
          </div>
        </transition>

        <!-- 숫자 입력 -->
        <div v-if="currentStep === 6" class="input-step">
          <input type="number" v-model.number="form.weekly_avg_reading_time" placeholder="주간 평균 독서 시간 (시간)" />
        </div>

        <div v-if="currentStep === 7" class="input-step">
          <input type="number" v-model.number="form.annual_reading_amount" placeholder="연간 목표 독서량 (권 수)" />
        </div>

        <div class="nav-btns">
          <button @click="prevStep" :disabled="currentStep === 1">이전</button>
          <button v-if="currentStep < 7" @click="nextStep" :disabled="isNextDisabled">
            다음
          </button>
          <button v-else @click="submitSurvey">제출</button>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const currentStep = ref(1)
const isComplete = ref(false)

const form = ref({
  lifestyles: [],
  preferred_reading_styles: [],
  interested_genres: [],
  avoided_genres: [],
  avoided_keywords: [],
  weekly_avg_reading_time: 0,
  annual_reading_amount: 0,
})

const stepTitles = [
  '당신의 라이프스타일은?',
  '당신의 독서 스타일은?',
  '관심 있는 장르는?',
  '비선호하는 장르는?',
  '피하고 싶은 키워드는?',
  '주간 평균 독서 시간은?',
  '연간 목표 독서량은?',
]

const stepKeys = [
  'lifestyles',
  'preferred_reading_styles',
  'interested_genres',
  'avoided_genres',
  'avoided_keywords',
]

const lifestyles = ref([])
const readingStyles = ref([])
const categories = ref([])
const avoidedKeywords = ref([])

onMounted(async () => {
  const [life, read, cat, avoid] = await Promise.all([
    axios.get('http://127.0.0.1:8000/api/v1/accounts/lifestyles/'),
    axios.get('http://127.0.0.1:8000/api/v1/accounts/readingstyles/'),
    axios.get('http://127.0.0.1:8000/api/v1/categories/'),
    axios.get('http://127.0.0.1:8000/api/v1/accounts/avoided-keywords/'),
  ])
  lifestyles.value = life.data
  readingStyles.value = read.data
  categories.value = cat.data
  avoidedKeywords.value = avoid.data
})

const getCurrentOptions = () => {
  if (currentStep.value === 1) return lifestyles.value
  if (currentStep.value === 2) return readingStyles.value
  if (currentStep.value === 3) return categories.value
  if (currentStep.value === 4) return categories.value
  if (currentStep.value === 5) return avoidedKeywords.value
  return []
}

const isNextDisabled = computed(() => {
  if (currentStep.value >= 1 && currentStep.value <= 5) {
    return form.value[stepKeys[currentStep.value - 1]].length === 0
  }
  if (currentStep.value === 6) return !form.value.weekly_avg_reading_time
  if (currentStep.value === 7) return !form.value.annual_reading_amount
  return false
})

const nextStep = () => {
  if (currentStep.value < 7) currentStep.value++
}

const prevStep = () => {
  if (currentStep.value > 1) currentStep.value--
}

const submitSurvey = async () => {
  try {
    const payload = { ...form.value }
    await axios.put('http://127.0.0.1:8000/api/v1/accounts/preference/', payload, {
      headers: {
        Authorization: `Token ${localStorage.getItem('access_token')}`,
      },
    })
    isComplete.value = true
  } catch (err) {
    console.error('❌ 제출 오류:', err.response?.data || err)
    alert('제출 실패!')
  }
}

const goToLogin = () => {
  router.push({ name: 'login' })
}
</script>

<style scoped>
.survey-wrapper {
  max-width: 1200px;
  margin: auto;
  padding: 4rem 2rem;
}

.progress-bar {
  height: 12px;
  background: #eee;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 3rem;
}

.progress-bar .fill {
  height: 100%;
  background-color: #ffc107;
  transition: width 0.3s ease;
}

.question-box h3 {
  margin-bottom: 2.2rem;
  font-size: 2rem;
  text-align: center;
  font-weight: 700;
}

.choice-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-bottom: 2.5rem;
}

.option-chip {
  padding: 1.6rem 2rem;
  border-radius: 3rem;
  border: 1px solid #ccc;
  font-size: 1rem;
  cursor: pointer;
  text-align: center;
  transition: background-color 0.2s, color 0.2s;
  background-color: #f9f9f9;
  white-space: normal;
  word-break: keep-all;
  min-height: 90px;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1.4;
}

.option-chip.selected {
  background-color: #ffc107;
  color: #fff;
  font-weight: bold;
}

.input-step input {
  width: 100%;
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 1.2rem;
}

.nav-btns {
  margin-top: 3rem;
  display: flex;
  justify-content: space-between;
  gap: 2rem;
}

button {
  padding: 1rem 2.5rem;
  font-size: 1.2rem;
  font-weight: 600;
  background-color: #444;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

/* 간단한 fade-slide 모션 */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.4s ease;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* 완료 화면 스타일 */
.end-screen {
  text-align: center;
  padding: 5rem 2rem;
}

.end-screen h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.end-screen p {
  font-size: 1.2rem;
  color: #555;
}

.end-screen button {
  margin-top: 2rem;
  padding: 1rem 2rem;
  font-size: 1rem;
  font-weight: bold;
  background-color: #ffc107;
  border: none;
  border-radius: 999px;
  cursor: pointer;
  color: black;
}

.end-screen button:hover {
  background-color: #e6b800;
}
</style>
