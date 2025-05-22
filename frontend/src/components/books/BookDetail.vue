<template>
  <div class="row">
    <div class="col-md-4">
      <img :src="book.cover" class="img-fluid" alt="도서 표지" />
    </div>
    <div class="col-md-8">
      <div class="row">
        <h2>{{ book.title }}</h2>
        <p><strong>저자:</strong> {{ book.author }}</p>
        <p><strong>출판사:</strong> {{ book.publisher }}</p>
        <p><strong>출판일:</strong> {{ book.pub_date }}</p>
        <p><strong>ISBN:</strong> {{ book.isbn }}</p>
        <p><strong>고객 리뷰 평점:</strong> {{ book.customer_review_rank }}</p>
        <p class="mt-3">{{ book.description }}</p>
        
      </div>
      
    </div>

  </div>

  <div class="row mt-3">
    <h5><strong>작가정보</strong></h5>
  </div>

  <div class="row">
    <div class="col-3 ">
      <img :src="book.author_photo" class="rounded-circle" alt="">
    </div>
    <div class="col-9">
      <div class="row fw-bold fs-4">
        {{ book.author }} 
      </div>
      <div class="row mt-2">
        {{ book.author_info }}
      </div>
    </div>
  </div>
 
</template>

<script setup>
defineProps({
  book: Object
})

</script>

<style scoped></style>