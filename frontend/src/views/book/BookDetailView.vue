<template>
  <div class="container mt-4" v-if="book">
    <!--  도서 상세 정보 -->
    <BookDetail :book="book" />

    <!-- 포스트 작성 버튼 -->
    <!-- <div class="mt-4 text-end">
      <router-link
        :to="{ name: 'posts-write', params: { bookId: book.id } }"
        class="btn btn-success"
      >
      + thread 
      </router-link>
      
    </div> -->
    <div class="mt-4 text-end">
      <button class="btn btn-outline-dark" @click="handleClick">
        포스트 작성
      </button>
    </div>
  </div>

  <div v-else class="container mt-4">
    <p>도서를 찾을 수 없습니다.</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useBookStore } from '@/stores/books.js'
import BookDetail from '@/components/books/BookDetail.vue'
import { useUserStore } from '@/stores/users'
import { useRouter } from 'vue-router'

const route = useRoute()
const bookStore = useBookStore()
const bookId = parseInt(route.params.bookId)
const userStore = useUserStore()
const router = useRouter()

// 도서 정보 가져오기
onMounted(async () => {
  if (!bookStore.books.results || bookStore.books.results.length === 0) {
    await bookStore.fetchBooks()
  }
})

// 해당 bookId의 도서 찾기
const book = computed(() => {
  return (bookStore.books.results || []).find(b => b.id === bookId)
})

const handleClick = () => {
  if (!userStore.isLogin) {
    alert('회원만 가능합니다.')
    router.push({ name: 'login' })
  } else {
    router.push({ name: 'posts-write' })
  }
}
</script>

<style scoped></style>