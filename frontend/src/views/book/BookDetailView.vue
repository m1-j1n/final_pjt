<template>
  <div class="container mt-4" v-if="book">
    <!-- 도서 상세 정보 -->
    <div class="mt-4 text-end">
      <button class="btn btn-outline-dark" @click="handleClick">
        포스트 작성
      </button>
    </div>
    <BookDetail :book="book" />
  </div>

  <div v-else class="container mt-4">
    <p>도서를 찾을 수 없습니다.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import BookDetail from '@/components/books/BookDetail.vue'
import { useUserStore } from '@/stores/users'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const book = ref(null)
const bookId = route.params.bookId

onMounted(async () => {
  try {
    const res = await axios.get(`http://localhost:8000/api/v1/books/${bookId}/`)
    book.value = res.data
  } catch (err) {
    console.error('도서 정보 불러오기 실패:', err)
  }
})

const handleClick = () => {
  if (!userStore.isLogin) {
    alert('회원만 가능합니다.')
    router.push({ name: 'login' })
  } else {
    router.push({ name: 'posts-write', params: { bookId } })
  }
}
</script>

<style scoped></style>