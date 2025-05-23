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

    <div class="row mt-5">
      <div class="col-md-12">
        <!-- 댓글 입력 & 목록 -->
        <div class="mt-5">
          <h5>💬 댓글</h5>

          <form @submit.prevent="submitComment" class="mb-3">
            <textarea v-model="newComment" class="form-control mb-2" rows="2" placeholder="댓글을 입력하세요" />
            <button class="btn btn-sm btn-primary" :disabled="!newComment.trim()">작성</button>
          </form>

          <ul class="list-group">
            <li
              v-for="comment in comments"
              :key="comment.id"
              class="list-group-item d-flex justify-content-between align-items-start"
            >
              <div>
                <strong>{{ comment.user }}</strong><br />
                {{ comment.content }}
              </div>
              <small class="text-muted">{{ formatDate(comment.created_at) }}</small>
            </li>
          </ul>
        </div>
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
import { useUserStore } from '@/stores/users'
import { ref, computed, onMounted } from 'vue'

const route = useRoute()
const router = useRouter()
const postStore = usePostStore()
const bookStore = useBookStore()
const userStore = useUserStore()

// 책 정보
const book = ref(null)
const postId  = Number(route.params.postId )
const post  = computed(() =>
postStore.posts.find(t => t.id === postId)
)

// 댓글 정보
const newComment = ref('')
const comments = ref([])

// 댓글 정보 가져오기
const fetchComments = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/api/v1/posts/${postId}/comments/`)
    comments.value = res.data
  } catch (err) {
    console.error('댓글 불러오기 실패:', err)
  }
}

// 댓글 정보 제출
const submitComment = async () => {
  try {
      await axios.post(
      `http://localhost:8000/api/v1/posts/${postId}/comments/create/`,
      { content: newComment.value },
      {
        headers: {
          Authorization: `Token ${userStore.token}`,
        }
      }
    )
    newComment.value = ''
    await fetchComments()
  } catch (err) {
    console.error('댓글 작성 실패:', err)
  }
}

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

  await fetchComments()  
})

// 수정 페이지 이동 이벤트 
const goToEdit = (bookId, postId) => {
  router.push({
    name: 'post-update',
    params: { bookId, postId }
  })
}

// 포스트 삭제 이벤트
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