<template>
  <div class="container mt-5" v-if="thread && book">
    <div class="row">
      <!-- 책 정보 -->
      <div class="col-md-4">
        <div class="card">
          <img :src="book.fields.cover" class="card-img-top" :alt="book.fields.title" />
          <div class="card-body">
            <h5 class="card-title">{{ book.fields.title }}</h5>
            <p class="card-text text-muted">{{ book.fields.author }}</p>
            <p class="card-text small">{{ book.fields.publisher }} / {{ book.fields.pub_date }}</p>
          </div>
        </div>
      </div>

      <!-- 스레드 내용 -->
      <div class="col-md-8">
        <h2 class="mb-3">{{ thread.title }}</h2>
        <p class="lead">{{ thread.content }}</p>
        <hr />
        <p class="text-muted">작성 시각: {{ formatDate(thread.datetime) }}</p>
      </div>

    </div>
  </div>

  <div v-else class="container mt-5">
    <p>❗ 해당 스레드를 찾을 수 없습니다.</p>
  </div>

</template>

<script setup>
import { useRoute } from 'vue-router'
import { useThreadStore } from '@/stores/threads'
import books from '@/assets/data/books.json'
import { computed } from 'vue'

const route = useRoute()
const store = useThreadStore()

const threadId = Number(route.params.threadId)

const thread = computed(() =>
  store.threads.find(t => t.id === threadId)
)

// bookId를 기반으로 책 정보 찾기
const book = computed(() => {
  return books.find(b => b.pk === thread.value?.bookId)
})

const formatDate = (iso) => {
  return new Date(iso).toLocaleString()
}
</script>

<style scoped>
p.lead {
  font-size: 1.2rem;
}

.card-img-top {
  max-height: 280px;
  object-fit: cover;
}
</style>
