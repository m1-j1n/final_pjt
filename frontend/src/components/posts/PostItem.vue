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
            <img :src="post.book_cover" class="card-img-top post-image" :alt="post.title" />
            <div class="card-body">
              <h5 class="card-title">{{ post.title }}</h5>
              <p class="card-text">{{ post.content }}</p>
            </div>
          </div>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { usePostStore } from '@/stores/post'
import { useBookStore } from '@/stores/books'
import axios from 'axios'

const postStore = usePostStore()
const bookStore = useBookStore()
const posts = computed(() => postStore.posts)
const categories = computed(() => bookStore.categories)

const selectedPosts = ref([])
const selectedCategory = ref(0)

// 카테고리 선택 시
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

onMounted(async () => {
  if (bookStore.categories.length === 0) {
    await bookStore.fetchCategories()
  }

  if (postStore.posts.length === 0) {
    await postStore.fetchPosts()
  }

  selectedPosts.value = posts.value 
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
