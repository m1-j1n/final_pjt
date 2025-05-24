<template>
  <router-link
    :to="{ name: 'books-detail', params: { bookId: book.id } }"
    class="card flex-row align-items-start p-3 text-dark text-decoration-none"
    style="height: 180px; max-width: 720px; position: relative;"
  >
    <!-- 책 표지 -->
    <div class="book-cover-wrapper me-3">
      <img
        :src="book.cover"
        class="book-cover"
        alt="도서 표지"
      />
    </div>

    <!-- 도서 정보 -->
    <div class="flex-grow-1 h-100 d-flex flex-column justify-content-between">
      <div class="info-wrapper me-3"> 
        <h5 class="card-title text-truncate-2">{{ book.title }}</h5>
        <p class="card-text mb-1">{{ book.author }} | {{ book.pub_date }} | {{ book.publisher}} </p>
        <p class="card-text mb-1">{{ book.description.slice(0, 50) }}{{ book.description.length > 50 ? '...' : '' }}</p>
      </div>
    </div>

    <!-- 버튼 영역 -->
    <div class="button-column ms-2">
      <button class="btn btn-outline-danger mb-1" @click.stop.prevent="toggleLike">
        ❤️ {{ likeCount }}
      </button>
      <button class="btn btn-outline-success mb-1" @click.stop.prevent="markAsRead">
        ✅ 읽었어요
      </button>
      <button class="btn btn-outline-primary" @click.stop.prevent="markAsReading">
        📖 읽고있어요
      </button>
    </div>
  </router-link>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios';

const props = defineProps({
  book: Object
})
const book = props.book

// 좋아요 처리 
const liked = ref(false)
const likeCount = ref(0)

const toggleLike = async () => {
  try {
    const res = await axios.post(`http://localhost:8000/api/v1/books/${book.id}/like/`)
    
    const updatedBook = res.data.book
    liked.value = updatedBook.liked
    likeCount.value = updatedBook.like_count

    Object.assign(book, updatedBook)

  } catch (err) {
    console.error('좋아요 실패:', err)
  }
}

onMounted(() => {
  if (book && book.id) {
    likeCount.value = book.like_count || 0
    liked.value = book.liked || false
  }
})

</script>

<style scoped>
/* 두 줄 말줄임 처리 */
.book-cover-wrapper {
  width: 120px;
  height: 160px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  /* border: 1px solid #ddd; */
  /* border-radius: 4px; */
}

.book-cover {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.info-wrapper {
  flex-grow: 1;
  min-width: 0;
  max-width: 100%;
}

.card-title {
  font-size: 1.1rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  word-wrap: break-word;
  white-space: normal;
}

.button-column {
  width: 120px; /* 너비 고정 */
  height: 160px; /* 이미지 높이 등과 맞춤 */
  display: flex;
  flex-direction: column;
  justify-content: center;
  flex-shrink: 0; /* 줄어들지 않게 */
}
</style>