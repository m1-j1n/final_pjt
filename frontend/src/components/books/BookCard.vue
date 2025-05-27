<template>
  <div class="book-card-wrapper text-center">
    <!-- 책 표지 + 버튼 -->
    <div class="cover-wrapper position-relative">
      <img :src="book.cover" class="cover-img" alt="도서 표지" />
      <div class="cover-overlay d-flex align-items-center justify-content-center">
        <h5 class="cover-title text-white text-center px-2">{{ book.title }}</h5>
      </div>

      <!-- 버튼 아이콘 (우측 하단 고정) -->
      <div class="action-buttons position-absolute bottom-0 end-0 d-flex gap-2 p-2">
        <!-- ❤️ 하트 버튼 -->
        <button
          class="btn btn-icon-soft"
          :class="liked ? 'btn-liked' : 'btn-unliked'"
          @click.stop.prevent="toggleLike"
        >
          ❤️
        </button>

        <!-- ✏️ 기록 버튼 -->
        <button
          class="btn btn-icon-soft"
          :class="readingStatus ? 'btn-recorded' : 'btn-unrecorded'"
          @click.stop.prevent="openModal"
        >
          ✏️
        </button>
      </div>

      <!-- 라우터 링크는 표지 전체에 -->
      <RouterLink
        :to="{ name: 'books-detail', params: { bookId: book.id } }"
        class="router-cover-link"
      ></RouterLink>
    </div>

      <!-- 작가 정보 -->
      <div class="author-info mt-2 d-flex justify-content-start align-items-center">
        <img
          :src="book.author_photo || 'https://placehold.co/40x40?text=Author'"
          alt="작가"
          class="me-2"
          style="width: 36px; height: 36px; object-fit: cover; border-radius: 8px;"
        />

        <div class="d-flex flex-column justify-content-start">
          <p class="author-name text-muted text-truncate mb-0 text-start" style="max-width: 120px;">
            {{ book.author }}
          </p>
          <small class="text-muted text-truncate text-start" style="max-width: 120px;">
            {{ book.pub_date }}
          </small>
        </div>
      </div>


    <!-- 모달 -->
    <BookCardModal
      v-if="showModal && modalType === 'create'"
      :book-id="selectedBookId"
      @close="closeModal"
      @saved="handleSave"
    />
    <BookCardUpdateModal
      v-if="showModal && modalType === 'edit'"
      :book-id="selectedBookId"
      :initial-data="readingStatus"
      @close="closeModal"
      @updated="handleSave"
      @deleted="handleDelete"
    />
  </div>
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
        icon: 'warning',
        title: '로그인이 필요합니다',
        text: '이 책을 찜하시려면 로그인해주세요.',
        confirmButtonText: '로그인',
        showCancelButton: true,
        cancelButtonText: '취소',
        buttonsStyling: false,
        customClass: {
          confirmButton: 'btn btn-dark rounded-pill px-4 me-2',
          cancelButton: 'btn btn-outline-secondary rounded-pill px-4',
          popup: 'rounded-4',
        },
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
      icon: 'warning',
      title: '독서 기록은 로그인 후에 가능해요',
      text: '로그인하면 독서 활동을 저장하고 관리할 수 있어요.',
      confirmButtonText: '로그인',
      showCancelButton: true,
      cancelButtonText: '닫기',
      buttonsStyling: false,
      customClass: {
        confirmButton: 'btn btn-dark rounded-pill px-4 me-2',
        cancelButton: 'btn btn-outline-secondary rounded-pill px-4',
        popup: 'rounded-4',
      },
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

    // ✅ 상태 즉시 반영 (GET 요청 생략)
    readingStatus.value = { ...readingStatus.value, ...data }

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
.book-card-wrapper {
  display: block;
  max-width: 200px;
  transition: all 0.3s ease;
}

.cover-wrapper {
  position: relative;
  height: 280px;
  border-radius: 12px;
  overflow: hidden;
  background-color: #fff;
  border: 1px solid #eee;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: box-shadow 0.2s ease-in-out;
}

.cover-wrapper:hover {
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
}

.cover-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: 0.3s ease;
}

.cover-overlay {
  position: absolute;
  inset: 0;
  background-color: rgba(0, 0, 0, 0);
  transition: background-color 0.3s ease;
  opacity: 0;
}

.book-card-wrapper:hover .cover-img {
  filter: brightness(60%);
}

.book-card-wrapper:hover .cover-overlay {
  opacity: 1;
  background-color: rgba(0, 0, 0, 0.5);
}

.cover-title {
  font-size: 1rem;
  font-weight: 600;
}

.router-cover-link {
  position: absolute;
  inset: 0;
  z-index: 0;
}

/* ❤️ ✏️ 버튼 공통 스타일 */
.btn-icon-soft {
  padding: 6px 10px;
  font-size: 16px;
  border-radius: 12px;
  background-color: #ffffffcc; /* 살짝 투명한 흰색 배경 */
  border: 1px solid #dee2e6;
  color: #495057;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: background-color 0.2s ease, box-shadow 0.2s ease;
  backdrop-filter: blur(4px); /* 자연스러운 유리 느낌 */
}

.btn-icon-soft:hover {
  background-color: #f1f3f5cc;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
}

/* ❤️ 좋아요 active */
.btn-liked {
  background-color: #ffe5e9;           /* 부드러운 연핑크 */
  color: #d6336c;                      /* 살짝 선명한 핑크 텍스트 */
  border: 1px solid #f8cfd7;           /* 테두리도 살짝 연핑크 */
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05); /* 은은한 그림자 */
  transition: all 0.2s ease-in-out;
}

.btn-liked:hover {
  background-color: #fddbe3;
  color: #c2255c;
  border-color: #f3bac9;
}

.btn-unliked {
  background-color: rgba(0, 0, 0, 0.1);  /* 불투명도 ↑ */
  color: #6c757d;
  border: 1px solid #d6dbe1;
}

.btn-unliked:hover {
  background-color: rgba(0, 0, 0, 0.15); /* hover 시 더 진하게 */
  color: #495057;
  border-color: #cbd2da;
}

.btn-recorded {
  background-color: #e2f4ea;           /* 산뜻한 민트톤 */
  color: #198754;                      /* 중간 녹색 */
  border: 1px solid #b7e1cb;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease-in-out;
}

.btn-recorded:hover {
  background-color: #d5ecdf;
  color: #157347;
  border-color: #a9d9bc;
}

.btn-unrecorded {
  background-color: rgba(0, 0, 0, 0.1);     /* 불투명한 회색 배경 */
  color: #6c757d;                           /* 중간 회색 텍스트 */
  border: 1px solid #d6dbe1;               /* 연한 회색 테두리 */
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: background-color 0.2s ease, box-shadow 0.2s ease;
}

.btn-unrecorded:hover {
  background-color: rgba(0, 0, 0, 0.15);    /* hover 시 살짝 더 진하게 */
  color: #495057;
  border-color: #cbd2da;
}

/* 하단 버튼 정렬 */
.action-buttons {
  z-index: 2;
}

/* 작가 정보 */
.author-info {
  margin-top: 0.5rem;
}

.author-name {
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
