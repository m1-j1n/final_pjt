<template>
  <div class="container blogy-theme">
    <h3 class="mb-3 text-heading">카테고리별 도서 보기</h3>
    <div class="row">
      <!-- ─── 좌측 사이드바 ─── -->
      <div class="col-3">
        <!-- 검색바 -->
        <div class="card mb-4 blogy-card blogy-search">
          <div class="card-body">
            <h5 class="blogy-title">Search</h5>
            <div class="input-group">
              <input
                v-model="searchQuery"
                @keyup.enter="doSearch"
                type="text"
                class="form-control"
                placeholder="검색어를 입력하세요"
              />
              <button class="btn blogy-btn" @click="doSearch">검색</button>
            </div>
          </div>
        </div>

        <!-- 카테고리 사이드바 -->
        <div class="card blogy-card blogy-categories">
          <div class="card-body">
            <h5 class="blogy-title">Categories</h5>
            <ul class="list-unstyled mb-0">
              <li
                v-for="cat in bookStore.categories"
                :key="cat.id"
                class="category-item mb-1"
                :class="{ active: bookStore.selectedCategory === cat.id }"
                @click="fetchBooksByCategory(cat.id)"
              >
                {{ cat.name }}
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- ─── 메인 콘텐츠: 도서 카드 리스트 ─── -->
      <div class="col-9">
        <div class="d-flex flex-column gap-3">
          <div
            v-for="book in searched ? results : bookStore.books"
            :key="book.id"
          >
            <BookCard :book="book" />
          </div>
        </div>
      </div>
       <!-- ─── 페이지네이션 (전체 폭) ─── -->
    <div class="row">
      <div class="col-12 d-flex justify-content-center">
        <nav v-if="!searched">
          <ul class="pagination pagination-sm justify-content-center">
            <li class="page-item" :class="{ disabled: pageGroupStart === 1 }">
              <button class="page-link" @click="goToPrevGroup">이전</button>
            </li>
            <li
              v-for="n in pageGroupEnd - pageGroupStart + 1"
              :key="n"
              class="page-item"
              :class="{ active: currentPage === pageGroupStart + n - 1 }"
            >
              <button
                class="page-link"
                @click="fetchBooksByCategory(bookStore.selectedCategory, pageGroupStart + n - 1)"
              >
                {{ pageGroupStart + n - 1 }}
              </button>
            </li>
            <li class="page-item" :class="{ disabled: pageGroupEnd === totalPages }">
              <button class="page-link" @click="goToNextGroup">다음</button>
            </li>
          </ul>
        </nav>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useBookStore } from '@/stores/books.js'
import { searchBooks } from '@/stores/search.js'
import BookCard from '@/components/books/BookCard.vue'
import Swal from 'sweetalert2'

const BASE_API_URL = 'http://localhost:8000'
const bookStore = useBookStore()

// 검색 관련 변수
const mode = ref('category')
const searchQuery = ref('')
const results = ref([])
const searched = ref(false)

const doSearch = async () => {
  if (!searchQuery.value.trim()) return

  const data = await searchBooks(searchQuery.value)
  if (!data.length) {
    Swal.fire({
      icon: 'info',
      title: '검색 결과 없음',
      text: '해당 키워드에 대한 도서를 찾을 수 없어요 😢',
      confirmButtonText: '확인',
    })
    return
  }

  results.value = data
  searched.value = true
  bookStore.selectedCategory = 0
}

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
  mode.value = 'category'
  currentPage.value = page
  searched.value = false
  results.value = []

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

<style scoped>
.blogy-card {
  border: 1px solid #e6e6e6;
  border-radius: 12px;
  background-color: #fafafa;
  padding: 1rem;
}

.blogy-title {
  position: relative;
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
  padding-left: 1rem;
  margin-bottom: 1rem;
}

.blogy-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.1rem;
  width: 4px;
  height: 100%;
  background-color: #f7a76c; /* 부드러운 주황색 */
  border-radius: 2px;
}

.blogy-search .input-group {
  border: 1px solid #ddd;
  border-radius: 50px;
  overflow: hidden;
  background-color: white;
}

.blogy-search input {
  border: none;
  outline: none;
  border-radius: 50px 0 0 50px;
  padding-left: 1rem;
}

.blogy-search button {
  border: none;
  background: none;
  color: #555;
  padding: 0 1rem;
  border-left: 1px solid #ddd;
  border-radius: 0 50px 50px 0;
}

.blogy-search input:focus {
  box-shadow: none;
}


</style>