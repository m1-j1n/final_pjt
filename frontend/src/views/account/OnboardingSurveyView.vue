<template>
  <div class="onboarding-survey">
    <!-- 인트로 화면: 설문 시작 전만 표시 -->
    <section class="intro" v-if="!showSurvey">
      <img src="https://cdn-icons-png.flaticon.com/512/3062/3062634.png" alt="책 읽는 캐릭터" class="character" />
      <h2>나의 도서 취향은?</h2>
      <p>
        당신에게 꼭 맞는 책을 추천드리기 위해<br />
        <strong>간단한 설문</strong>을 준비했어요.
      </p>
      <button @click="showSurvey = true">설문 시작하기</button>
    </section>

    <!-- 설문 폼: 버튼 누르면 표시 -->
    <OnBoardingSurveyForm v-if="showSurvey" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import OnBoardingSurveyForm from '@/components/survey/OnBoardingSurvey.vue'

const showSurvey = ref(false)
</script>

<style scoped>
.onboarding-survey {
  max-width: 1000px;
  margin: 4rem auto;
  padding: 2rem;
  text-align: center;
  animation: fade-in 0.8s ease-in;
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.intro {
  padding: 4rem 2rem;
  border-radius: 1.5rem;
  background: linear-gradient(135deg, #fff8f2, #fffaf6);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  animation: fade-in 1s ease;
}

.character {
  width: 140px;
  margin-bottom: 1.5rem;
  animation: float 2.5s ease-in-out infinite;
}

@keyframes float {
  0% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
  100% {
    transform: translateY(0);
  }
}

h2 {
  font-size: 2.2rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #222;
}

p {
  font-size: 1.25rem;
  color: #555;
  line-height: 1.8;
  margin-bottom: 2.5rem;
}

button {
  padding: 0.9rem 2.2rem;
  background-color: #f8a33b;
  border: none;
  border-radius: 9999px;
  font-size: 1.1rem;
  font-weight: bold;
  color: #fff;
  cursor: pointer;
  transition: background-color 0.3s, box-shadow 0.3s ease;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
}

button:hover {
  background-color: #f29b2f;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
}
</style>
