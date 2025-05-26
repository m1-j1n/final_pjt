<template>
  <div class="container py-5">
    <div class="row">
      <!-- Left: Profile Card -->
      <div class="col-lg-4 mb-4 mb-lg-0">
        <div class="card shadow-sm text-center p-4">
          <img :src="profileImg" alt="Author" class="rounded-circle mb-3" width="120" height="120">

          <h4>{{ user.name }}</h4>
          <p class="text-muted">독서 회원</p>
          <p class="mb-3 small text-muted">{{ user.bio }}</p>

          <div class="d-flex justify-content-between my-4">
            <div>
              <h5>{{ user.articles }}</h5>
              <small class="text-muted">Articles</small>
            </div>
            <div>
              <h5>{{ user.awards }}</h5>
              <small class="text-muted">Awards</small>
            </div>
            <div>
              <h5>{{ user.followers }}</h5>
              <small class="text-muted">Followers</small>
            </div>
          </div>

          <div class="d-flex justify-content-center gap-3">
            <i class="bi bi-twitter-x"></i>
            <i class="bi bi-facebook"></i>
            <i class="bi bi-instagram"></i>
            <i class="bi bi-linkedin"></i>
          </div>

          <RouterLink :to="{ name: 'mypage-edit' }" class="btn btn-outline-primary mt-3">
            ✏ 내 정보 수정
          </RouterLink>
        </div>
      </div>

      <!-- Right: About + Tags + Books/Posts Tabs -->
      <div class="col-lg-8">
        <div class="card p-4 shadow-sm mb-4">
          <h4>About Me</h4>
          <p>{{ user.about }}</p>

          <h5 class="mt-4">설문 기본 태그</h5>
          <div class="mb-3">
            <span
              v-for="tag in user.tags"
              :key="tag"
              class="badge bg-light text-dark border me-2"
            >{{ tag }}</span>
          </div>
        </div>

        <!-- Tab Buttons -->
        <div class="d-flex mb-3">
          <button class="btn me-2" :class="{ 'btn-primary': activeTab === 'books', 'btn-outline-primary': activeTab !== 'books' }" @click="activeTab = 'books'">📚 책</button>
          <button class="btn" :class="{ 'btn-primary': activeTab === 'posts', 'btn-outline-primary': activeTab !== 'posts' }" @click="activeTab = 'posts'">📝 포스트</button>
        </div>

        <!-- Book Tab Content -->
        <div v-if="activeTab === 'books'" class="book-grid">
          <div v-for="book in books" :key="book.id" class="book-card" @click="goToBookDetail(book.id)">
            <img :src="book.cover" class="book-img" />
            <span class="badge position-absolute top-0 end-0 m-2 bg-primary">{{ book.status }}</span>
          </div>
        </div>

        <!-- Post Tab Content -->
        <div v-if="activeTab === 'posts'" class="row">
          <!-- ✅ 포스트가 아예 없는 경우 -->
          <p v-if="myPosts.length === 0" class="text-muted text-center">
            📝 포스트가 아직 작성되지 않았습니다.
          </p>

          <div class="col-md-6 mb-4" v-for="post in myPosts" :key="post.id">
            <div class="card h-100" @click="goToPostDetail(post.id)" style="cursor: pointer;">
              <img
                :src="post.cover_img || post.book_cover"
                class="card-img-top"
                alt="포스트 이미지"
                style="height: 200px; object-fit: cover;"
              />
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
import axios from 'axios'
import { useRouter } from 'vue-router'
import defaultImg from '@/assets/img/default-profile.png'

const router = useRouter()
const API_ACCOUNT_URL = 'http://127.0.0.1:8000/api/v1/accounts'

const profileImg = ref(defaultImg)
const activeTab = ref('books')

const user = ref({
  name: '',
  bio: '',
  about: '',
  tags: [],
  articles: 0,
  awards: 0,
  followers: 0
})

const books = ref([
  { id: 1, title: '책1', cover: '/media/book1.jpg', status: '완독' },
  { id: 2, title: '책2', cover: '/media/book2.jpg', status: '읽는 중' },
  { id: 3, title: '책3', cover: '/media/book3.jpg', status: '읽고 싶은 책' },
  { id: 4, title: '책4', cover: '/media/book4.jpg', status: '중단' },
])

const myPosts = ref([])

const goToBookDetail = (bookId) => {
  router.push({ name: 'books-detail', params: { bookId } })
}

const goToPostDetail = (postId) => {
  router.push({ name: 'posts-detail', params: { postId } })
}

onMounted(() => {
  // ✅ 사용자 정보 요청
  axios.get(`${API_ACCOUNT_URL}/mypage/`, {
    headers: {
      Authorization: `Token ${localStorage.getItem('access_token')}`
    }
  }).then(res => {
    const data = res.data
    user.value.name = data.name
    user.value.bio = `${data.gender === 'M' ? '남성' : '여성'}, ${data.age}세`

    const tags = []
    if (data.preference) {
      user.value.about = `주 ${data.preference.weekly_avg_reading_time}시간 독서, 연간 ${data.preference.annual_reading_amount}권 읽음`

      if (data.preference.interested_genres) {
        tags.push(...data.preference.interested_genres.map(g => g.name))
      }
      if (data.preference.lifestyle?.name) {
        tags.push(`라이프스타일: ${data.preference.lifestyle.name}`)
      }
      if (data.preference.preferred_reading_style?.name) {
        tags.push(`독서 스타일: ${data.preference.preferred_reading_style.name}`)
      }
      if (data.preference.avoided_keywords) {
        tags.push(`기피: ${data.preference.avoided_keywords}`)
      }
    } else {
      user.value.about = '설문 미완료'
    }
    user.value.tags = tags

    if (data.profile_img) {
      profileImg.value = data.profile_img.startsWith('http')
        ? data.profile_img
        : `http://127.0.0.1:8000${data.profile_img}`
    }

    user.value.articles = data.articles_count || 0
    user.value.awards = data.awards_count || 0
    user.value.followers = data.followers_count || 0
  }).catch(err => {
    console.error('사용자 정보 불러오기 실패:', err)
  })

  // ✅ 내 포스트 목록 요청 (경로 수정!)
  axios.get('http://127.0.0.1:8000/api/v1/posts/mine/', {
    headers: {
      Authorization: `Token ${localStorage.getItem('access_token')}`
    }
  }).then(res => {
    myPosts.value = res.data
  }).catch(err => {
    console.error('내 포스트 불러오기 실패:', err)
  })
})

</script>

<style scoped>
.card {
  border-radius: 16px;
}
.badge {
  font-size: 0.75rem;
  padding: 0.3em 0.6em;
  border-radius: 8px;
}
.book-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 20px;
}
.book-card {
  position: relative;
  cursor: pointer;
}
.book-img {
  width: 100%;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
</style>
