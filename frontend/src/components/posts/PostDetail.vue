<template>
  <div class="container mt-4" v-if="post && book">
    <!-- 상단 커버 이미지 -->
    <div v-if="post.cover_img" class="mb-4">
      <img
        :src="getImageUrl(post.cover_img)"
        class="w-100 rounded shadow-sm"
        style="max-height: 400px; object-fit: cover;"
        :alt="post.title"
      />
    </div>

    <!-- 본문 + 사이드 (책 정보) -->
    <div class="row">
      <!-- 왼쪽: 본문 영역 -->
      <div class="col-lg-8 mb-4">
        <div class="mb-2 text-muted small">
          ✍️ {{ post.user }} · 🕒 {{ formatDate(post.created_at) }}
        </div>
        <h2 class="fw-bold mb-3">{{ post.title }}</h2>
        <p class="fs-5" style="line-height: 1.8;" v-html="formattedContent"></p>
        <!-- <p class="fs-5" style="line-height: 1.8;">{{ post.content }}</p> -->
      </div>

      <!-- 오른쪽: 책 정보 (작게) -->
      <div class="col-lg-4">
        <div class="card shadow-sm">
          <img :src="book.cover" class="card-img-top" :alt="book.title" style="height: 400px; object-fit: cover;" />
          <div class="card-body">
            <h5 class="card-title mb-1">{{ book.title }}</h5>
            <p class="text-muted mb-1">{{ book.author }}</p>
            <p class="small mb-1">{{ book.publisher }} · {{ book.pub_date }}</p>
            <p class="small text-muted mb-0">⭐ 평점: {{ book.customer_review_rank }}</p>
          </div>
        </div>
      </div>

        <!-- 수정/삭제 -->
        <div class="d-flex justify-content-end mt-4">
          <button class="btn btn-outline-primary me-2" @click="goToEdit(book.id, post.id)">수정</button>
          <button class="btn btn-outline-danger" @click="deleteThread(book.id, post.id)">삭제</button>
        </div>
    </div>

    <!-- 댓글 컴포넌트 -->
    <div class="mt-5">
          <PostComments :postId="postId" />
        </div>
  </div>

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

const getImageUrl = (path) => `http://localhost:8000${path}`
// 포스트 출력 형식 지정
const formattedContent = computed(() => {
  return post.value?.content.replace(/\n/g, '<br>')
})

onMounted(async () => {
  if (postStore.posts.length === 0) {
    await postStore.fetchPosts()
  }

  const target = postStore.posts.find(p => p.id === postId)
  if (target?.book_id) {
    bookStore.fetchBookDetail(target.book_id).then(res => {
      book.value = res
    })
  }
})

// 작성자 여부 확인
const isOwner = computed(() => {
  return post.value?.user === userStore.user?.username
})

// 수정 버튼
const goToEdit = (bookId, postId) => {
  router.push({ name: 'post-update', params: { bookId, postId } })
}

// 삭제 버튼
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
  font-size: 1.1rem;
  font-weight: 600;
}
</style>