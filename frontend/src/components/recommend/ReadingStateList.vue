<template>
  <div class="container mt-5">
    <h2 class="mb-4 fw-bold">현재 읽고 있는 책과 유사한 추천 도서</h2>

    <!-- GPT 추천 멘트 -->
    <p v-if="recommendSummary" class="alert alert-light text-muted fst-italic mb-4 px-2">
      📌 {{ recommendSummary }}
    </p>

    <!-- 📖 로딩 상태 -->
    <div v-if="isLoading" class="loading-area text-center py-5">
      <div class="book-spinner fs-1">📖</div>
      <p class="loading-text text-muted mt-3">당신의 책을 찾고 있어요<span class="dot-animation">...</span></p>
    </div>

    <!-- 📚 추천 도서 -->
    <div v-else-if="recommendedBooks.length">
      <div class="row row-cols-2 row-cols-sm-3 row-cols-md-4 row-cols-lg-5 g-3">
        <div class="col" v-for="book in recommendedBooks" :key="book.id">
          <RouterLink
            :to="{ name: 'books-detail', params: { bookId: book.id } }"
            class="text-decoration-none"
          >
            <div class="card h-100 shadow-sm">
              <img
                :src="book.cover"
                class="card-img-top book-cover"
                :alt="book.title"
              />
              <div class="card-body px-2 py-2 d-flex flex-column justify-content-between">
                <div>
                  <h6 class="card-title text-truncate mb-1">{{ book.title }}</h6>
                  <p class="card-text text-muted small mb-1">{{ book.author }}</p>
                </div>
              </div>
            </div>
          </RouterLink>
        </div>
      </div>
    </div>

    <!-- 추천 없음 -->
    <div v-else class="text-center mt-4 text-muted">
      <p>추천 도서를 찾지 못했어요.</p>
    </div>
  </div>
</template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useUserStore } from '@/stores/users.js'
  import { useRouter } from 'vue-router'
  import axios from 'axios'
  import Swal from 'sweetalert2'
  
  const recommendedBooks = ref([])
  const recommendSummary = ref('')
  const userStore = useUserStore()
  const router = useRouter()
  const isLoading = ref(true)
  
  onMounted(() => {
    axios.get('http://13.124.181.201:8000/api/v1/recommend/content-based/', {
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
    .then(res => {
      console.log('✅ 추천 도서 응답:', res.data)
      recommendedBooks.value = res.data.books
      recommendSummary.value = res.data.summary
  
      // 📌 추천 결과가 비었을 경우
      if (res.data.books.length === 0) {
        Swal.fire({
          icon: 'info',
          title: '추천 도서가 아직 없어요',
          text: '책을 읽고 독서 상태를 기록하면, 더 정확한 추천이 가능해져요.',
          confirmButtonText: '독서 기록하러 가기',
          showCancelButton: true,
          cancelButtonText: '닫기',
          buttonsStyling: false,
          customClass: {
            confirmButton: 'btn btn-dark rounded-pill px-4 me-2',
            cancelButton: 'btn btn-outline-secondary rounded-pill px-4',
            popup: 'rounded-4',
          },
        }).then(result => {
          if (result.isConfirmed) {
            router.push({ name: 'books' })
          }
        })
      }
    })
    .catch(err => {
      console.error('❗ 추천 실패:', err)
    })
    .finally(() => {
    isLoading.value = false 
  })
  })
  </script>

<style scoped>
.book-spinner {
  animation: bounce 1s infinite;
}
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

.dot-animation::after {
  content: '';
  display: inline-block;
  animation: dots 1.5s infinite steps(3, jump-none);
  width: 1em;
  text-align: left;
}

@keyframes dots {
  0% { content: ''; }
  33% { content: '.'; }
  66% { content: '..'; }
  100% { content: '...'; }
}
</style>