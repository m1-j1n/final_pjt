<template>
  <div class="onboarding-survey">
    <!-- 인트로 화면: 설문 시작 전만 표시 -->
    <section class="intro" v-if="!showSurvey">
      <img src="" alt="책 읽는 캐릭터" class="character" />
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
}

.intro {
  padding: 3rem 2rem;
  border-radius: 1rem;
  background-color: #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.character {
  width: 120px;
  margin-bottom: 1rem;
}

h2 {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 0.8rem;
  color: #222;
}

p {
  font-size: 1.1rem;
  color: #555;
  line-height: 1.6;
  margin-bottom: 2rem;
}

button {
  padding: 0.75rem 2rem;
  background-color: #ffcb05;
  border: none;
  border-radius: 9999px;
  font-size: 1rem;
  font-weight: bold;
  color: #000;
  cursor: pointer;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #e0b800;
}
</style>
