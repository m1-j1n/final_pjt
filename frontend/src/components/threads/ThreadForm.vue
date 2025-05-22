<template>
  <div class="d-flex justify-content-center pt-5 bg-light">
    <div class="card p-4 shadow" style="max-width: 720px; width: 100%;">
      <h4 class="mb-4 text-center">📝 새로운 스레드 작성</h4>

      <!-- 제목 -->
      <div class="mb-3">
        <label for="threadTitle" class="form-label">제목</label>
        <input type="text" class="form-control" id="threadTitle" v-model="title" placeholder="제목을 입력하세요">
      </div>

      <!-- 내용 -->
      <div class="mb-3">
        <label for="threadContent" class="form-label">내용</label>
        <textarea class="form-control" id="threadContent" rows="5" v-model="content" placeholder="내용을 입력하세요"></textarea>
      </div>

      <!-- 작성 시각 -->
      <div class="mb-3">
        <label for="threadDate" class="form-label">읽은 날짜</label>
        <input v-model="datetime" id="threadDate" type="datetime-local" class="form-control mb-3" />
      </div>

      <!-- 책 정보 카드 가운데 정렬 -->
      <label for="">도서 정보</label>
      <div class="d-flex justify-content-center">
        <div v-if="book" class="card mb-4" style="max-width: 60%;">
          <div class="row g-0">
            <div class="col-md-4">
              <img :src="book.fields.cover" class="img-fluid rounded-start" :alt="book.fields.title" />
            </div>
            <div class="col-md-8">
              <div class="card-body">
                <h5 class="card-title">{{ book.fields.title }}</h5>
                <p class="card-text text-muted">{{ book.fields.author }}</p>
                <p class="card-text small">{{ book.fields.publisher }} / {{ book.fields.pub_date }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 버튼 영역 가운데 정렬 -->
      <div class="d-flex justify-content-center gap-3 mt-4">
        <button class="btn btn-secondary btn-lg px-4" @click="handleCancel">취소</button>
        <button class="btn btn-primary btn-lg px-4" @click="handleCreateThread">작성</button>
      </div>


    </div>
  </div>
</template>


<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useThreadStore } from '@/stores/threads'
import books from '@/assets/data/books.json'

// 라우터 정보
const router = useRouter()
const route = useRoute()
const threadStore = useThreadStore()

// bookId는 라우트에서 받아옴 (ex: /books/:bookId/write-thread)
const bookId = Number(route.params.bookId)

// 해당 책 데이터 가져오기
const book = computed(() => {
  return books.find(b => b.pk === bookId)
})

// 입력값 상태
const title = ref('')
const content = ref('')
const datetime = ref('')

// 스레드 생성
const handleCreateThread = () => {
  if (title.value && content.value) {
    threadStore.createThread(bookId, title.value, content.value, datetime.value)
    router.push('/threads')
  } else {
    alert('필드를 모두 입력해주세요!')
  }
}

// 취소 시 이전 페이지로
const handleCancel = () => {
  router.back()
}
</script>

<style scoped>
.img-fluid {
  max-height: 180px;
  object-fit: cover;
}
</style>
