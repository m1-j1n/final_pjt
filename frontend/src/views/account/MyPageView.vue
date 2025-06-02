<template>
  <div class="mypage-wrapper container pb-5">
    <!-- 상단 제목 -->
    <div class="text-start mb-4">
      <h2 class="shelf-title">{{ user.name }}님의 서재</h2>
      <div class="shelf-decoration"></div>
    </div>

    <!-- 좌: 프로필+AboutMe / 우: 책장+포스트 -->
    <div class="row gx-4 align-items-start">

      <!-- 왼쪽 -->
      <div class="col-lg-4 d-flex flex-column gap-4">
        <!-- 프로필 -->
        <div class="card-section shadow-block text-center py-4">
          <img :src="profileImg" class="profile-img-large mb-3" alt="프로필" />
          <h5 class="fw-semibold">{{ user.username }}</h5>
          <p class="text-muted small">
            팔로잉 {{ user.followings_count }} · 팔로워 {{ user.followers_count }}
          </p>
          <RouterLink :to="{ name: 'mypage-edit' }" class="btn btn-mypage-edit">프로필 편집</RouterLink>
        </div>

        <!-- About Me -->
        <div class="card-section shadow-block p-4" style="min-height: 460px;">
          <h5 class="fw-semibold mb-3">About Me</h5>

          <!-- ✅ 설문 안한 경우 -->
        <div v-if="!user.is_signup_complete" class="survey-guide text-center mt-4">
          <p class="survey-text text-muted">
            좋아하는 스타일, 관심 있는 주제를 알려주세요!<br />
            설문을 통해 당신만의 책장을 채워드릴게요.
          </p>
          <RouterLink :to="{ name: 'onboarding-survey' }" class="btn btn-outline-primary btn-sm mt-2">
            설문하러 가기
          </RouterLink>
        </div>


          <!-- ✅ 설문 완료한 경우 -->
          <div v-else class="aboutme-section">
            <div class="aboutme-item">
              <strong class="aboutme-label">라이프스타일</strong>
              <div class="tag-row">
                <span v-for="item in user.preference.lifestyles" :key="item.id" class="badge badge-lifestyle">{{ item.name }}</span>
              </div>
            </div>

            <div class="aboutme-item">
              <strong class="aboutme-label">독서 스타일</strong>
              <div class="tag-row">
                <span v-for="item in user.preference.preferred_reading_styles" :key="item.id" class="badge badge-reading">{{ item.name }}</span>
              </div>
            </div>

            <div class="aboutme-item">
              <strong class="aboutme-label">관심 장르</strong>
              <div class="tag-row">
                <span v-for="item in user.preference.interested_genres" :key="item.id" class="badge badge-interest">{{ item.name }}</span>
              </div>
            </div>

            <div class="aboutme-item">
              <strong class="aboutme-label">비선호 장르</strong>
              <div class="tag-row">
                <span v-for="item in user.preference.avoided_genres" :key="item.id" class="badge badge-avoid">{{ item.name }}</span>
              </div>
            </div>

            <div class="aboutme-item">
              <strong class="aboutme-label">기피 키워드</strong>
              <div class="tag-row">
                <span v-for="item in user.preference.avoided_keywords" :key="item.id" class="badge badge-muted">{{ item.name }}</span>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- 오른쪽 -->
      <div class="col-lg-8">
        <div class="card-section shadow-block right-section px-4 py-4">
          <!-- 설문 미완료 안내 -->
          <div v-if="!user.preference || Object.keys(user.preference).length === 0" class="survey-warning">
            <p class="text-muted">아직 선호 설문을 완료하지 않으셨네요!<br />추천을 받으시려면 먼저 설문을 진행해주세요 💛</p>
            <button class="btn btn-outline-primary" @click="goToSurvey">설문하러 가기</button>
          </div>

          <!-- 탭 -->
          <div class="d-flex mb-3 gap-3" v-else>
            <button @click="activeTab = 'books'" :class="['tab-btn', activeTab === 'books' ? 'active' : '']">책장</button>
            <button @click="activeTab = 'posts'" :class="['tab-btn', activeTab === 'posts' ? 'active' : '']">포스트</button>
          </div>

          <!-- 책장 -->
          <div v-if="activeTab === 'books'" class="bookshelf-area">
            <template v-if="books.length === 0">
              <p class="empty-message text-muted text-center">서재가 비어 있어요.<br />지금 한 권 시작해볼까요?</p>
            </template>
            <template v-else>
              <div class="shelf-row" v-for="(row, index) in bookRows" :key="index">
                <div v-for="book in row" :key="book.id" class="book-item">
                    <div class="book-img-wrapper position-relative">
                  <img :src="book.cover" class="book-img" @click="goToBookDetail(book.id)" />

                  <!-- 왼쪽 상단: 읽기 상태 뱃지 -->
                  <span v-if="book.status === 'reading'" class="badge-status green left-top">읽는 중</span>
                  <span v-else-if="book.status === 'done'" class="badge-status blue left-top">완독</span>
                  <span v-else-if="book.status === 'stop'" class="badge-status gray left-top">중단</span>

                  <!-- 오른쪽 상단: 좋아요 하트 뱃지 -->
                  <span v-if="book.liked" class="badge-status red right-top">❤️</span>
                </div>
                </div>
                <div class="shelf-line"></div>
              </div>
            </template>
          </div>

          <!-- 포스트 -->
          <div v-if="activeTab === 'posts'" class="pt-3">
            <template v-if="myPosts.length === 0">
              <p class="empty-message text-muted text-center">아직 포스트가 없어요.<br />당신의 독서 기록을 남겨보세요.</p>
            </template>
            <div class="row">
              <div class="col-md-6 mb-4" v-for="post in myPosts" :key="post.id">
                <div class="card h-100" @click="goToPostDetail(post.id)" style="cursor: pointer;">
                  <img :src="getImageUrl(post.cover_img || post.book_cover)" class="card-img-top" alt="포스트 이미지"
                    style="height: 200px; object-fit: cover;" />
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

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import defaultImg from '@/assets/img/default-profile.png'
import { useUserStore } from '@/stores/users.js'
const userStore = useUserStore()
const router = useRouter()
const API_ACCOUNT_URL = 'http://13.124.181.201:8000/api/v1/accounts'

const profileImg = ref(defaultImg)
const activeTab = ref('books')

const user = ref({
  name: '',
  username: '',
  about: '',
  is_signup_complete: false,
  followers_count: 0,
  followings_count: 0,
  preference: {
    lifestyles: [],
    preferred_reading_styles: [],
    interested_genres: [],
    avoided_genres: [],
    avoided_keywords: [],
  },
})

const likedBooks = ref([])
const readingBooks = ref([])
const books = ref([])
const myPosts = ref([])

const goToBookDetail = (bookId) => {
  router.push({ name: 'books-detail', params: { bookId } })
}

const goToPostDetail = (postId) => {
  router.push({ name: 'posts-detail', params: { postId } })
}

const goToSurvey = () => {
  router.push({ name: 'onboarding-survey' })  // 설문 페이지로 라우팅
}

function mergeBooks() {
  const bookMap = new Map()
  const combined = [...readingBooks.value, ...likedBooks.value]
  console.log('📚 병합 전 책들:', combined)
  

  for (const book of combined) {
    const existing = bookMap.get(book.id) || {}
    bookMap.set(book.id, { ...existing, ...book })
  }

  books.value = Array.from(bookMap.values())
}

const bookRows = computed(() => {
  const rows = []
  for (let i = 0; i < books.value.length; i += 5) {
    rows.push(books.value.slice(i, i + 5))
  }
  return rows
})

onMounted(() => {
  const headers = { Authorization: `Token ${userStore.token}` }

  axios.get(`${API_ACCOUNT_URL}/mypage/`, { headers }).then(res => {
    const data = res.data
    console.log(data)
    user.value.name = data.name
    user.value.username = data.username
    user.value.preference = data.preference || {}
    user.value.is_signup_complete = data.is_signup_complete

    user.value.followers_count = data.followers_count
    user.value.followings_count = data.followings_count 

    if (data.profile_img) {
      profileImg.value = data.profile_img.startsWith('http')
        ? data.profile_img
        : `http://13.124.181.201:8000${data.profile_img}`
    } else {
      profileImg.value = 'https://www.gravatar.com/avatar/?d=mp'
    }

    user.value.about = data.preference
      ? `주 ${data.preference.weekly_avg_reading_time ?? 0}시간 독서, 연간 ${data.preference.annual_reading_amount ?? 0}권 읽음`
      : '설문 미완료'

  })

  axios.get('http://13.124.181.201:8000/api/v1/posts/mine/', { headers }).then(res => {
    myPosts.value = res.data.posts
  })

  axios.get('http://13.124.181.201:8000/api/v1/books/mine/reading/', { headers }).then(res => {
    readingBooks.value = res.data.map(book => ({ ...book, source: 'reading' }))
    mergeBooks()
  })

  axios.get('http://13.124.181.201:8000/api/v1/books/mine/liked/', { headers }).then(res => {
    likedBooks.value = res.data.map(book => ({ ...book, liked: true }))
    mergeBooks()
  })
})

const getImageUrl = (src) => {
  if (!src) return ''
  return src.startsWith('http') ? src : `http://13.124.181.201:8000${src}`
}
</script>

<style scoped>
body {
  background-color: #fcfcfc;
}

.mypage-wrapper {
  font-family: 'Noto Sans KR', sans-serif;
  color: #333;
  padding: 3rem 1rem;
}

/* 제목 */
.shelf-title {
  font-size: 1.8rem;
  font-weight: 600;
  color: #444;
}
.shelf-decoration {
  height: 6px;
  width: 120px;
  background-color: #e2c8aa;
  border-radius: 4px;
  margin-top: 4px;
}

/* 공통 카드 스타일 */
.card-section {
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}


.right-section {
  min-height: 760px;
  padding: 2rem;
}


/* 프로필 이미지 */
.profile-img-large {
  width: 140px;
  height: 140px;
  object-fit: cover;
  border-radius: 50%;
  margin: 0 auto;
}

/* 탭 버튼 */
.tab-btn {
  font-weight: 600;
  font-size: 1.1rem;
  padding: 0.6rem 1.5rem;
  border: none;
  background-color: transparent;
  color: #666;
  border-bottom: 2px solid transparent;
  transition: 0.2s;
}
.tab-btn.active {
  color: #222;
  border-color: #222;
}

/* 책장 */
.bookshelf-area {
  margin-top: 1.5rem;
}

.shelf-row {
  display: flex;
  justify-content: flex-start;
  align-items: flex-end;
  gap: 24px;
  margin-bottom: 40px;
  position: relative;
}

.book-item {
  width: 160px;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  min-height: 220px;
}

.book-img {
  width: 100%;
  height: 220px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 6px; /* 살짝 띄우기 */
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s;
}

.book-img:hover {
  transform: scale(1.04);
}

/* 선반 */
.shelf-line {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 14px;
  width: 100%;
  background-color: #e7cdb1;
  border-radius: 2px;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1);
  z-index: 0;
}

/* 뱃지 밀착 */
.badge-status {
  position: absolute;
  top: 6px;
  left: 6px;
  font-size: 0.75rem;
  padding: 2px 8px;
  border-radius: 999px;
  font-weight: 500;
  z-index: 1;
  background-color: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
.badge-status.green { background-color: #e6f4ea; color: #2e7d32; }
.badge-status.blue { background-color: #e3f2fd; color: #1565c0; }
.badge-status.gray { background-color: #f1f1f1; color: #777; }
.badge-status.red { background-color: #fde8ec; color: #c62828; }

/* 비어 있을 때 */
.empty-message {
  font-size: 1rem;
  color: #888;
  line-height: 1.7;
  padding: 60px 0;
}

/* 설문 미완료 안내 */
.survey-warning {
  background-color: #fff4e1;
  border: 1px solid #fdd99d;
  padding: 1.5rem;
  border-radius: 10px;
  text-align: center;
  margin-bottom: 2rem;
}

/* About Me */
.aboutme-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.aboutme-item .aboutme-label {
  font-size: 0.95rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  display: block;
}

.tag-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

/* 색상별 태그 */
.badge {
  font-size: 0.8rem;
  padding: 6px 12px;
  border-radius: 999px;
  display: inline-block;
}

.badge-lifestyle {
  background-color: #fff9db;
  color: #8d6d00;
}
.badge-reading {
  background-color: #e1f5fe;
  color: #0277bd;
}
.badge-interest {
  background-color: #e8f5e9;
  color: #2e7d32;
}
.badge-avoid {
  background-color: #fce4ec;
  color: #c2185b;
}
.badge-muted {
  background-color: #eceff1;
  color: #455a64;
}

.survey-guide {
  padding: 1rem;
  margin-top: 1.5rem;
}

.survey-text {
  font-size: 0.92rem;
  line-height: 1.6;
}

.badge-status.left-top {
  top: 6px;
  left: 6px;
}

.badge-status.right-top {
  top: 6px;
  right: 6px;
  left: auto; /* 왼쪽 위치 초기화 */
}

.btn-mypage-edit {
  background-color: #f8f9fa;
  color: #343a40;
  border: 1px solid #ced4da;
  border-radius: 999px;
  padding: 0.5rem 1.25rem;
  font-weight: 600;
  font-size: 0.8rem;
  transition: all 0.2s ease;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.btn-mypage-edit:hover {
  background-color: #e9ecef;
  color: #212529;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}
</style>
