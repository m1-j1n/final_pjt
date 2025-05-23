<template>
  <div class="container mt-4">
    <h3 class="mb-3">📚 카테고리별 포스트 보기</h3>

    <!-- 카테고리 버튼 -->
    <div class="mb-4 d-flex flex-wrap gap-2">
      <button v-for="category in categories" :key="category.pk" class="btn"
        :class="category.id === selectedCategory ? 'btn-primary' : 'btn-outline-primary'"
        @click="fetchPostsByCategory(category.id)">
        {{ category.name }}
      </button>
    </div>

    <!-- 필터링된 포스트 카드 -->
    <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
      <div class="col" v-for="post in selectedPosts" :key="post.id">
        <RouterLink :to="{ name: 'posts-detail', params: { postId: post.id } }"
          class="text-decoration-none text-dark">
          <div class="card h-100" style="cursor: pointer;">
            <img :src="getImageUrl(post.cover_img)" class="card-img-top post-image" :alt="post.title" />
            <div class="card-body">
              
              <!-- 유저명 + 작성 시간 -->
              <p class="text-muted mb-1">
                <strong>{{ post.user }}</strong> · 
                {{ formatTimeAgo(post.created_at) }}
              </p>

              <h5 class="card-title">{{ post.title }}</h5>
              <p class="card-text">{{ post.content }}</p>

              <!-- 댓글 개수 -->
              <p class="text-muted mt-2 small">💬 댓글 {{ post.comment_count || 0 }}개</p>
            </div>
          </div>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watchEffect } from 'vue'
import { RouterLink } from 'vue-router'
import { usePostStore } from '@/stores/post'
import { useBookStore } from '@/stores/books'
import axios from 'axios'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
dayjs.extend(relativeTime)

const formatTimeAgo = (isoString) => {
  return dayjs(isoString).fromNow()
}

const postStore = usePostStore()
const bookStore = useBookStore()
const posts = computed(() => postStore.posts)
const categories = computed(() => bookStore.categories)

const selectedPosts = ref([])
const selectedCategory = ref(0)

// 카테고리 선택 시 이동
const fetchPostsByCategory = async (categoryId) => {
  selectedCategory.value = categoryId

  if (categoryId === 0) {
    selectedPosts.value = posts.value
    return
  }

  try {
    const res = await axios.get(`http://localhost:8000/api/v1/posts/category/${categoryId}/`)
    selectedPosts.value = res.data.posts
  } catch (err) {
    console.error('카테고리 필터링 실패:', err)
  }
}

// 포스트 이미지 불러오기
const getImageUrl = (path) => {
  if (!path) return '/default-image.jpg' // 이미지 없을 때 기본 이미지
  return `http://localhost:8000${path}`  
}

onMounted(async () => {
  if (bookStore.categories.length === 0) {
    await bookStore.fetchCategories()
  }

  if (postStore.posts.length === 0) {
    await postStore.fetchPosts()
  }

  selectedPosts.value = posts.value 
})


watchEffect(() => {
  if (selectedCategory.value === 0) {
    selectedPosts.value = posts.value
  }
})
</script>

<style scoped>
.card {
  min-height: 100%;
}

.post-image {
  height: 200px;
  object-fit: cover;
}
</style>
