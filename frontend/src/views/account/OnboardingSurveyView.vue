<template>
  <div class="onboarding-survey">
    <section class="intro">
      <h2>🎉 회원가입이 완료되었습니다!</h2>
      <p>당신에게 꼭 맞는 책을 추천드리기 위해, <strong>간단한 설문</strong>을 진행합니다.</p>
    </section>

    <!-- 여기에 실제 설문 폼 컴포넌트를 삽입 -->
    <OnBoardingSurveyForm />
  </div>
</template>

<script setup>
import OnBoardingSurveyForm from '@/components/survey/OnBoardingSurvey.vue'  // 실제 설문 폼은 따로 구성할 예정
</script>

<style scoped>
.onboarding-survey {
  padding: 2rem;
  max-width: 800px;
  margin: auto;
}

.intro {
  text-align: center;
  margin-bottom: 2rem;
  background-color: #f0f8ff;
  padding: 1.5rem;
  border-radius: 1rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
.intro h2 {
  color: #333;
  margin-bottom: 0.5rem;
}
.intro p {
  color: #555;
  font-size: 1.1rem;
}
</style>
