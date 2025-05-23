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

      <!-- 도서 카드 리스트 하단 -->
      <nav class="mt-4 d-flex justify-content-center">
        <ul class="pagination">
          <!-- 이전 그룹 버튼 -->
          <li class="page-item" :class="{ disabled: pageGroupStart === 1 }">
            <button class="page-link" @click="goToPrevGroup">이전</button>
          </li>

          <!-- 현재 그룹의 페이지 번호 -->
          <li
            class="page-item"
            v-for="n in pageGroupEnd - pageGroupStart + 1"
            :key="n"
            :class="{ active: currentPage === pageGroupStart + n - 1 }"
          >
            <button
              class="page-link"
              @click="fetchBooksByCategory(bookStore.selectedCategory, pageGroupStart + n - 1)"
            >
              {{ pageGroupStart + n - 1 }}
            </button>
          </li>

          <!-- 다음 그룹 버튼 -->
          <li class="page-item" :class="{ disabled: pageGroupEnd === totalPages }">
            <button class="page-link" @click="goToNextGroup">다음</button>
          </li>
        </ul>
      </nav>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useBookStore } from '@/stores/books.js'
import BookCard from '@/components/books/BookCard.vue'

const BASE_API_URL = 'http://localhost:8000'
const bookStore = useBookStore()

// 페이지네이션 관련 변수
const currentPage = ref(1)
const totalCount = ref(0)
const pageSize = 12
const pageGroupSize = 10
const totalPages = computed(() => {
  const pages = Math.ceil(totalCount.value / pageSize)
  return isNaN(pages) || pages < 1 ? 1 : pages
})

const currentGroup = computed(() => Math.floor((currentPage.value - 1) / pageGroupSize))
const pageGroupStart = computed(() => currentGroup.value * pageGroupSize + 1)
const pageGroupEnd = computed(() => {
  const end = pageGroupStart.value + pageGroupSize - 1
  return Math.min(end, totalPages.value)
})

// 이전 이동
const goToPrevGroup = () => {
  const target = pageGroupStart.value - pageGroupSize
  if (target >= 1) {
    fetchBooksByCategory(bookStore.selectedCategory, target)
  }
}

// 다음 이동
const goToNextGroup = () => {
  const target = pageGroupStart.value + pageGroupSize
  if (target <= totalPages.value) {
    fetchBooksByCategory(bookStore.selectedCategory, target)
  }
}

onMounted(() => {
  bookStore.fetchCategories()
  fetchBooksByCategory(0, 1) 
})

// 카테고리별 도서 요청
const fetchBooksByCategory = async (categoryId, page = 1) => {
  bookStore.selectedCategory = categoryId
  currentPage.value = page

  const url = categoryId === 0
  ? `${BASE_API_URL}/api/v1/books/?page=${page}`
  : `${BASE_API_URL}/api/v1/books/category/${categoryId}/?page=${page}`
  
  try {
    const res = await axios.get(url)
    bookStore.books = res.data.results     
    totalCount.value = res.data.count 

  } catch (err) {
    console.error('도서 목록 요청 실패:', err)
  }
}
</script>
