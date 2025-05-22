// 도서 목록, 도서 상세, 카테고리별 필터 정보
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useBookStore = defineStore('book', () => {
  const books = ref([])
  const categories = ref([])
  const selectedCategory = ref(0)
  const BASE_API_URL = 'http://localhost:8000'

  // 🔹 도서 API 요청 (.then().catch() 방식)
  const fetchBooks = () => {
    axios.get(`${BASE_API_URL}/api/v1/books/`)
      .then(res => {
        console.log('📚 API 응답:', res.data)
        books.value = res.data
      })
      .catch(err => {
        console.error('책 데이터를 불러오는 데 실패했습니다.', err)
      })
  }

  // 🔹 카테고리 API 요청 (.then().catch() 방식)
  const fetchCategories = () => {
    axios.get(`${BASE_API_URL}/api/v1/categories/`)
      .then(res => {
        categories.value = res.data
      })
      .catch(err => {
        console.error('카테고리 데이터를 불러오는 데 실패했습니다.', err)
      })
  }

  // 🔹 카테고리 ID로 이름 찾기
  const getCategoryNameById = (id) => {
    const match = categories.value.find(c => c.id === id)
    return match ? match.name : '기타'
  }


  // 🔹 선택된 카테고리로 필터링
  const filteredBooks = computed(() => {
    if (selectedCategory.value === 0) return books.value
    return books.value.filter(book => book.category.id === selectedCategory.value)
  })


  return {
    books,
    categories,
    selectedCategory,
    filteredBooks,
    fetchBooks,
    fetchCategories,
    getCategoryNameById,
  }
})
