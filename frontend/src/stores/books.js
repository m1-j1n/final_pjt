// 도서 목록, 도서 상세, 카테고리별 필터 정보
import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { API } from '@/api/api'

export const useBookStore = defineStore('book', () => {
  const books = ref([])
  const categories = ref([])
  const selectedCategory = ref(0)

  // 🔹 도서 API 요청 
  const fetchBooks = () => {
    axios.get(API.BOOK.LIST)
      .then(res => {
        books.value = res.data
      })
      .catch(err => {
        console.error('책 데이터를 불러오는 데 실패했습니다.', err)
      })
  }

  // 🔹 카테고리 목록 불러오기
  const fetchCategories = () => {
    axios.get(API.CATEGORY.LIST, {
      headers: {
        Authorization: undefined,
      }
    })
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

  // 🔹 bookId로 도서 상세 정보 불러오기
  const fetchBookDetail = (bookId) => {
    return axios.get(API.BOOK.DETAIL(bookId))
      .then(res => res.data)
      .catch(err => {
        console.error('도서 상세 정보 요청 실패:', err)
        return null
      })
  }

  // 🔹 좋아요 버튼
const toggleLike = async (book, likedRef, likeCountRef) => {
    const userStore = useUserStore()

    try {
      // UI 반영 먼저
      likedRef.value = !likedRef.value

      const res = await axios.post(
        API.BOOK.TOGGLE_LIKE(book.id),
        {},
        {
          headers: {
            Authorization: `Token ${userStore.token}`,
          },
        }
      )

      const updatedBook = res.data.book
      likedRef.value = updatedBook.liked
      likeCountRef.value = updatedBook.like_count

      // 원본 book 객체도 업데이트 (선택)
      book.liked = updatedBook.liked
      book.like_count = updatedBook.like_count
    } catch (err) {
      if (err.response?.status === 401) {
        Swal.fire({
          icon: 'warning',
          title: '로그인이 필요합니다',
          text: '이 책을 찜하시려면 로그인해주세요.',
          confirmButtonText: '로그인',
          showCancelButton: true,
          cancelButtonText: '취소',
        }).then((result) => {
          if (result.isConfirmed) {
            window.location.href = '/login'
          }
        })
      } else {
        console.error('좋아요 실패:', err)
      }
    }
  }

  return {
    books,
    categories,
    selectedCategory,
    fetchBooks,
    fetchCategories,
    getCategoryNameById,
    fetchBookDetail,
    toggleLike,
  }
})
