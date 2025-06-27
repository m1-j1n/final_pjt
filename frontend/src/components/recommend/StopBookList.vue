<template>
  <div class="container my-5">
    <h2 class="mb-4 fw-bold">많은 사람들이 읽다 그만둔 책</h2>
    <div class="alert alert-light">
      <p class="mb-0">
        사람들은 
        <strong>어떤 이유로</strong>
        책 읽기를 멈췄을까요?
      </p>
    </div>
    <!-- 데이터가 있을 때만 카드 보여줌 -->
    <div v-if="droppedBooks.length" class="row row-cols-1 row-cols-md-3 g-4">
      <div
        v-for="(book, index) in droppedBooks.slice(0, 3)"
        :key="index"
        class="col"
        style="min-height: 600px;"
      >
        <RouterLink
          :to="{ name: 'books-detail', params: { bookId: book.book_id } }"
          class="text-decoration-none"
        >
          <div class="card h-100 shadow-sm">
            <img
              :src="book.book_cover"
              alt="책 표지"
              class="card-img-top object-fit-cover"
              style="height: 400px"
            />
            <div class="card-body">
              <h5 class="card-title">{{ book.book_title }}</h5>
              <p class="card-text text-muted">"{{ book.stop_reason }}"</p>
            </div>
          </div>
        </RouterLink>
      </div>

    </div>

    <!-- 데이터가 없을 경우 -->
    <p v-else class="text-muted">아직 중단된 책 데이터가 없습니다.</p>
  </div>
</template>

<script setup>
import { API } from '@/api/api.js'
import { ref, onMounted } from 'vue'
import axios from 'axios'

const droppedBooks = ref([])

onMounted(async () => {
  try {
    const res = await axios.get(API.RECOMMEND.DROPPED_BOOKS)
    droppedBooks.value = res.data
  } catch (err) {
    console.error('❌ 중단된 책 데이터 불러오기 실패:', err)
  }
})
</script>

<style scoped>
.object-fit-cover {
  object-fit: cover;
}
</style>
