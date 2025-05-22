<template>
  <div class="card" v-if="book && book.cover" style="width: 20rem;">
    <div class="row card-body">
      <div class="col-5">
        <img :src="book.cover" class="card-img-top" alt="도서 표지">
      </div>
      <div class="col-6">
        <h5 class="card-title">{{ book.title }}</h5>
        <p class="card-text">{{ book.author }}</p>

        <router-link :to="{ name: 'books-detail', params: { bookId: book.id } }" class="btn btn-primary">
          자세히 보기
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  book: Object
})
</script>
