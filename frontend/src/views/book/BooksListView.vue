<template>
  <div class="container">
    <div class="row">
      <!-- 카테고리 사이드바 -->
      <div class="col-3">
        <h5>카테고리</h5>
        <ul class="list-group">
          <li
            v-for="cat in bookStore.categories"
            :key="cat.id"
            class="list-group-item"
            :class="{ active: bookStore.selectedCategory === cat.id }"
            @click="fetchBooksByCategory(cat.id)"
          >
            {{ cat.name }}
          </li>
        </ul>
      </div>

      <!-- 도서 카드 리스트 -->
      <div class="col-9">
        <div class="row">
          <div class="col" v-for="book in bookStore.books" :key="book.id">
            <BookCard :book="book" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useBookStore } from '@/stores/books.js'
import BookCard from '@/components/books/BookCard.vue'

const BASE_API_URL = 'http://localhost:8000'
const bookStore = useBookStore()

onMounted(() => {
  bookStore.fetchBooks()
  bookStore.fetchCategories()
})

// 카테고리별 도서 요청
const fetchBooksByCategory = async (categoryId) => {
  bookStore.selectedCategory = categoryId
  const url = categoryId === 0
    ? `${BASE_API_URL}/api/v1/books/`
    : `${BASE_API_URL}/api/v1/books/category/${categoryId}/`

  try {
    const res = await axios.get(url)
    bookStore.books = res.data.books

  } catch (err) {
    console.error('도서 목록 요청 실패:', err)
  }
}
</script>
