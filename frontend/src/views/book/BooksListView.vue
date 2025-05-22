<template>
  <div class="container">
    <div class="row">
      <!-- 카테고리 사이드바 -->
      <div class="col-3">
        <h5>카테고리</h5>
        <ul class="list-group">
          <li
            v-for="cat in bookStore.categories"
            :key="cat.id"
            class="list-group-item"
            :class="{ active: bookStore.selectedCategory === cat.id }"
            @click="bookStore.selectedCategory = cat.id"
          >
            {{ cat.name }}
          </li>
        </ul>
      </div>

      <!-- 도서 카드 리스트 -->
      <div class="col-9">
        <div class="row">
          <div class="col" v-for="book in bookStore.filteredBooks" :key="book.id">
            <BookCard :book="book" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useBookStore } from '@/stores/books.js'
import BookCard from '@/components/books/BookCard.vue'

const bookStore = useBookStore()

onMounted(() => {
  bookStore.fetchBooks()
  bookStore.fetchCategories()
  console.log('📘 첫 번째 book 데이터:', bookStore.books[0])

})

</script>
