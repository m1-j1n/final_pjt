<template>
  <div class="container mt-4">
    <h3 class="mb-4 fw-bold">📝 요즘 유저들이 남긴 포스트</h3>

    <!-- 포스트 카드 (2열 고정) -->
    <div class="row row-cols-1 row-cols-md-2 g-4">
      <div class="col" v-for="post in selectedPosts" :key="post.id">
        <RouterLink :to="{ name: 'posts-detail', params: { postId: post.id } }" class="text-decoration-none text-dark">
          <div class="card h-100 shadow-sm" style="cursor: pointer;">
            <img :src="getImageUrl(post.cover_img)" class="card-img-top post-image" :alt="post.title" />
            <div class="card-body d-flex flex-column justify-content-between">
              <div>
                <p class="text-muted mb-1">
                  <strong>{{ post.user }}</strong> · 
                  {{ formatTimeAgo(post.created_at) }}
                </p>
                <h5 class="card-title">{{ post.title }}</h5>
                <p class="card-text">
                  {{ post.content.length > 100 ? post.content.slice(0, 100) + '...' : post.content }}
                </p>
              </div>

              <!-- 하단 고정: 댓글 수 + 키워드 -->
              <div class="d-flex justify-content-between align-items-center mt-3">
                <p class="text-muted small mb-0">💬 댓글 {{ post.comment_count || 0 }}개</p>
                <div class="d-flex flex-wrap gap-1 justify-content-end">
                  <span
                    v-for="(kw, i) in post.keywords.slice(0, 3)"
                    :key="i"
                    class="badge rounded-pill bg-light text-dark border"
                  >
                    #{{ kw.name }}
                  </span>
                </div>
              </div>
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
const selectedPosts = ref([])

// onMounted(async () => {
//   if (postStore.posts.length === 0) {
//     await postStore.fetchPosts()
//   }
//   selectedPosts.value = postStore.posts
// })


// 포스트 이미지 불러오기
const getImageUrl = (path) => {
  if (!path) return `https://picsum.photos/seed/${Math.floor(Math.random() * 1000)}/400/300`
  return `http://localhost:8000${path}`
}

onMounted(async () => {
  await postStore.fetchPosts()
  selectedPosts.value = postStore.posts
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
