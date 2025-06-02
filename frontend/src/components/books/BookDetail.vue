<template>
  <div v-if="book" class="container py-5">

    <!-- 📘 책 정보 -->
    <section class="mb-5">
      <h5 class="fw-bold mb-4">책 정보</h5>
      <div class="row g-4">
        <div class="col-md-3">
          <img :src="book.cover" class="img-fluid rounded shadow-sm" alt="도서 표지" />
        </div>
        <div class="col-md-9">
          <h4 class="fw-bold mb-2">{{ book.title }}</h4>
          <p class="mb-1 text-muted">{{ book.author }} 지음</p>
          <p class="mb-1 text-secondary"><strong>출판사:</strong> {{ book.publisher }}</p>
          <p class="mb-1 text-secondary"><strong>출판일:</strong> {{ book.pub_date }}</p>
          <p class="mb-1 text-secondary"><strong>ISBN:</strong> {{ book.isbn }}</p>
          <p class="mb-1 text-secondary"><strong>평점:</strong> ⭐ {{ book.customer_review_rank }}</p>
          <p class="mt-3 text-muted lh-lg">{{ book.description }}</p>
        </div>
      </div>
    </section>
    <hr>

    <!-- 👤 작가 정보 -->
    <section class="my-5">
      <h5 class="fw-bold mb-4">작가 정보</h5>
      <div class="d-flex align-items-start gap-4">
        <img
          :src="book.author_photo || 'https://www.gravatar.com/avatar/?d=mp'"
          class="rounded shadow-sm"
          style="width: 120px; height: 120px; object-fit: cover;"
          alt="작가 사진"
        />
        <div>
          <h6 class="fw-bold">{{ book.author }}</h6>
          <p class="text-muted lh-lg mb-0">{{ book.author_info }}</p>
        </div>
      </div>
    </section>
    <hr>

    <!-- 📝 관련 포스트 -->
    <section class="mt-5">
      <h5 class="fw-bold mb-4">이 책과 관련된 포스트</h5>
      <div v-if="relatedPosts.length" class="row row-cols-1 row-cols-md-2 g-4">
        <div class="col" v-for="post in relatedPosts" :key="post.id">
          <RouterLink
            :to="{ name: 'posts-detail', params: { postId: post.id } }"
            class="text-decoration-none text-dark"
          >
            <div class="card h-100 border-0 shadow-sm rounded-4">
              <img
                :src="getImageUrl(post.cover_img)"
                class="card-img-top rounded-top-4"
                alt="포스트 이미지"
                style="height: 180px; object-fit: cover;"
              />
              <div class="card-body">
                <h6 class="fw-semibold mb-2 text-truncate">{{ post.title }}</h6>
                <p class="text-muted small lh-sm">{{ post.content.slice(0, 80) }}...</p>
              </div>
            </div>
          </RouterLink>
        </div>
      </div>
      <p v-else class="text-muted mt-3">아직 이 책에 대한 포스트가 없습니다.</p>
    </section>

  </div>

  <!-- 📖 로딩 중 -->
  <div v-else class="text-center mt-5">
    <p class="text-muted">📖 도서 정보를 불러오는 중입니다...</p>
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
  return `http://13.124.181.201:8000${path}`
}


const fetchRelatedPosts = async () => {
  try {
    const res = await axios.get(`http://13.124.181.201:8000/api/v1/books/${bookId}/posts/list/`)
    relatedPosts.value = res.data
  } catch (err) {
    console.error('📌 관련 포스트 불러오기 실패:', err)
  }
}

onMounted(async () => {
  try {
    const res = await axios.get(`http://13.124.181.201:8000api/v1/books/${bookId}/`)
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