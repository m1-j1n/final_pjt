<template>
  <div class="survey-wrapper">
    <!-- ✅ 항상 보여지는 상단 문구 -->
    <div class="survey-header">
      <h1>📖 오늘의 당신에게</h1>
      <p class="description">
        지금의 기분, 관심사, 스타일을 알려주시면<br />
        당신에게 어울리는 책을 찾아드릴게요.
      </p>
    </div>

    <!-- 시작 화면 -->
    <transition name="fade-slide" mode="out-in" v-if="!started" >
      <div v-if="!started" key="start" class="start-screen">
        <button class="start-btn" @click="started = true">시작하기</button>
      </div>
    </transition>


    <!-- 설문 흐름 -->
    <div v-if="started" class="questions-flow">
      <div
        v-for="(question, index) in questions.slice(0, currentStep + 1)"
        :key="question.key"
        class="question-block"
        :class="{ blurred: index < currentStep }"
        :ref="el => questionRefs[index] = el"
      >
        <h3 class="question-text">{{ question.text }}</h3>
        <div class="option-list">
          <button
            v-for="option in question.options"
            :key="option.value"
            :class="['option-btn', { selected: answers[question.key] === option.value }]"
            @click="selectAnswer(index, question.key, option.value)"
          >
            {{ option.label }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const started = ref(false)
const currentStep = ref(0)
const questionRefs = []

const answers = ref({
  mood: '',
  interest: '',
  style: '',
  reason: ''
})

const questions = [
  { key: 'mood', text: '당신의 오늘은 어떤 색인가요?', options: [
    { label: '동기부여가 필요해요', value: 'motivation' },
    { label: '답답해요', value: 'frustrated' },
    { label: '일상의 재미를 원해요', value: 'fun' },
    { label: '불안해요', value: 'anxiety' },
    { label: '달달한 로맨스를 원해요', value: 'romance' },
    { label: '기분전환이 필요해요', value: 'refresh' },
    { label: '떠나고 싶어요', value: 'travel' },
    { label: '힐링이 필요해요', value: 'healing' },
    { label: '고민이 있어요', value: 'worry' }
  ]},
  { key: 'interest', text: '요즘 가장 관심 있는 주제는 무엇인가요?', options: [
    { label: '심리', value: 'psychology' },
    { label: '경제', value: 'economy' },
    { label: '요리', value: 'cooking' },
    { label: '음악', value: 'music' },
    { label: '여행', value: 'travel' },
    { label: '관계소통', value: 'communication' },
    { label: '미술', value: 'art' },
    { label: '자아찾기', value: 'identity' },
    { label: '자녀교육', value: 'parenting' }
  ]},
  { key: 'style', text: '어떤 스타일의 책이 당신에게 잘 맞나요?', options: [
    { label: '힐링', value: 'healing' },
    { label: '몰입', value: 'immersion' },
    { label: '지적 자극', value: 'intellectual' },
    { label: '가볍게 읽기', value: 'light' },
    { label: '울컥한 감동', value: 'touching' },
    { label: '실용', value: 'practical' },
    { label: '트렌디', value: 'trendy' },
    { label: '차분함', value: 'calm' },
    { label: '상상력 자극', value: 'imaginative' }
  ]},
  { key: 'reason', text: '책을 읽는 이유, 무엇인가요?', options: [
    { label: '스트레스를 해소하고 싶어서', value: 'stress' },
    { label: '스스로를 성장시키고 싶어서', value: 'growth' },
    { label: '그냥 재미있으니까요!', value: 'fun' },
    { label: '일이나 공부에 도움이 되니까', value: 'work' },
    { label: '생각을 정리하고 싶어서', value: 'thinking' },
    { label: '감정을 느끼고 싶어서', value: 'emotion' },
    { label: '책을 좋아하니까요', value: 'love' },
    { label: '습관적으로요', value: 'habit' },
    { label: '현실을 잊고 싶어서', value: 'escape' }
  ]}
]

const selectAnswer = async (index, key, value) => {
  if (answers.value[key] === value) {
    answers.value[key] = ''
    currentStep.value = index
    await nextTick()
    questionRefs[index]?.scrollIntoView({ behavior: 'smooth', block: 'center' })
    return
  }

  answers.value[key] = value
  if (index < questions.length - 1) {
    currentStep.value++
    await nextTick()
    questionRefs[currentStep.value]?.scrollIntoView({ behavior: 'smooth', block: 'center' })
  } else {
    router.push({ name: 'basic-recommend', query: answers.value })
  }
}
</script>

<style scoped>
.survey-header {
  text-align: center;
  margin-bottom: 2rem;
}

.survey-header h1 {
  font-size: 1.8rem;
  color: #444;
  margin-bottom: 0.4rem;
}

.survey-header .description {
  font-size: 1.05rem;
  color: #666;
  line-height: 1.6;
  margin: 0 auto;
  max-width: 90%;
}


.survey-wrapper {
  max-width: 720px;
  margin: 0 auto;
  padding: 6vh 1rem;
  font-family: 'Noto Sans KR', sans-serif;
}

.start-screen {
  text-align: center;
  animation: fadeIn 1s ease forwards;
}

.description {
  color: #666;
  margin: 1rem 0 2rem;
  font-size: 1.1rem;
}

.start-btn {
  background-color: #f3a5c2;
  border: none;
  padding: 0.8rem 2rem;
  border-radius: 999px;
  font-size: 1.1rem;
  color: white;
  cursor: pointer;
  transition: 0.2s;
}
.start-btn:hover {
  background-color: #f087ae;
}

.questions-flow {
  display: flex;
  flex-direction: column;
  gap: 4rem;
}

.question-block {
  padding: 1.5rem;
  border-radius: 1rem;
  background: #fff8f9;
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.05);
  transition: filter 0.3s, opacity 0.3s;
}

.question-block.blurred {
  filter: blur(2px);
  opacity: 0.4;
  pointer-events: none;
}
.question-text {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
  text-align: center;
  color: #333;
}


.option-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  justify-content: center;
}


.option-btn {
  background: white;
  border: 2px solid #f3a5c2;
  border-radius: 999px;
  padding: 0.6rem 1.2rem;
  font-size: 0.95rem;
  color: #f087ae;
  cursor: pointer;
  transition: 0.2s;
}

.option-btn.selected,
.option-btn:hover {
  background-color: #f3a5c2;
  color: white;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.4s ease;
}
.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(20px);
}
.fade-slide-enter-to {
  opacity: 1;
  transform: translateY(0);
}
</style>
