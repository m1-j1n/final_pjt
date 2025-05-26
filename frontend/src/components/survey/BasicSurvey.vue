<!-- src/components/survey/BasicSurvey.vue -->
<template>
  <div class="survey-step">
    <h2 class="question">{{ question }}</h2>

    <div class="options-grid">
      <div
        v-for="(item, index) in options"
        :key="index"
        :class="['option-card', modelValue === item.value ? 'selected' : '']"
        @click="$emit('update:modelValue', item.value)"
      >
        <span class="label-text">{{ item.label }}</span>
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
  padding: 5vh 1rem;
}

.question {
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 2.5rem;
  color: #333;
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  max-width: 700px;
  margin: 0 auto;
}

.option-card {
  background: #fdfdfd;
  border-radius: 1.2rem;
  padding: 1.2rem;
  border: 2px solid transparent;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
  transition: all 0.2s ease;
  cursor: pointer;
}

.option-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0,0,0,0.08);
}

.option-card.selected {
  border-color: #6c63ff;
  background: #f0edff;
  transform: scale(1.02);
}

.label-text {
  font-size: 1.05rem;
  color: #444;
}
</style>
