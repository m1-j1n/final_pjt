<template>
  <div class="card p-4 shadow">
    <h4 class="mb-4 text-center">📝 새 포스트 작성</h4>

    <div class="mb-3">
      <label class="form-label">제목</label>
      <input v-model="title" class="form-control" />
    </div>

    <div class="mb-3">
      <label class="form-label">내용</label>
      <textarea v-model="content" class="form-control" rows="5" />
    </div>

    <div class="mb-3">
      <label class="form-label">읽은 날짜</label>
      <input v-model="datetime" type="datetime-local" class="form-control" />
    </div>

    <div class="d-flex justify-content-center gap-3 mt-4">
      <button class="btn btn-secondary" @click="handleCancel">취소</button>
      <button class="btn btn-primary" @click="handleSubmit">작성</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { usePostStore } from '@/stores/post'

const title = ref('')
const content = ref('')
const datetime = ref('')

const store = usePostStore()
const router = useRouter()
const route = useRoute()

const bookId = Number(route.params.bookId)

const handleSubmit = () => {
  if (!title.value || !content.value) {
    alert('제목과 내용을 모두 입력하세요.')
    return
  }

  const payload = {
    title: title.value,
    content: content.value,
    created_at: datetime.value,
  }

  store.createPost(bookId, payload)
    .then(() => {
      router.push({ name: 'posts'})
    })
    .catch(() => {
      alert('작성에 실패했습니다.')
    })
}

const handleCancel = () => {
  router.back()
}
</script>
