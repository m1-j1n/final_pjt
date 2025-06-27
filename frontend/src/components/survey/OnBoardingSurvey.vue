<template>
  <div class="survey-wrapper">
    <!-- 완료 화면 -->
    <div v-if="isComplete" class="end-screen">
      <h2>🎉 설문 완료!</h2>
      <p>회원가입이 끝났어요. 지금 바로 다양한 책을 만나보세요.</p>
      <button @click="goToLogin">로그인하러 가기</button>
    </div>

    <!-- 설문 진행 화면 -->
    <div v-else>
      <div class="progress-container">
        <div class="progress-text">STEP {{ currentStep }} / 7</div>
        <div class="progress-track">
          <div class="progress-fill" :style="{ width: `${(currentStep) / 7 * 100}%` }"></div>
        </div>
      </div>

      <section class="question-box">
        <transition name="fade-slide" mode="out-in">
          <div :key="currentStep">
            <h3>{{ stepTitles[currentStep - 1] }}</h3>

            <div v-if="currentStep <= 5" class="choice-list">
              <label v-for="item in getCurrentOptions()" :key="item.id"
                     :class="['option-chip', { selected: form[stepKeys[currentStep - 1]].includes(item.id) }]">
                <input type="checkbox" :value="item.id" v-model="form[stepKeys[currentStep - 1]]" hidden />
                <span class="text">{{ item.name }}</span>
              </label>
            </div>

            <div v-if="currentStep === 6" class="input-step">
              <label class="input-label">일주일에 이 정도는 읽고 싶어요!</label>
              <input type="number" v-model.number="form.weekly_avg_reading_time" placeholder="예: 5 (시간)" />
            </div>

            <div v-if="currentStep === 7" class="input-step">
              <label class="input-label">한 달 동안 이 정도는 읽고 싶어요!</label>
              <input type="number" v-model.number="form.annual_reading_amount" placeholder="예: 8 (권)" />
            </div>

            <div class="nav-btns">
              <button @click="prevStep" :disabled="currentStep === 1">이전</button>
              <button v-if="currentStep < 7" @click="nextStep" :disabled="isNextDisabled">다음</button>
              <button v-else @click="submitSurvey">제출</button>
            </div>
          </div>
        </transition>
      </section>
    </div>
  </div>
</template>


<script setup>
import { API } from '@/api/api.js'
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
  '주간 독서 시간은?',
  '월간 목표 독서량은?',
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
    axios.get(API.ACCOUNT.LIFESTYLES),
    axios.get(API.ACCOUNT.READING_STYLES),
    axios.get(API.CATEGORY.LIST),
    axios.get(API.ACCOUNT.AVOIDED_KEYWORDS),
  ])
  lifestyles.value = life.data
  readingStyles.value = read.data
  categories.value = cat.data
  avoidedKeywords.value = avoid.data
})

const getCurrentOptions = () => {
  switch (currentStep.value) {
    case 1: return lifestyles.value
    case 2: return readingStyles.value
    case 3: return categories.value
    case 4: return categories.value
    case 5: return avoidedKeywords.value
    default: return []
  }
}

const isNextDisabled = computed(() => {
  if (currentStep.value <= 5) {
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
    await axios.put(API.ACCOUNT.PREFERENCE, form.value, {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`,
      },
    })
    isComplete.value = true
  } catch (err) {
    console.error('❌ 제출 오류:', err)
    alert('제출 실패!')
  }
}
const goToLogin = () => router.push({ name: 'login' })
</script>

<style scoped>
.survey-wrapper {
  max-width: 800px;
  margin: auto;
  padding: 4rem 2rem;
  font-family: 'Pretendard', sans-serif;
  color: #333;
}

/* ✅ 진행률 */
.progress-container {
  margin-bottom: 2.5rem;
}
.progress-text {
  text-align: center;
  margin-bottom: 0.4rem;
  font-weight: 500;
  color: #888;
}
.progress-track {
  height: 8px;
  background-color: #eee;
  border-radius: 999px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background-color: #ffc107; /* 단색으로 */
  transition: width 0.4s ease;
}

/* ✅ 질문 타이틀 */
.question-box h3 {
  text-align: center;
  font-size: 1.8rem;
  margin-bottom: 2rem;
}

/* ✅ 선택지 */
.choice-list {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 2rem;
}
.option-chip {
  padding: 0.8rem 1.5rem;
  border-radius: 999px;
  border: 1px solid #ccc;
  background-color: #f9f9f9;
  transition: all 0.2s ease;
  cursor: pointer;
  white-space: normal;            /* ✅ 줄바꿈 허용 */
  overflow: visible;              /* ✅ 생략 안되게 */
  max-width: 240px;
  text-align: center;
}
.option-chip.selected {
  background-color: #ffc107;
  color: white;
  font-weight: bold;
  border: none;
}

/* ✅ 숫자 입력 */
.input-step {
  text-align: center;
  margin-bottom: 2rem;
}
.input-label {
  display: block;
  font-size: 1.1rem;
  margin-bottom: 1rem;
}
.input-step input {
  width: 60%;
  max-width: 280px;
  padding: 0.8rem;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 1rem;
}

/* ✅ 버튼 */
.nav-btns {
  margin-top: 2rem;
  display: flex;
  justify-content: center;
  gap: 1rem;
}
button {
  background-color: #222;
  color: white;
  border: none;
  padding: 0.9rem 1.8rem;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
button:hover {
  background-color: #444;
}
button:disabled {
  background-color: #bbb;
  cursor: not-allowed;
}

/* ✅ 완료 화면 */
.end-screen {
  text-align: center;
  padding: 5rem 2rem;
}
.end-screen h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
}
.end-screen p {
  font-size: 1.1rem;
  color: #666;
}
.end-screen button {
  margin-top: 2rem;
  background-color: #ffc107;
  border: none;
  padding: 1rem 2rem;
  border-radius: 999px;
  font-size: 1rem;
  font-weight: bold;
  color: white;
  cursor: pointer;
}
.end-screen button:hover {
  opacity: 0.9;
}

/* ✅ 전환 효과 */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.5s ease;
}
.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>



