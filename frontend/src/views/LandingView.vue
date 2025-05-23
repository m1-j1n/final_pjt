<template>
  <div class="container py-5">

    <!-- 추천 콘텐츠 (비회원용) -->
    <section class="mb-5">
      <h3 class="mb-4 fw-bold">📚 당신을 위한 추천 콘텐츠</h3>
      <div class="row g-3">
        <div class="col-md-8">
          <div class="card recommendation-card large-card text-white position-relative overflow-hidden" @click="goToSurvey">
            <img src="@/assets/img/book-cover/a.jpg" class="card-img object-fit-cover" alt="추천 콘텐츠">
            <div class="card-img-overlay d-flex flex-column justify-content-end bg-dark bg-opacity-50 p-3">
              <small>Apr. 14th, 2025 • Technology</small>
              <h4 class="fw-bold">Lorem ipsum dolor sit amet, consectetur adipiscing elit</h4>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card recommendation-card medium-card text-white position-relative overflow-hidden" @click="goToSurvey">
            <img src="@/assets/img/book-cover/b.jpg" class="card-img object-fit-cover" alt="추천 콘텐츠">
            <div class="card-img-overlay d-flex flex-column justify-content-end bg-dark bg-opacity-50 p-3">
              <small>Apr. 14th, 2025 • Security</small>
              <h5 class="fw-bold">Sed do eiusmod tempor incididunt ut labore</h5>
            </div>
          </div>
        </div>
      </div>

      <div class="row g-3 mt-2">
        <div class="col-md-4">
          <div class="card recommendation-card small-card text-white position-relative overflow-hidden" @click="goToSurvey">
            <img src="@/assets/img/book-cover/d.jpg" class="card-img object-fit-cover" alt="추천 콘텐츠">
            <div class="card-img-overlay d-flex flex-column justify-content-end bg-dark bg-opacity-50 p-3">
              <small>Apr. 14th, 2025 • Career</small>
              <h6 class="fw-bold">Ut enim ad minim veniam, quis nostrud exercitation</h6>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card recommendation-card small-card text-white position-relative overflow-hidden" @click="goToSurvey">
            <img src="@/assets/img/book-cover/a.jpg" class="card-img object-fit-cover" alt="추천 콘텐츠">
            <div class="card-img-overlay d-flex flex-column justify-content-end bg-dark bg-opacity-50 p-3">
              <small>Apr. 14th, 2025 • Cloud</small>
              <h6 class="fw-bold">Adipiscing elit, sed do eiusmod tempor incididunt</h6>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card recommendation-card small-card text-white position-relative overflow-hidden" @click="goToSurvey">
            <img src="@/assets/img/book-cover/b.jpg" class="card-img object-fit-cover" alt="추천 콘텐츠">
            <div class="card-img-overlay d-flex flex-column justify-content-end bg-dark bg-opacity-50 p-3">
              <small>Apr. 14th, 2025 • Programming</small>
              <h6 class="fw-bold">Excepteur sint occaecat cupidatat non proident</h6>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 인기 책 섹션 -->
    <section class="mb-5">
      <h3 class="mb-4 fw-bold">🔥 인기 책</h3>
      <Swiper
        :modules="[Autoplay]"
        :slides-per-view="3"
        :space-between="30"
        :loop="true"
        :autoplay="{ delay: 3000, disableOnInteraction: false }"
      >
        <SwiperSlide v-for="book in topBooks" :key="book.id">
          <div class="card h-100">
            <img :src="book.cover" class="card-img-top" :alt="book.title">
            <div class="card-body">
              <h5 class="card-title">{{ book.title }}</h5>
              <p class="card-text text-muted">{{ book.author }}</p>
            </div>
          </div>
        </SwiperSlide>
      </Swiper>
    </section>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

import { Swiper, SwiperSlide } from 'swiper/vue'
import { Autoplay } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/autoplay'

const router = useRouter()

const goToSurvey = () => {
  router.push('/survey')
}

const topBooks = ref([])

onMounted(() => {
  axios.get('http://127.0.0.1:8000/api/v1/books/')
    .then(res => {
      const books = res.data
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
