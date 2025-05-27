<template>
  <div class="recommend-container">
    <h2 class="title">당신을 위한 책 추천</h2>

    <!-- 로딩 화면 -->
    <div v-if="isLoading" class="loading-area">
      <div class="book-spinner">📖</div>
      <p class="loading-text">당신의 책을 찾고 있어요<span class="dot-animation">...</span></p>
    </div>

    <!-- 추천 결과 -->
    <div v-else-if="books.length">
      <!-- 책 1 : 텍스트 왼쪽, 이미지 오른쪽 -->
      <div class="book-section light row flex-lg-row flex-column align-items-center mb-5">
        <div class="col-lg-6 text-start">
          <span class="badge bg-light text-dark mb-2">추천 도서</span>
          <h3 class="book-title">{{ books[currentIndex]?.title }}</h3>
          <p class="book-desc">{{ books[currentIndex]?.description }}</p>
          <button class="btn-detail" @click="goToDetail(books[currentIndex]?.id)">자세히 보기 →</button>
        </div>
        <div class="col-lg-6 text-center mt-4 mt-lg-0">
          <img :src="books[currentIndex]?.cover" class="book-image" alt="book" />
        </div>
      </div>

      <!-- 책 2 : 이미지 왼쪽, 텍스트 오른쪽 -->
      <div v-if="books[currentIndex + 1]" class="book-section soft-bg row flex-lg-row-reverse flex-column align-items-center mb-5">
        <div class="col-lg-6 text-start">
          <span class="badge bg-light text-dark mb-2">추천 도서</span>
          <h3 class="book-title">{{ books[currentIndex + 1]?.title }}</h3>
          <p class="book-desc">{{ books[currentIndex + 1]?.description }}</p>
          <button class="btn-detail" @click="goToDetail(books[currentIndex + 1]?.id)">자세히 보기 →</button>
        </div>
        <div class="col-lg-6 text-center mt-4 mt-lg-0">
          <img :src="books[currentIndex + 1]?.cover" class="book-image" alt="book" />
        </div>
      </div>

      <!-- 이전/다음 버튼 -->
      <div class="buttons d-flex justify-content-center gap-3">
        <button @click="prev" :disabled="currentIndex === 0" class="btn btn-outline-secondary">← 이전</button>
        <button @click="next" :disabled="currentIndex + 2 >= books.length" class="btn btn-primary">다음 →</button>
      </div>
    </div>

    <!-- 책 없음 -->
    <div v-else class="text-center text-muted mt-5">
      추천된 책이 없습니다.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const books = ref([])
const currentIndex = ref(0)
const isLoading = ref(true)

onMounted(async () => {
  isLoading.value = true
  try {
    const answers = route.query
    const res = await axios.post('http://localhost:8000/api/v1/recommend/basic/', { answers })
    books.value = res.data.recommended_books
  } catch (err) {
    console.error('❌ 추천 실패:', err)
  } finally {
    isLoading.value = false
  }
})

const next = () => {
  if (currentIndex.value + 2 < books.value.length) currentIndex.value += 2
}
const prev = () => {
  if (currentIndex.value >= 2) currentIndex.value -= 2
}
const goToDetail = (bookId) => {
  if (bookId) router.push({ name: 'books-detail', params: { bookId } })
}
</script>

<style scoped>
.recommend-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 5vh 2rem;
}

.title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 3rem;
  text-align: center;
  color: #222;
}

.book-section {
  padding: 4rem 2rem;
  border-radius: 1rem;
  margin-bottom: 3rem;
}

.book-section.light {
  background-color: #ffffff;
}

.book-section.soft-bg {
  background-color: #f7f3ee;
}

.book-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #222;
  margin-bottom: 1rem;
}

.book-desc {
  font-size: 1.1rem;
  color: #555;
  line-height: 1.6;
}

.book-image {
  width: 85%;
  max-width: 300px;
  height: auto;
  margin: 0 auto;
  display: block;
  border-radius: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.btn-detail {
  margin-top: 1.2rem;
  padding: 0.6rem 1.4rem;
  font-size: 1rem;
  font-weight: 600;
  color: white;
  background-color: #f8a33b;
  border: none;
  border-radius: 999px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-detail:hover {
  background-color: #e9962a;
}

.book-spinner {
  font-size: 5rem;
  animation: spin 2s linear infinite;
  margin-bottom: 1.2rem;
  text-align: center;
}

.loading-area {
  height: 60vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.loading-text {
  font-size: 1.4rem;
  text-align: center;
  color: #444;
}

.dot-animation::after {
  content: '';
  display: inline-block;
  animation: dots 1.5s steps(3, end) infinite;
}

@keyframes dots {
  0% { content: ''; }
  33% { content: '.'; }
  66% { content: '..'; }
  100% { content: '...'; }
}

@keyframes spin {
  from { transform: rotate(0); }
  to { transform: rotate(360deg); }
}
</style>