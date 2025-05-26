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
        <span>
          {{ readingStatus ? '✏️ 독서 기록 수정하기' : '✏️ 독서 기록하기' }}
        </span>
      </button>
    </div>
  </div>

    <!-- 모달 컴포넌트 -->
    <BookCardModal
      v-if="showModal && modalType === 'create'"
      :book-id="selectedBookId"
      @close="closeModal"
      @saved="handleSave"
    />

    <!-- 수정 모달 -->
    <BookCardUpdateModal
      v-if="showModal && modalType === 'edit'"
      :book-id="selectedBookId"
      :initial-data="readingStatus"
      @close="closeModal"
      @updated="handleSave"
      @deleted="handleDelete"
    />

</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/users.js'
import BookCardModal from '@/components/books/BookCardModal.vue'
import BookCardUpdateModal from './BookCardUpdateModal.vue'
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
const readingStatus = ref(null)
const modalType = ref('create')

// 독서 기록하기 모달 관리
const openModal = async () => {
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

  try {
    const res = await axios.get(
      `http://localhost:8000/api/v1/books/${book.id}/reading-status/`,
      {
        headers: {
          Authorization: `Token ${userStore.token}`,
        },
      }
    )

    readingStatus.value = res.data
    modalType.value = 'edit'
    showModal.value = true
  } catch (err) {
    if (err.response?.status === 404) {
      // ✅ 기록 없음
      readingStatus.value = null
      modalType.value = 'create'
      showModal.value = true
    } else {
      console.error('기록 조회 실패:', err)
    }
  }
}

// 모달 닫는 창
const closeModal = () => {
  showModal.value = false
  readingStatus.value = null
  modalType.value = 'create'
}

// 📌 저장 이벤트에서 axios 요청 수행
const handleSave = async ({ bookId, data, mode }) => {
  try {
    const url = `http://localhost:8000/api/v1/books/${bookId}/reading-status/`
    const config = {
      headers: {
        Authorization: `Token ${userStore.token}`,
      },
    }

    let res
    if (mode === 'edit') {
      res = await axios.patch(url, data, config)
      Swal.fire({
        icon: 'success',
        title: '수정 완료!',
        text: '독서 기록이 수정되었습니다.',
        timer: 1500,
        showConfirmButton: false,
      })
    } else {
      res = await axios.post(url, data, config)
      Swal.fire({
        icon: 'success',
        title: '저장 완료!',
        text: '독서 기록이 저장되었습니다.',
        timer: 1500,
        showConfirmButton: false,
      })
    }
    const statusRes = await axios.get(url, config)
    readingStatus.value = statusRes.data
    console.log('저장 성공:', res.data)
    closeModal()
  } catch (err) {
    console.error(`${mode === 'edit' ? '수정' : '저장'} 실패:`, err.response?.data)
    Swal.fire({
      icon: 'error',
      title: '오류 발생',
      text: '저장 중 문제가 발생했습니다.',
    })
  }
}


// 독서 댓글 삭제
const handleDelete = () => {
  console.log('🗑 삭제 완료')
  Swal.fire({
    icon: 'info',
    title: '삭제 완료',
    text: '독서 기록이 삭제되었습니다.',
    timer: 1500,
    showConfirmButton: false,
  })
  readingStatus.value = null
  modalType.value = 'create'
  closeModal()
}


onMounted(async () => {
  if (book && book.id) {
    likeCount.value = book.like_count || 0
    liked.value = book.liked || false

    // ✅ 로그인한 유저의 독서 기록이 있는지 미리 확인
    if (userStore.token) {
      try {
        const res = await axios.get(
          `http://localhost:8000/api/v1/books/${book.id}/reading-status/`,
          {
            headers: {
              Authorization: `Token ${userStore.token}`,
            },
          }
        )
        readingStatus.value = res.data
        modalType.value = 'edit'
      } catch (err) {
        if (err.response?.status === 404) {
          readingStatus.value = null
          modalType.value = 'create'
        } else {
          console.error('초기 상태 조회 실패:', err)
        }
      }
    }
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