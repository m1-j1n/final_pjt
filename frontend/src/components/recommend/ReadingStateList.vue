<template>
  <div class="container mt-5">
    <h2 class="mb-4 fw-bold">현재 읽고 있는 책과 유사한 추천 도서</h2>

     <!-- GPT 추천 멘트 -->
     <p v-if="recommendSummary" class="text-muted fst-italic mb-4 px-2">
      📌 {{ recommendSummary }}
    </p>

    <div v-if="recommendedBooks.length">
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

    <div v-else class="text-center mt-4 text-muted">
      <p>추천 도서를 불러오는 중입니다.</p>
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
  
  onMounted(() => {
    axios.get('http://localhost:8000/api/v1/recommend/content-based/', {
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
  })
  </script>
