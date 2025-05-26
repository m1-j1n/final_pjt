<template>
  <div class="container mt-5">
    <h2 class="mb-4 fw-bold">📚 회원님의 스타일과 어울리는 도서 리스트</h2>

    <div v-if="recommendedBooks.length" class="row row-cols-1 row-cols-md-3 g-4">
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

    <p v-else class="text-muted">아직 추천 도서가 없습니다.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const recommendedBooks = ref([])

onMounted(async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/v1/recommend/personal/', {
      headers: {
        Authorization: `Token ${localStorage.getItem('access_token')}`,
      },
    })
    recommendedBooks.value = res.data
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
