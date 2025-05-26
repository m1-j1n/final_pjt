<template>
  <div class="survey-container">
    <BasicSurvey v-if="currentStep === 1" question="요즘 어떠세요?" :options="moodOptions" v-model="answers.mood" />
    <BasicSurvey v-else-if="currentStep === 2" question="요즘 가장 관심 있는 것은 무엇인가요?" :options="interestOptions"
      v-model="answers.interest" />
    <BasicSurvey v-else-if="currentStep === 3" question="선호하는 책은 어떤 스타일인가요?" :options="styleOptions"
      v-model="answers.style" />
    <BasicSurvey v-else-if="currentStep === 4" question="책을 읽는 이유는 무엇인가요?" :options="reasonOptions"
      v-model="answers.reason" />




    <div class="buttons">
      <button @click="prevStep" :disabled="currentStep === 1">뒤로가기</button>
      <button @click="nextStep" :disabled="!currentAnswerSelected">다음</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import BasicSurvey from '@/components/survey/BasicSurvey.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const currentStep = ref(1)

const answers = ref({
  mood: '',
  interest: '',
  style: '',
  reason: ''
})


const moodOptions = [
  { label: '동기부여가 필요해요', value: 'motivation' },
  { label: '답답해요', value: 'frustrated' },
  { label: '일상의 재미를 원해요', value: 'fun' },
  { label: '불안해요', value: 'anxiety' },
  { label: '달달한 로맨스를 원해요', value: 'romance' },
  { label: '기분전환이 필요해요', value: 'refresh' },
  { label: '떠나고 싶어요', value: 'travel' },
  { label: '힐링이 필요해요', value: 'healing' },
  { label: '고민이 있어요', value: 'worry' }
]

const interestOptions = [
  { label: '심리', value: 'psychology' },
  { label: '경제', value: 'economy' },
  { label: '요리', value: 'cooking' },
  { label: '음악', value: 'music' },
  { label: '여행', value: 'travel' },
  { label: '관계소통', value: 'communication' },
  { label: '미술', value: 'art' },
  { label: '자아찾기', value: 'identity' },
  { label: '자녀교육', value: 'parenting' }
]

const styleOptions = [
  { label: '힐링', value: 'healing' },
  { label: '몰입', value: 'immersion' },
  { label: '지적 자극', value: 'intellectual' },
  { label: '가볍게 읽기', value: 'light' },
  { label: '울컥한 감동', value: 'touching' },
  { label: '실용', value: 'practical' },
  { label: '트렌디', value: 'trendy' },
  { label: '차분함', value: 'calm' },
  { label: '상상력 자극', value: 'imaginative' }
]


const reasonOptions = [
  { label: '스트레스를 해소하고 싶어서', value: 'stress' },
  { label: '스스로를 성장시키고 싶어서', value: 'growth' },
  { label: '그냥 재미있으니까요!', value: 'fun' },
  { label: '일이나 공부에 도움이 되니까', value: 'work' },
  { label: '생각을 정리하고 싶어서', value: 'thinking' },
  { label: '감정을 느끼고 싶어서', value: 'emotion' },
  { label: '책을 좋아하니까요', value: 'love' },
  { label: '습관적으로요', value: 'habit' },
  { label: '현실을 잊고 싶어서', value: 'escape' }
]


const currentAnswerSelected = computed(() => {
  switch (currentStep.value) {
    case 1: return answers.value.mood
    case 2: return answers.value.interest
    case 3: return answers.value.style
    case 4: return answers.value.reason
    default: return false
  }
})

const nextStep = () => {
  if (currentStep.value < 4) {
    currentStep.value++
  } else {
    router.push({
      name: 'basic-recommend',
      query: answers.value  // query로 전달
    })
  }
}
const prevStep = () => {
  if (currentStep.value > 1) currentStep.value--
}


</script>

<style scoped>
.survey-container {
  padding: 2rem;
}

.buttons {
  margin-top: 2rem;
  display: flex;
  justify-content: space-between;
}
</style>
