<template>
  <div class="container mt-5" v-if="post && book">
    <div class="row">
      <!-- 책 정보 -->
      <div class="col-md-4">
        <div class="card">
          <img :src="book.cover" class="card-img-top" :alt="book.title" />
          <div class="card-body">
            <h5 class="card-title">{{ book.title }}</h5>
            <p class="card-text text-muted">{{ book.author }}</p>
            <p class="card-text small">{{ book.publisher }} / {{ book.pub_date }}</p>
          </div>
        </div>
      </div>

      <!-- 스레드 내용 -->
      <div class="col-md-8">
        <div class="row d-flex justify-content-between align-items-center">
          <h2 class="col mb-3">{{ post.title }}</h2>
          <div class="col-auto">
            <button class="btn btn-outline-primary me-2"
            @click="goToEdit(book.id, post.id)"
            >수정</button>
            <button class="btn btn-outline-danger"
            @click="deleteThread(book.id, post.id)"
            >삭제</button>
          </div>
        </div>
        <p class="lead">{{ post.content }}</p>
        <hr />
        <p class="text-muted">작성 시각: {{ formatDate(post.created_at) }}</p>
      </div>

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
import { ref, computed, onMounted } from 'vue'

const route = useRoute()
const router = useRouter()
const postStore = usePostStore()
const bookStore = useBookStore()

const book = ref(null)
const postId  = Number(route.params.postId )
const post  = computed(() =>
postStore.posts.find(t => t.id === postId)
)

// bookId를 기반으로 책 정보 찾기
onMounted(async () => {
  if (postStore.posts.length === 0) {
    await postStore.fetchPosts()
  }
  
  const target = postStore.posts.find(t => t.id === postId)
  if (target?.book_id) {
    post.value = target
    bookStore.fetchBookDetail(target.book_id).then(res => {
      book.value = res
    })
  }
})

// 수정 페이지 이동 이벤트 
const goToEdit = (bookId, postId) => {
  router.push({
    name: 'post-update',
    params: { bookId, postId }
  })
}

// 삭제 이벤트
const deleteThread = (bookId, postId) => {
  if (!confirm('정말 삭제하시겠습니까?')) return

  axios.delete(`http://localhost:8000/api/v1/books/${bookId}/posts/${postId}/delete/`)
    .then(() => {
      return postStore.fetchPosts()           
    })
    .then(() => {
      router.push({ name: 'posts' })         
    })
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
p.lead {
  font-size: 1.2rem;
}

.card-img-top {
  max-height: 280px;
  object-fit: cover;
}
</style>