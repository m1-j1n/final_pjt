<template>
  <div class="container py-5">


    <!-- 추천 콘텐츠 (비회원용) -->
    <section class="mb-5">
      <h3 class="mb-4 fw-bold">
        <i class="bi bi-stars me-2 text-primary"></i>당신을 위한 추천 콘텐츠
      </h3>
      <div class="row g-3">
        <div class="col-md-8">
          <div class="card recommendation-card large-card text-white position-relative overflow-hidden"
            @click="goToSurvey">
            <img src="@/assets/img/book-cover/a.jpg" class="card-img object-fit-cover" alt="추천 콘텐츠">
            <div class="card-img-overlay d-flex flex-column justify-content-end bg-dark bg-opacity-50 p-3">
              <small>무엇을 읽어야 할 지 모를 때,</small>
              <h4 class="fw-bold">인생 책을 찾고 싶으신가요?</h4>
            </div>
          </div>
        </div>
        <!-- 읽은 책 기반 추천 리스트 -->
        <div class="col-md-4">
          <div class="card recommendation-card medium-card text-white position-relative overflow-hidden"
            @click="goToReadingRecommend">
            <img src="@/assets/img/book-cover/b.jpg" class="card-img object-fit-cover" alt="추천 콘텐츠">
            <div class="card-img-overlay d-flex flex-column justify-content-end bg-dark bg-opacity-50 p-3">
              <small>Curated for your taste</small>
              <h5 class="fw-bold">당신이 읽고 있는 책과 유사한 리스트</h5>
            </div>
          </div>
        </div>
      </div>
      <!--포스트 추천-->
      <div class="row g-3 mt-2">
        <div class="col-md-4">
          <div class="card recommendation-card small-card text-white position-relative overflow-hidden"
            @click="goToPost">
            <img src="@/assets/img/book-cover/d.jpg" class="card-img object-fit-cover" alt="추천 콘텐츠">
            <div class="card-img-overlay d-flex flex-column justify-content-end bg-dark bg-opacity-50 p-3">
              <small>:-)</small>
              <h6 class="fw-bold">다른 사람의 인생 책이 궁금하신가요?</h6>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card recommendation-card small-card text-white position-relative overflow-hidden"
            @click="gotoStyleRecommned">
            <img src="@/assets/img/book-cover/a.jpg" class="card-img object-fit-cover" alt="추천 콘텐츠">
            <div class="card-img-overlay d-flex flex-column justify-content-end bg-dark bg-opacity-50 p-3">
              <small>책을 고르기 망설여질 때,</small>
              <h6 class="fw-bold">당신이 선호하는 스타일의 책은 ?</h6>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card recommendation-card small-card text-white position-relative overflow-hidden"
            @click="gotoStopBookList">
            <img src="@/assets/img/book-cover/b.jpg" class="card-img object-fit-cover" alt="추천 콘텐츠">
            <div class="card-img-overlay d-flex flex-column justify-content-end bg-dark bg-opacity-50 p-3">
              <small>책을 덮은 사람들이 궁금할 때,</small>
              <h6 class="fw-bold">사람들이 많이 중단한 책.. 그 이유는 ?</h6>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 인기 책 섹션 -->
    <section class="mb-5">
      <h3 class="mb-4 fw-bold">
        <i class="bi bi-bookmark-star-fill me-2 text-danger"></i>인기 책
      </h3>
      <Swiper :modules="[Autoplay]" :slides-per-view="3" :space-between="30" :loop="true"
        :autoplay="{ delay: 3000, disableOnInteraction: false }">
        <SwiperSlide v-for="book in topBooks" :key="book.id">
          <RouterLink :to="{ name: 'books-detail', params: { bookId: book.id } }">
            <div class="card h-100">
              <img :src="book.cover" class="card-img-top" :alt="book.title">
              <div class="card-body">
                <h5 class="card-title">{{ book.title }}</h5>
                <p class="card-text text-muted">{{ book.author }}</p>
              </div>
            </div>
          </RouterLink>

        </SwiperSlide>
      </Swiper>
    </section>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { RouterLink } from "vue-router";
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Autoplay } from 'swiper/modules'
import { useUserStore } from '@/stores/users.js'
import 'swiper/css'
import 'swiper/css/autoplay'
import Swal from 'sweetalert2'

const userStore = useUserStore()
const router = useRouter()

// 설문 이동
const goToSurvey = () => {
  router.push('/survey')
}

// 포스트 추천
const goToPost = () => {
  router.push({ name: 'posts-recommend' })
}


// 독서 상태 기반 추천 이동
const goToReadingRecommend = () => {
  if (!userStore.token) {
    Swal.fire({
      icon: 'info',
      title: '로그인이 필요해요',
      text: '추천 기능은 로그인 후 이용하실 수 있어요.',
      confirmButtonText: '로그인',
      showCancelButton: true,
      cancelButtonText: '닫기',
      buttonsStyling: false,
      customClass: {
        confirmButton: 'btn btn-dark rounded-pill px-4 me-2',
        cancelButton: 'btn btn-outline-secondary rounded-pill px-4',
        popup: 'rounded-4',
      },
    }).then((result) => {
      if (result.isConfirmed) {
        router.push({ name: 'login' })
      }
    })
    return
  }

  router.push({ name: 'recommend-reading' })
}

// 사람들이 읽다 중단한 책으로 이동
const gotoStopBookList = () => {
  router.push('/recommend/stop')
}

// 회원가입 키워드 기반 추천
const gotoStyleRecommned = () => {
  router.push('/recommend/style')
}

const topBooks = ref([])

onMounted(() => {
  axios.get('http://127.0.0.1:8000/api/v1/books/', {
    headers: { Authorization: undefined }
  })
    .then(res => {
      const books = res.data.results
      topBooks.value = books
        .filter(book => book.customer_review_rank !== undefined)
        .sort((a, b) => b.customer_review_rank - a.customer_review_rank)
        .slice(0, 9)
    })
    .catch(err => {
      console.error('🔥 인기 책 로드 실패:', err)
    })
})


</script>

<style scoped>
.card {
  cursor: pointer;
  transition: transform 0.2s ease-in-out;
  border-radius: 16px;
  overflow: hidden;
}

.card:hover {
  transform: scale(1.02);
}

.card-img {
  object-fit: cover;
  width: 100%;
  height: 100%;
}

.recommendation-card.large-card {
  height: 320px;
}

.recommendation-card.medium-card {
  height: 320px;
}

.recommendation-card.small-card {
  height: 200px;
}
</style>
