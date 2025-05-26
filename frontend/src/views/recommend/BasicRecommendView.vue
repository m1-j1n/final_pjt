<template>
  <div class="container py-5">
    <h2 class="text-center fw-bold mb-5">📚 당신을 위한 책 추천</h2>

    <!-- 🔄 로딩 중 -->
    <div v-if="isLoading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3 text-muted">추천 결과를 생성 중입니다...</p>
    </div>

    <!-- ✅ 추천 결과 -->
    <div v-else-if="books.length" class="d-flex flex-column align-items-center gap-4">
      <div class="d-flex flex-wrap justify-content-center gap-4 w-100">
        <BookRecommendCard v-for="(book, index) in books.slice(currentIndex, currentIndex + 2)" :key="book.id || index"
          :book="book" />
      </div>

      <div class="d-flex justify-content-between mt-4 w-100" style="max-width: 800px">
        <button class="btn btn-outline-secondary" @click="prev" :disabled="currentIndex === 0">이전</button>
        <button class="btn btn-primary" @click="next" :disabled="currentIndex + 2 >= books.length">다음</button>
      </div>
    </div>

    <!-- 📭 책 없음 -->
    <div v-else class="text-center text-muted">
      추천된 책이 없습니다.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import BookRecommendCard from '@/components/recommend/BookRecommendCard.vue'

const route = useRoute()
const books = ref([])
const currentIndex = ref(0)
const isLoading = ref(true)

onMounted(async () => {
  isLoading.value = true
  try {
    const answers = route.query
    const res = await axios.post('http://localhost:8000/api/v1/recommend/basic/', {
      answers
    })
    books.value = res.data.recommended_books
  } catch (err) {
    console.error('❌ 추천 실패:', err)
  } finally {
    isLoading.value = false
  }
})

const next = () => {
  if (currentIndex.value + 2 < books.value.length) {
    currentIndex.value += 2
  }
}

const prev = () => {
  if (currentIndex.value >= 2) {
    currentIndex.value -= 2
  }
}
</script>

<style scoped>
.container {
  max-width: 1200px;
}
</style>
