<template>
  <div class="container mt-4" v-if="post && book">
    <!-- 포스트 영역 -->
    <div class="row">
      <div class="col-md-8 mb-4">
        <div class="card shadow-sm">
          <img
            v-if="post.cover_img"
            :src="getImageUrl(post.cover_img)"
            class="card-img-top"
            :alt="post.title"
            style="max-height: 400px; object-fit: cover;"
          />
          <div class="card-body">
            <h2 class="card-title">{{ post.title }}</h2>
            <p class="text-muted mb-2">✍️ {{ post.user }} · 🕒 {{ formatDate(post.created_at) }}</p>
            <p class="lead">{{ post.content }}</p>
            <div class="d-flex justify-content-end">
              <button class="btn btn-outline-primary me-2" @click="goToEdit(book.id, post.id)">수정</button>
              <button class="btn btn-outline-danger" @click="deleteThread(book.id, post.id)">삭제</button>
            </div>
          </div>
        </div>

        <!-- 댓글 컴포넌트 -->
        <div class="mt-4">
          <PostComments :postId="postId" />
        </div>
      </div>

      <!-- 도서 정보 요약 -->
      <div class="col-md-4">
        <div class="card shadow-sm h-100">
          <img :src="book.cover" class="card-img-top" :alt="book.title" />
          <div class="card-body">
            <h5 class="card-title">{{ book.title }}</h5>
            <p class="text-muted mb-1">{{ book.author }}</p>
            <p class="small mb-1">{{ book.publisher }} · {{ book.pub_date }}</p>
            <p class="small text-muted">📚 평점: {{ book.customer_review_rank }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 에러 메시지 -->
  <div v-else class="container mt-5">
    <p>❗ 해당 스레드를 찾을 수 없습니다.</p>
  </div>
</template>

<script setup>
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'
import { usePostStore } from '@/stores/post'
import { useBookStore } from '@/stores/books'
import { useUserStore } from '@/stores/users'
import { ref, computed, onMounted } from 'vue'
import PostComments from '@/components/posts/PostComments.vue'

const route = useRoute()
const router = useRouter()
const postStore = usePostStore()
const bookStore = useBookStore()
const userStore = useUserStore()

const postId = Number(route.params.postId)
const post = computed(() => postStore.posts.find(p => p.id === postId))
const book = ref(null)

const getImageUrl = (path) => {
  return `http://localhost:8000${path}`
}

onMounted(async () => {
  if (postStore.posts.length === 0) {
    await postStore.fetchPosts()
  }

  const target = postStore.posts.find(p => p.id === postId)
  if (target?.book_id) {
    post.value = target
    bookStore.fetchBookDetail(target.book_id).then(res => {
      book.value = res
    })
  }
})

const goToEdit = (bookId, postId) => {
  router.push({ name: 'post-update', params: { bookId, postId } })
}

const deleteThread = (bookId, postId) => {
  if (!confirm('정말 삭제하시겠습니까?')) return

  axios.delete(`http://localhost:8000/api/v1/books/${bookId}/posts/${postId}/delete/`)
    .then(() => postStore.fetchPosts())
    .then(() => router.push({ name: 'posts' }))
    .catch((err) => {
      console.error('❌ 삭제 실패:', err)
      alert('삭제에 실패했습니다.')
    })
}

const formatDate = (iso) => {
  return new Date(iso).toLocaleString()
}
</script>

<style scoped>
.card-title {
  font-size: 1.5rem;
  font-weight: bold;
}
.card-img-top {
  border-bottom: 1px solid #eee;
}
</style>