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
      <div
        v-for="(book, i) in books.slice(0, 3)"
        :key="book.id"
        :class="['book-section', i % 2 === 0 ? 'light' : 'soft-bg', 'row', 'flex-lg-row', 'flex-column', 'align-items-center', 'mb-5']"
      >
        <div class="col-lg-6 text-start">
          <span class="badge bg-light text-dark mb-2">추천 도서</span>
          <h3 class="book-title">{{ book.title }}</h3>
          <p class="book-desc">{{ truncateWords(book.description, 20) }}</p>

          <button class="btn-detail" @click="goToDetail(book.id)">이 책이 더 궁금하다면? →</button>
        </div>
        <div class="col-lg-6 text-center mt-4 mt-lg-0">
          <img :src="book.cover" class="book-image" :alt="book.title" />
        </div>
      </div>
    </div>

    <!-- 책 없음 -->
    <!-- <div v-else class="text-center text-muted mt-5">
      추천된 책이 없습니다.
    </div> -->
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const books = ref([])
const isLoading = ref(true)

onMounted(async () => {
  isLoading.value = true
  try {
    const answers = route.query
    const res = await axios.post('http://13.124.181.201:8000/api/v1/recommend/basic/', { answers })
    books.value = res.data.recommended_books

    // 📌 추천 결과가 없다면 랜덤 3권 요청
    if (!books.value.length) {
      const fallback = await axios.get('http://13.124.181.201:8000/api/v1/books/random/?count=3')
      books.value = fallback.data
    }
  } catch (err) {
    console.error('❌ 추천 실패:', err)
  } finally {
    isLoading.value = false
  }
})


const goToDetail = (bookId) => {
  if (bookId) router.push({ name: 'books-detail', params: { bookId } })
}

const truncateWords = (text, maxWords) => {
  if (!text) return ''
  const words = text.trim().split(/\s+/)  // 공백 기준으로 단어 나눔
  console.log('📚 단어 수:', words.length)

  return words.length > maxWords
    ? words.slice(0, maxWords).join(' ') + '...'
    : text
    
}


</script>

<style scoped>
.recommend-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 5vh 2rem;
  font-family: 'Pretendard', sans-serif;
  color: #333;
}

.title {
  font-size: 2.2rem;
  font-weight: bold;
  margin-bottom: 3rem;
  text-align: center;
  color: #222;
}

.book-section {
  padding: 4rem 2rem;
  border-radius: 1.2rem;
  margin-bottom: 3rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}

.book-section.light {
  background-color: #fff9f4;
}

.book-section.soft-bg {
  background-color: #f3efe8;
}

.book-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #222;
  margin-bottom: 1rem;
  word-break: keep-all;
}

.book-desc {
  font-size: 1.1rem;
  color: #555;
  line-height: 1.7;
  word-break: keep-all;
}

.book-image {
  width: 85%;
  max-width: 300px;
  height: auto;
  margin: 0 auto;
  display: block;
  border-radius: 1rem;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
}

.badge {
  font-size: 0.85rem;
  font-weight: 500;
  padding: 0.4rem 0.9rem;
  border-radius: 999px;
  background-color: #fff;
  border: 1px solid #ccc;
}

.btn-detail {
  margin-top: 1.4rem;
  padding: 0.6rem 1.6rem;
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

/* 로딩 화면 */
.loading-area {
  height: 60vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.book-spinner {
  font-size: 4.5rem;
  animation: spin 2s linear infinite;
  margin-bottom: 1.2rem;
  text-align: center;
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
