<template>
  <div v-if="book">
    <div class="row">
      <div class="col-md-4">
        <img :src="book.cover" class="img-fluid" alt="도서 표지" />
      </div>
      <div class="col-md-8">
        <div class="row">
          <h2>{{ book.title }}</h2>
          <p><strong>저자:</strong> {{ book.author }}</p>
          <p><strong>출판사:</strong> {{ book.publisher }}</p>
          <p><strong>출판일:</strong> {{ book.pub_date }}</p>
          <p><strong>ISBN:</strong> {{ book.isbn }}</p>
          <p><strong>고객 리뷰 평점:</strong> {{ book.customer_review_rank }}</p>
          <p class="mt-3">{{ book.description }}</p>
        </div>
      </div>
    </div>

    <div class="row mt-3">
      <h5><strong>작가정보</strong></h5>
    </div>

    <div class="row">
      <div class="col-3">
        <img :src="book.author_photo" class="rounded-circle" alt="">
      </div>
      <div class="col-9">
        <div class="row fw-bold fs-4">
          {{ book.author }} 
        </div>
        <div class="row mt-2">
          {{ book.author_info }}
        </div>
      </div>
    </div>
  </div>

  <div v-else class="text-center mt-5">
    <p>📖 도서 정보를 불러오는 중입니다...</p>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

const route = useRoute()
const bookId = route.params.bookId
const book = ref(null)
console.log('라우트 파라미터:', route.params)

onMounted(async () => {
  try {
    const res = await axios.get(`http://localhost:8000/api/v1/books/${bookId}/`)
    console.log('book 데이터:', res.data)
    book.value = res.data
  } catch (err) {
    console.error('도서 상세 조회 실패:', err)
  }
})
</script>

<style scoped></style>