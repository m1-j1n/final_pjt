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

          <!-- 내 정보 수정 페이지로 이동 -->
          <RouterLink :to="{ name: 'mypage-edit' }" class="btn btn-outline-primary mt-3">
            ✏ 내 정보 수정
          </RouterLink>
        </div>
      </div>

      <!-- Right: About + Tags + Articles -->
      <div class="col-lg-8">
        <div class="card p-4 shadow-sm">
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

          <h5 class="mt-4">Featured Articles</h5>
          <div class="row">
            <div
              class="col-md-6"
              v-for="article in user.articlesFeatured"
              :key="article.title"
            >
              <div class="card">
                <img :src="article.image" class="card-img-top" alt="Article">
                <div class="card-body">
                  <span class="badge bg-warning text-dark">{{ article.category }}</span>
                  <h6 class="mt-2">{{ article.title }}</h6>
                  <small class="text-muted">
                    <i class="bi bi-clock"></i> {{ article.date }}
                    <i class="bi bi-chat-dots ms-3"></i> {{ article.comments }} Comments
                  </small>
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
import axios from 'axios'
import defaultImg from '@/assets/img/default-profile.png'

// ✅ API base 주소 상수화
const API_ACCOUNT_URL = 'http://127.0.0.1:8000/api/v1/accounts'

const profileImg = ref(defaultImg)
const user = ref({
  name: '',
  bio: '',
  about: '',
  tags: [],
  articles: 0,
  awards: 0,
  followers: 0,
  articlesFeatured: [
    {
      title: 'The Future of AI in Everyday Computing',
      category: 'Technology',
      date: 'Jan 15, 2024',
      comments: 24,
      image: '/profile/article1.webp'
    },
    {
      title: 'Understanding Digital Privacy in 2024',
      category: 'Privacy',
      date: 'Feb 3, 2024',
      comments: 18,
      image: '/profile/article2.webp'
    }
  ]
})

onMounted(() => {
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

    // 🔄 추후 실제 값으로 대체 가능
    user.value.articles = data.articles_count || 0
    user.value.awards = data.awards_count || 0
    user.value.followers = data.followers_count || 0

  }).catch(err => {
    console.error('사용자 정보 불러오기 실패:', err)
  })
})
</script>

<style scoped>
.card {
  border-radius: 16px;
}
.badge {
  font-size: 0.9rem;
  padding: 0.5em 0.75em;
  border-radius: 999px;
}
</style>
