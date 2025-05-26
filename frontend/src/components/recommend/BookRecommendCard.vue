<template>
  <div class="recommend-card d-flex flex-column flex-md-row align-items-center bg-white shadow rounded-4 p-4 gap-4">
    <!-- 왼쪽 텍스트 -->
    <div class="flex-grow-1 text-section">
      <!-- 키워드 -->
      <div class="mb-2">
        <span v-for="(kw, i) in book.keywords.slice(0, 3)" :key="i" class="badge bg-warning text-dark me-2">
          {{ kw }}
        </span>
      </div>

      <!-- 제목 -->
      <h3 class="fw-bold mb-1">{{ book.title }}</h3>

      <!-- 부제 or 내용 -->
      <p class="text-muted mb-1">{{ book.description }}</p>

      <!-- 작가 -->
      <p class="mb-2"><strong>By {{ book.author }}</strong></p>

      <!-- 추천 이유 -->
      <p class="text-secondary">{{ book.reason }}</p>

      <!-- 버튼 -->
      <div class="mt-3 d-flex gap-2">
        <RouterLink :to="{ name: 'books-detail', params: { bookId: book.id } }" class="btn btn-primary">
          상세 보기
        </RouterLink>
        <a :href="book.book_url || '#'" class="btn btn-outline-secondary" target="_blank">미리 보기</a>
      </div>
    </div>

    <!-- 오른쪽 책 이미지 -->
    <div class="image-section text-center">
      <img :src="book.cover" alt="책 표지" class="book-image shadow" />
    </div>
  </div>
</template>

<script setup>
defineProps({
  book: Object
})
</script>

<style scoped>
.recommend-card {
  background-color: #fff;
  border-radius: 1.5rem;
}

.text-section {
  max-width: 60%;
}

.image-section {
  flex-shrink: 0;
}

.book-image {
  width: 200px;
  height: auto;
  border-radius: 1rem;
  object-fit: cover;
}
</style>
