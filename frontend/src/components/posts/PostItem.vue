<template>
  <div class="container">
    <h3 class="mb-3 fw-bold text-heading">요즘 유저들이 남긴 포스트</h3>

    <!-- 포스트 카드 (2열 고정) -->
    <div class="row row-cols-1 row-cols-md-2 g-4">
      <div class="col" v-for="post in selectedPosts" :key="post.id">
        <RouterLink :to="{ name: 'posts-detail', params: { postId: post.id } }" class="text-decoration-none text-dark">
          <div class="card h-100 shadow-sm" style="cursor: pointer;">
            <img v-if="post.cover_img" :src="getImageUrl(post.cover_img)" class="card-img-top post-image" :alt="post.title" />
            <div class="card-body d-flex flex-column">
              <p class="text-muted mb-1">
                <strong>{{ post.user }}</strong> · 
                {{ formatTimeAgo(post.created_at) }}
              </p>
              <h5 class="card-title">{{ post.title }}</h5>
              <p class="card-text">
                {{ post.content.length > 100 ? post.content.slice(0, 100) + '...' : post.content }}
              </p>
              <p class="text-muted mt-auto small">💬 댓글 {{ post.comment_count || 0 }}개</p>
              <!-- 키워드 해시태그 -->
              <p>
                <span
                  v-for="(kw, i) in post.keywords.slice(0, 3)"
                  :key="i"
                  class="badge rounded-pill bg-light text-dark border"
                >
                  #{{ kw.name }}
                </span>
              </p>
            </div>
          </div>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { usePostStore } from '@/stores/post'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
dayjs.extend(relativeTime)

const formatTimeAgo = (isoString) => {
  return dayjs(isoString).fromNow()
}

const postStore = usePostStore()
const selectedPosts = ref([])

const BASE_API_URL = import.meta.env.VITE_API_URL

// 포스트 이미지 불러오기
const getImageUrl = (path) => {
  if (!path) {
    return 'https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?fit=crop&w=600&h=400&auto=format'; // 책 느낌의 기본 이미지
  }
  if (path.startsWith('http')) return path;
  return `${BASE_API_URL}/media/${path.replace(/^\/?media\//, '')}`;
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
