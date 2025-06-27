<template>
  <div class="mypage-wrapper container py-5">
    <!-- 상단 제목 -->
    <div class="text-start mb-4">
      <h2 class="shelf-title">{{ user.name }}님의 서재</h2>
      <div class="shelf-decoration"></div>
    </div>

    <!-- 좌: 프로필 + About -->
    <div class="row gx-4 align-items-start">
      <div class="col-lg-4 d-flex flex-column gap-4">
        <!-- 📌 프로필 카드 -->
        <div class="card-section shadow-block text-center py-4">
          <img :src="profileImg" class="profile-img-large mb-3" alt="프로필" />
          <h5 class="fw-semibold">{{ user.username }}</h5>

          <!-- 📌 팔로워/팔로잉 수 -->
          <div class="d-flex justify-content-center gap-4 my-3">
            <div>
              <h6 class="mb-0">{{ user.followers_count }}</h6>
              <small class="text-muted">팔로워</small>
            </div>
            <div>
              <h6 class="mb-0">{{ user.followings_count }}</h6>
              <small class="text-muted">팔로잉</small>
            </div>
          </div>

          <!-- 📌 팔로우 버튼 -->
          <button
            @click="toggleFollow"
            class="btn btn-sm mt-2"
            :class="isFollowing ? 'btn-outline-secondary' : 'btn-outline-primary'"
          >
            {{ isFollowing ? '언팔로우' : '팔로우' }}
          </button>
        </div>

        <!-- 📌 About Me (선호도) -->
        <div class="card-section shadow-block p-4">
          <h5 class="fw-semibold mb-3">About</h5>

          <template v-if="user.preference">
            <div class="aboutme-item mb-3">
              <strong class="aboutme-label">라이프스타일</strong>
              <div class="tag-row">
                <span v-for="item in user.preference.lifestyles" :key="item.id" class="badge badge-lifestyle">
                  {{ item.name }}
                </span>
              </div>
            </div>

            <div class="aboutme-item mb-3">
              <strong class="aboutme-label">독서 스타일</strong>
              <div class="tag-row">
                <span v-for="item in user.preference.preferred_reading_styles" :key="item.id" class="badge badge-reading">
                  {{ item.name }}
                </span>
              </div>
            </div>

            <div class="aboutme-item mb-3">
              <strong class="aboutme-label">관심 장르</strong>
              <div class="tag-row">
                <span v-for="item in user.preference.interested_genres" :key="item.id" class="badge badge-interest">
                  {{ item.name }}
                </span>
              </div>
            </div>

            <div class="aboutme-item mb-3">
              <strong class="aboutme-label">비선호 장르</strong>
              <div class="tag-row">
                <span v-for="item in user.preference.avoided_genres" :key="item.id" class="badge badge-avoid">
                  {{ item.name }}
                </span>
              </div>
            </div>

            <div class="aboutme-item">
              <strong class="aboutme-label">기피 키워드</strong>
              <div class="tag-row">
                <span v-for="item in user.preference.avoided_keywords" :key="item.id" class="badge badge-muted">
                  {{ item.name }}
                </span>
              </div>
            </div>
          </template>
        </div>
      </div>

      <!-- 📚 책 / 포스트 -->
      <div class="col-lg-8">
        <div class="card-section shadow-block px-4 py-4">
          <!-- 탭 -->
          <div class="d-flex mb-3 gap-3">
            <button @click="activeTab = 'books'" :class="['tab-btn', activeTab === 'books' ? 'active' : '']">책장</button>
            <button @click="activeTab = 'posts'" :class="['tab-btn', activeTab === 'posts' ? 'active' : '']">포스트</button>
          </div>

          <!-- 책장 -->
          <div v-if="activeTab === 'books'" class="book-grid bookshelf-area">
            <template v-if="books.length === 0">
              <div class="w-100 d-flex justify-content-center align-items-center" style="height: 300px;">
                <p class="empty-message text-muted text-center">서재가 비어 있어요.<br />지금 한 권 시작해볼까요?</p>
              </div>
            </template>
            <template v-else>
              <div v-for="book in books" :key="book.id" class="book-card shelf-row" @click="goToBookDetail(book.id)">
                <div class="book-img-wrapper position-relative">
                  <img :src="book.cover" class="book-img" />
                </div>
                <div class="shelf-line"></div>
              </div>
            
            </template>
          </div>

          <!-- 포스트 -->
          <div v-if="activeTab === 'posts'" class="row pt-3">
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
  if (!src) return 'https://www.gravatar.com/avatar/?d=mp'
  return src.startsWith('http') ? src : `${import.meta.env.VITE_API_URL}${src}`
}

const goToBookDetail = (bookId) => {
  router.push({ name: 'books-detail', params: { bookId } })
}

const goToPostDetail = (postId) => {
  router.push({ name: 'posts-detail', params: { postId } })
}

const toggleFollow = async () => {
  try {
    await axios.post(API.ACCOUNT.FOLLOW(userId), {}, {
      headers: { Authorization: `Token ${localStorage.getItem('token')}` }
    })
    isFollowing.value = !isFollowing.value

    // 팔로워 수 변경
    if (isFollowing.value) {
      user.value.followers_count += 1
    } else {
      user.value.followers_count -= 1
    }

  } catch (err) {
    console.error('팔로우 요청 실패:', err)
  }
}

onMounted(async () => {
  const headers = {
    Authorization: `Token ${localStorage.getItem('token')}`
  }

  // 1. 프로필 정보 불러오기
  const fetchUserProfile = async () => {
    try {
      const { data } = await axios.get(API.ACCOUNT.PROFILE_BY_ID(userId), { headers })
      user.value = data
      
      profileImg.value = getImageUrl(data.profile_img)
      posts.value = data.posts || []
      books.value = data.books || []
      postCount.value = posts.value.length
      bookCount.value = books.value.length
    } catch (err) {
      console.error('❌ 프로필 데이터 로딩 실패:', err)
    }
  }

  // 2. 팔로우 상태 확인
  const fetchFollowStatus = async () => {
    try {
      const { data } = await axios.get(API.ACCOUNT.FOLLOW_STATUS(userId), { headers })
      isFollowing.value = data.is_following
    } catch (err) {
      console.error('❌ 팔로우 상태 확인 실패:', err)
    }
  }

  await Promise.all([fetchUserProfile(), fetchFollowStatus()])
})

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

/* 카드 공통 스타일 */
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
  margin-bottom: 6px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s;
}
.book-img:hover {
  transform: scale(1.04);
}
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

/* 뱃지 */
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

.badge-status.left-top {
  top: 6px;
  left: 6px;
}
.badge-status.right-top {
  top: 6px;
  right: 6px;
  left: auto;
}

/* 비어 있을 때 메시지 */
.empty-message {
  font-size: 1rem;
  color: #888;
  line-height: 1.7;
  padding: 60px 0;
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

.book-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 20px;
}

.book-card {
  position: relative;
  aspect-ratio: 2 / 3;
  overflow: hidden;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.book-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

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
</style>

