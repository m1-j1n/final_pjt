<!-- components/SurveyStep.vue -->
<template>
  <div class="survey-step">
    <h2 class="question">{{ question }}</h2>

    <div class="options-grid">
      <div v-for="(item, idx) in options" :key="idx"
        :class="['option-card', modelValue === item.value ? 'selected' : '']"
        @click="$emit('update:modelValue', item.value)">
        <div class="emoji-wrapper">
          <div class="emoji-circle">🙂</div> <!-- 이모지는 나중에 -->
          <span class="label-text">{{ item.label }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  question: String,
  options: Array,
  modelValue: String
})

defineEmits(['update:modelValue'])
</script>

<style scoped>
.survey-step {
  text-align: center;
}

.question {
  font-size: 1.4rem;
  margin-bottom: 1.5rem;
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  max-width: 700px;
  margin: 0 auto;
}

.option-card {
  background: #f9f9f9;
  border-radius: 1rem;
  padding: 0.8rem;
  cursor: pointer;
  border: 2px solid transparent;
  display: flex;
  align-items: center;
  justify-content: center;
}

.option-card.selected {
  border-color: #5c6bc0;
  background: #e8eaf6;
}

.emoji-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.emoji-circle {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.label-text {
  font-size: 0.9rem;
}
</style>
