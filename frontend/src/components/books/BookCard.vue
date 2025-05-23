<template>
  <div class="card" v-if="book && book.cover" style="width: 20rem; height: 320px;">
    <div class="row card-body">
      <div class="col-5">
        <img :src="book.cover" class="card-img-top" alt="도서 표지" style="height: 100%; object-fit: contain;" />
      </div>
      <div class="col-6 d-flex flex-column justify-content-end">
        <div>
          <h5 class="card-title text-truncate-2">{{ book.title }}</h5>
          <p class="card-text">{{ book.author }}</p>
        </div>
        <!-- 버튼 영역 -->
        <div class="d-flex gap-2 mt-auto">
          <router-link
            :to="{ name: 'books-detail', params: { bookId: book.id } }"
            class="btn btn-primary"
          >
            자세히 보기
          </router-link>

          <button
            class="btn"
            :class="liked ? 'btn-danger' : 'btn-outline-danger'"
            @click="toggleLike"
          >
            ❤️ {{ likeCount }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios';

const props = defineProps({
  book: Object
})
const book = props.book

// 좋아요 처리 
const liked = ref(false)
const likeCount = ref(0)

const toggleLike = async () => {
  try {
    const res = await axios.post(`http://localhost:8000/api/v1/books/${book.id}/like/`)
    liked.value = res.data.liked
    likeCount.value = res.data.like_count
  } catch (err) {
    console.error('좋아요 실패:', err)
  }
}

onMounted(() => {
  if (book && book.id) {
    likeCount.value = book.like_count || 0
    liked.value = book.liked || false
  }
})

</script>

<style scoped>
/* 두 줄 말줄임 처리 */
.text-truncate-2 {
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2; /* 최대 2줄 */
  -webkit-box-orient: vertical;
  line-height: 1.2rem;
  max-height: 2.4rem; /* 2줄 */
}
</style>