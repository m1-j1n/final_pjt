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
        <h2 class="mb-3">{{ post.title }}</h2>
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
import { useRoute } from 'vue-router'
import { usePostStore } from '@/stores/post'
import { useBookStore } from '@/stores/books'
import { ref, computed, onMounted } from 'vue'

const route = useRoute()
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