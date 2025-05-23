<template>
  <div class="card flex-row p-3" style="height: 180px; max-width: 720px;">
    <!-- 책 표지 -->
    <router-link
      :to="{ name: 'books-detail', params: { bookId: book.id } }"
      class="book-cover-wrapper me-3 text-decoration-none"
    >
      <img :src="book.cover" class="book-cover" alt="도서 표지" />
    </router-link>

    <!-- 도서 정보 -->
    <div class="flex-grow-1 h-100 d-flex flex-column justify-content-between">
      <div class="info-wrapper me-3">
        <router-link
          :to="{ name: 'books-detail', params: { bookId: book.id } }"
          class="text-dark text-decoration-none"
        >
        <h5 class="card-title text-truncate-2">
            {{ book.title }}
          </h5>
          <p class="card-text mb-1">{{ book.author }} | {{ book.pub_date }} | {{ book.publisher }} </p>
          <p class="card-text mb-1">{{ book.description.slice(0, 50) }}{{ book.description.length > 50 ? '...' : '' }}</p>
        </router-link>
      </div>
    </div>
    <!-- 버튼 영역 -->
    <div class="button-column ms-2">
      <button class="btn btn-outline-danger mb-1" @click.stop.prevent="toggleLike">
        <span class="fs-6">
          ❤️ 읽고싶어요 {{ likeCount }}
        </span>
      </button>
      <button class="btn btn-outline-success" @click.prevent="openModal">
        <span class="fs-6">
          ✏️ 독서 기록하기
        </span>
      </button>
    </div>
  </div>

    <!-- 모달 컴포넌트 -->
    <BookCardModal
    v-if="showModal"
    :book-id="selectedBookId"
    @close="closeModal"
    @saved="handleSave"
  />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/users.js'
import BookCardModal from '@/components/books/BookCardModal.vue'
import axios from 'axios'

const props = defineProps({
  book: Object
})
const book = props.book

// 좋아요 처리 
const liked = ref(false)
const likeCount = ref(0)
const userStore = useUserStore()

const toggleLike = async () => {
  try {
    const res = await axios.post(
      `http://localhost:8000/api/v1/books/${book.id}/like/`,
      {},
      {
        headers: {
          Authorization: `Token ${userStore.token}`
        }
      }
    )
    
    const updatedBook = res.data.book
    liked.value = updatedBook.liked
    likeCount.value = updatedBook.like_count

    Object.assign(book, updatedBook)

  } catch (err) {
    console.error('좋아요 실패:', err)
  }
}

// 모달 처리
const showModal = ref(false)
const selectedBookId = ref(null)

const openModal = () => {
  console.log('모달 열기')
  selectedBookId.value = book.id
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

// 📌 저장 이벤트에서 axios 요청 수행
const handleSave = async ({ bookId, data }) => {
  try {
    const res = await axios.post(
      `http://localhost:8000/api/v1/books/${bookId}/reading-status/`,
      data,
      {
        headers: {
          Authorization: `Token ${userStore.token}`,
        },
      }
    )
    console.log('저장 성공:', res.data)
  } catch (err) {
    console.error('저장 실패:',err.response?.data)
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