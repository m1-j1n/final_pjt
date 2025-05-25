<template>
  <div v-if="book" class="container py-4">

    <!-- 책 정보 섹션 -->
    <h5 class="fw-bold mb-3">📘 책 정보</h5>
    <div class="row g-4 align-items-start">
      <!-- 책 표지 -->
      <div class="col-md-3 text-center">
        <img :src="book.cover" class="img-fluid rounded shadow-sm book-cover" alt="도서 표지" />
      </div>

      <!-- 책 텍스트 정보 -->
      <div class="col-md-9">
        <h4 class="fw-semibold mb-2">{{ book.title }}</h4>
        <p class="mb-1 text-muted">{{ book.author }} 지음</p>
        <p class="mb-1"><strong>출판사:</strong> {{ book.publisher }}</p>
        <p class="mb-1"><strong>출판일:</strong> {{ book.pub_date }}</p>
        <p class="mb-1"><strong>ISBN:</strong> {{ book.isbn }}</p>
        <p class="mb-1"><strong>평점:</strong> ⭐ {{ book.customer_review_rank }}</p>
        <p class="mt-3 text-muted" style="line-height: 1.7;">{{ book.description }}</p>
      </div>
    </div>

    <!-- 작가 정보 섹션 -->
    <div class="mt-5">
      <h5 class="fw-bold mb-3">👤 작가 정보</h5>
      <div class="row g-3 align-items-center">
        <div class="col-3 text-center">
          <img :src="book.author_photo" class="author-photo shadow-sm" alt="작가 사진" />
        </div>
        <div class="col-9">
          <h6 class="fw-semibold mb-2">{{ book.author }}</h6>
          <p class="text-muted" style="line-height: 1.7;">{{ book.author_info }}</p>
        </div>
      </div>
    </div>

  </div>

  <div v-else class="text-center mt-5">
    <p>📖 도서 정보를 불러오는 중입니다...</p>
  </div>

  <div class="mt-5">
  <h5 class="fw-bold mb-3">📝 이 책과 관련된 포스트</h5>

  <div v-if="relatedPosts.length">
    <div class="row row-cols-1 row-cols-md-2 g-3">
      <div class="col" v-for="post in relatedPosts" :key="post.id">
        <RouterLink :to="{ name: 'posts-detail', params: { postId: post.id } }" class="text-decoration-none text-dark">
          <div class="card h-100 shadow-sm">
            <img :src="getImageUrl(post.cover_img)" class="card-img-top" alt="포스트 이미지" style="height: 200px; object-fit: cover;" />
            <div class="card-body">
              <h6 class="fw-bold">{{ post.title }}</h6>
              <p class="text-muted small">{{ post.content.slice(0, 80) }}...</p>
            </div>
          </div>
        </RouterLink>
      </div>
    </div>
  </div>
  <p v-else class="text-muted">아직 이 책에 대한 포스트가 없습니다.</p>
</div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

const route = useRoute()
const bookId = route.params.bookId
const book = ref(null)
const relatedPosts = ref([])

const getImageUrl = (path) => {
  if (!path) return 'https://via.placeholder.com/400x300?text=No+Image'
  return `http://localhost:8000${path}`
}


const fetchRelatedPosts = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/api/v1/books/${bookId}/posts/list/`)
    relatedPosts.value = res.data
  } catch (err) {
    console.error('📌 관련 포스트 불러오기 실패:', err)
  }
}

onMounted(async () => {
  try {
    const res = await axios.get(`http://localhost:8000/api/v1/books/${bookId}/`)
    book.value = res.data
  } catch (err) {
    console.error('도서 상세 조회 실패:', err)
  }

  await fetchRelatedPosts()
})
</script>

<style scoped>
.book-cover {
  max-height: 300px;
  object-fit: contain;
  border-radius: 8px;
}

.author-photo {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
}
</style>