<template>
  <div class="container mt-4">
    <h3 class="mb-3">📚 카테고리별 스레드 보기</h3>

    <!-- 카테고리 버튼 -->
    <div class="mb-4 d-flex flex-wrap gap-2">
      <button v-for="category in categories" :key="category.pk" class="btn"
        :class="category.pk === selectedCategory ? 'btn-primary' : 'btn-outline-primary'"
        @click="selectedCategory = category.pk">
        {{ category.fields.name }}
      </button>
    </div>

    <!-- 필터링된 스레드 카드 -->
    <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
      <div class="col" v-for="thread in filteredThreads" :key="thread.id">
        <RouterLink :to="{ name: 'threads-detail', params: { threadId: thread.id } }"
          class="text-decoration-none text-dark">
          <div class="card h-100" style="cursor: pointer;">
            <img :src="getBookCover(thread.bookId)" class="card-img-top thread-image" :alt="thread.title" />
            <div class="card-body">
              <h5 class="card-title">{{ thread.title }}</h5>
              <p class="card-text">{{ thread.content }}</p>
            </div>
          </div>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useThreadStore } from '@/stores/threads'
import categories from '@/assets/data/categories.json'
import books from '@/assets/data/books.json'

const store = useThreadStore()
const threads = computed(() => store.threads)

const selectedCategory = ref(0)

// findBookById : bookId → book 객체를 찾는 도우미
const findBookById = (bookId) => {
  return books.find(book => book.pk === bookId)
}

// filteredThreads : 필터링된 스레드
const filteredThreads = computed(() => {
  if (selectedCategory.value === 0) return threads.value

  return threads.value.filter(thread => {
    const book = findBookById(thread.bookId)
    return book?.fields.category === selectedCategory.value
  })
})

// getBookCover: 책의 cover 이미지 찾기
const getBookCover = (bookId) => {
  const book = findBookById(bookId)
  return book?.fields.cover || 'https://via.placeholder.com/286x180.png?text=No+Image'
}


const formatDate = (iso) => {
  return new Date(iso).toLocaleString()
}
</script>

<style scoped>
.card {
  min-height: 100%;
}

.thread-image {
  height: 200px;
  object-fit: cover;
}
</style>
