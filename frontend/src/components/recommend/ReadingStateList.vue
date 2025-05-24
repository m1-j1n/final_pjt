<template>
    <div class="container mt-5">
      <h2 class="mb-4 fw-bold">📚 현재 읽고 있는 책과 유사한 추천 도서</h2>
  
      <div v-if="recommendedBooks.length">
        <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
          <div class="col" v-for="book in recommendedBooks" :key="book.id">
            <RouterLink :to="{ name: 'books-detail', params: { bookId: book.id } }" class="text-decoration-none">
              <div class="card h-100">
                <img :src="book.cover" class="card-img-top" :alt="book.title" />
                <div class="card-body">
                  <h5 class="card-title">{{ book.title }}</h5>
                  <p class="card-text text-muted">{{ book.author }}</p>
                </div>
              </div>
            </RouterLink>
          </div>
        </div>
      </div>
  
      <div v-else>
        <p>추천 도서를 불러오는 중이거나 없습니다.</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useUserStore } from '@/stores/users.js'
  import axios from 'axios'
  
  const recommendedBooks = ref([])
  const userStore = useUserStore()
  
  onMounted(() => {
  axios.get('http://localhost:8000/api/v1/recommend/content-based/', {
        headers: {
        Authorization: `Token ${userStore.token}`
        }
    })
    .then(res => {
        console.log('✅ 추천 도서 응답:', res.data)
        recommendedBooks.value = res.data
    })
    .catch(err => {
        console.error('❗ 추천 실패:', err)
    })
    })
  </script>