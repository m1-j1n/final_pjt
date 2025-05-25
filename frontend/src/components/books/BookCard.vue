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
  <div class="flex-grow-1 h-100 d-flex flex-column justify-content-start align-self-start">
    <div class="info-wrapper me-3">
      <router-link
        :to="{ name: 'books-detail', params: { bookId: book.id } }"
        class="text-dark text-decoration-none"
      >
        <h5 class="card-title text-truncate-2">
          {{ book.title }}
        </h5>
        <p class="card-text mb-1">{{ book.author }} | {{ book.pub_date }} | {{ book.publisher }}</p>
        <p class="card-text mb-1">{{ book.description.slice(0, 50) }}{{ book.description.length > 50 ? '...' : '' }}</p>
      </router-link>
    </div>
  </div>
  
    <!-- 버튼 영역 -->
    <div class="button-column ms-2 d-flex flex-column justify-content-center gap-2">
      <button
        class="btn btn-like d-flex align-items-center justify-content-center gap-1"
        :class="liked ? 'liked' : 'not-liked'"
        @click.stop.prevent="toggleLike"
      >
        <i class="bi bi-heart-fill" v-if="liked"></i>
        <i class="bi bi-heart" v-else></i>
        <span>❤️ 읽고싶어요 {{ likeCount }}</span>
      </button>

      <button class="btn btn-record d-flex align-items-center justify-content-center gap-1" @click.prevent="openModal">
        <i class="bi bi-journal-text"></i>
        <span>✏️ 독서 기록하기</span>
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
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/users.js'
import BookCardModal from '@/components/books/BookCardModal.vue'
import axios from 'axios'
import Swal from 'sweetalert2'

const props = defineProps({
  book: Object
})
const book = props.book
const router = useRouter()

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
    if (err.response?.status === 401) {
      Swal.fire({
        icon: 'info',
        title: '🛑 로그인 먼저 🛑',
        text: '이 책이 맘에 들었다면, 로그인하고 찜해보세요 ✨',
        confirmButtonText: '로그인하러 가기',
        showCancelButton: true,
        cancelButtonText: '나중에 할게요',
      }).then((result) => {
        if (result.isConfirmed) {
          router.push({ name: 'login' })
        }
      })
    } else {
      console.error('좋아요 실패:', err)
    }
  }
}

// 모달 처리
const showModal = ref(false)
const selectedBookId = ref(null)

const openModal = () => {
  if (!userStore.token) {
    Swal.fire({
      icon: 'info',
      title: '📝 독서 기록은 로그인 후에 📝',
      text: '로그인하면 독서 기록을 남길 수 있어요 ✨',
      confirmButtonText: '지금 로그인하기',
      showCancelButton: true,
      cancelButtonText: '나중에 할게요',
    }).then((result) => {
      if (result.isConfirmed) {
        router.push({ name: 'login' })
      }
    })
    return
  }

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

.button-column .btn {
  white-space: nowrap;
  padding: 0.4rem 0.8rem;
  font-size: 0.85rem; /* 기존보다 약간 작은 크기 */
  min-width: 130px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.like-btn,
.record-btn {
  white-space: nowrap;         /* 줄바꿈 금지 */
  overflow: hidden;            /* 넘치는 텍스트 숨기기 */
  text-overflow: ellipsis;     /* 넘치면 ... 표시 */
  font-size: 0.9rem;
  padding: 0.4rem 0.4rem;
  max-width: 100%;             /* 필요 시 지정 가능 */
}

.liked {
  background-color: #dc3545;
  color: #fff;
  border: none;
}

.not-liked {
  background-color: #fff;
  color: #dc3545;
  border: 1px solid #dc3545;
}

.not-liked:hover {
  background-color: #ffe5e9;
}

.btn-record {
  background-color: #f8f9fa;
  border: 1px solid #198754;
  color: #198754;
}

.btn-record:hover {
  background-color: #e6f4ea;
}
</style>