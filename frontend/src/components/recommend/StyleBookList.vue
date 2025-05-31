<template>
  <div class="container mt-5">
    <h2 class="mb-4 fw-bold">이런 책들이 회원님의 스타일과 잘 어울려요</h2>

    <div v-if="recommendationSummary" class="alert alert-light">
      <p class="mb-0">
        {{ name }}님은 <strong>{{ genres }}</strong> 장르를 선호하고,
        <strong>{{ styles }}</strong>
      </p>
    </div>

    <div v-if="recommendedBooks.length" class="row row-cols-1 row-cols-md-3 g-4 mt-3">
      <div v-for="book in recommendedBooks" :key="book.id" class="col">
        <RouterLink
          :to="{ name: 'books-detail', params: { bookId: book.id } }"
          class="text-decoration-none"
        >
          <div class="card h-100 shadow-sm">
            <img
              :src="book.cover"
              class="card-img-top"
              :alt="book.title"
              style="height: 300px; object-fit: cover;"
            />
            <div class="card-body">
              <h5 class="card-title text-truncate">{{ book.title }}</h5>
              <p class="card-text text-muted">{{ book.author }}</p>
              <p class="card-text small text-muted">{{ book.publisher }} · {{ book.pub_date }}</p>
            </div>
          </div>
        </RouterLink>
      </div>
    </div>

    <p v-else class="text-muted mt-3">아직 추천 도서가 없습니다.</p>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useUserStore } from '@/stores/users.js'

const userStore = useUserStore()
const recommendedBooks = ref([])
const recommendationSummary = ref(null)
const name = userStore.username

const genres = computed(() =>
  recommendationSummary.value?.preferred_genres?.join(', ') || '관심 장르 정보 없음'
)

const styles = computed(() =>
  recommendationSummary.value?.preferred_reading_styles?.join(', ') || '선호 스타일 없음'
)

const avoids = computed(() =>
  recommendationSummary.value?.avoided_keywords?.join(', ') || '기피 키워드 없음'
)

onMounted(async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/v1/recommend/personal/', {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`,
      },
    })
    recommendedBooks.value = res.data.books
    recommendationSummary.value = res.data.recommendation_summary
  } catch (err) {
    console.error('추천 도서 불러오기 실패:', err)
  }
})
</script>

<style scoped>
.card-title {
  font-size: 1rem;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
