<template>
  <div class="container py-5">
    <div class="row">
      <!-- Left: 유저 카드 -->
      <div class="col-lg-4 mb-4 mb-lg-0">
        <div class="card shadow-sm text-center p-4 mb-4">
          <img :src="profileImg" alt="Author" class="rounded-circle mb-3" width="120" height="120" />
          <h4>{{ user.name }}</h4>
          <p class="text-muted">독서 회원</p>
          <p class="mb-3 small text-muted">{{ user.bio }}</p>

          <div class="d-flex justify-content-between my-4">
            <div>
              <h5>{{ bookCount }}</h5>
              <small class="text-muted">Books</small>
            </div>
            <div>
              <h5>{{ postCount }}</h5>
              <small class="text-muted">Posts</small>
            </div>
            <div>
              <h5>{{ user.followers }}</h5>
              <small class="text-muted">Followers</small>
            </div>
          </div>

          <button @click="toggleFollow" class="btn btn-outline-primary mt-2">
            {{ isFollowing ? '언팔로우' : '팔로우' }}
          </button>
        </div>

        <!-- 라이프스타일, 선호도 -->
        <div class="card p-4 shadow-sm">
          <h4 class="mb-3">About</h4>
          <p>{{ user.about }}</p>

          <template v-if="user.preference">
            <h6 class="mt-4">라이프스타일</h6>
            <div class="mb-2">
              <span v-for="item in user.preference.lifestyles" :key="item.id" class="badge bg-light text-dark border me-1">
                {{ item.name }}
              </span>
            </div>

            <h6 class="mt-3">독서 스타일</h6>
            <div class="mb-2">
              <span v-for="item in user.preference.preferred_reading_styles" :key="item.id" class="badge bg-light text-dark border me-1">
                {{ item.name }}
              </span>
            </div>

            <h6 class="mt-3">관심 장르</h6>
            <div class="mb-2">
              <span v-for="item in user.preference.interested_genres" :key="item.id" class="badge bg-primary-subtle text-primary-emphasis border me-1">
                {{ item.name }}
              </span>
            </div>

            <h6 class="mt-3">비선호 장르</h6>
            <div class="mb-2">
              <span v-for="item in user.preference.avoided_genres" :key="item.id" class="badge bg-danger-subtle text-danger-emphasis border me-1">
                {{ item.name }}
              </span>
            </div>

            <h6 class="mt-3">기피 키워드</h6>
            <div>
              <span v-for="item in user.preference.avoided_keywords" :key="item.id" class="badge bg-warning-subtle text-dark border me-1">
                {{ item.name }}
              </span>
            </div>
          </template>
        </div>
      </div>

      <!-- Right: 책/포스트 -->
      <div class="col-lg-8">
        <div class="d-flex mb-3">
          <button class="btn me-2" :class="{ 'btn-primary': activeTab === 'books', 'btn-outline-primary': activeTab !== 'books' }" @click="activeTab = 'books'">📚 책</button>
          <button class="btn" :class="{ 'btn-primary': activeTab === 'posts', 'btn-outline-primary': activeTab !== 'posts' }" @click="activeTab = 'posts'">📝 포스트</button>
        </div>

        <!-- 책 리스트 -->
        <div v-if="activeTab === 'books'" class="book-grid">
          <div v-for="book in books" :key="book.id" class="book-card" @click="goToBookDetail(book.id)">
            <div class="book-img-wrapper position-relative">
              <img :src="book.cover" class="book-img" />
            </div>
          </div>
        </div>

        <!-- 포스트 리스트 -->
        <div v-if="activeTab === 'posts'" class="row">
          <p v-if="posts.length === 0" class="text-muted text-center">작성한 포스트가 없습니다.</p>
          <div class="col-md-6 mb-4" v-for="post in posts" :key="post.id" @click="goToPostDetail(post.id)" style="cursor: pointer;">
            <div class="card h-100">
              <img :src="getImageUrl(post.cover_img || post.book_cover)" class="card-img-top" style="height: 200px; object-fit: cover;" />
              <div class="card-body">
                <h6 class="card-title">{{ post.title }}</h6>
                <p class="text-muted small">{{ post.content.slice(0, 50) }}...</p>
                <small class="text-muted">작성일: {{ new Date(post.created_at).toLocaleDateString() }}</small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const userId = route.params.userId

const profileImg = ref('')
const user = ref({})
const posts = ref([])
const books = ref([])
const postCount = ref(0)
const bookCount = ref(0)
const isFollowing = ref(false)
const activeTab = ref('books')

const getImageUrl = (src) => {
  if (!src) return ''
  return src.startsWith('http') ? src : `http://localhost:8000${src}`
}

const goToBookDetail = (bookId) => {
  router.push({ name: 'books-detail', params: { bookId } })
}

const goToPostDetail = (postId) => {
  router.push({ name: 'posts-detail', params: { postId } })
}

const toggleFollow = async () => {
  try {
    await axios.post(`http://localhost:8000/api/v1/accounts/${userId}/follow/`, {}, {
      headers: { Authorization: `Token ${localStorage.getItem('access_token')}` }
    })
    isFollowing.value = !isFollowing.value
  } catch (err) {
    console.error('팔로우 요청 실패:', err)
  }
}

onMounted(async () => {
  const headers = { Authorization: `Token ${localStorage.getItem('access_token')}` }

  try {
    const res = await axios.get(`http://localhost:8000/api/v1/accounts/${userId}/profile/`, { headers })
    user.value = res.data
    profileImg.value = getImageUrl(res.data.profile_img)
    posts.value = res.data.posts || []
    books.value = res.data.books || []
    postCount.value = posts.value.length
    bookCount.value = books.value.length
  } catch (err) {
    console.error('프로필 데이터 로딩 실패:', err)
  }

  try {
    const followRes = await axios.get(`http://localhost:8000/api/v1/accounts/${userId}/follow-status/`, { headers })
    isFollowing.value = followRes.data.is_following
  } catch (err) {
    console.error('팔로우 상태 확인 실패:', err)
  }
})
</script>

<style scoped>
.book-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 20px;
}
.book-card {
  position: relative;
  cursor: pointer;
  aspect-ratio: 2 / 3;
  overflow: hidden;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}
.book-img {
  width: 100%;
  height: 300px;
  object-fit: cover;
}
</style>
