<template>
  <div class="card p-4 shadow">
    <h4 class="mb-4 text-center">📝 포스트 수정</h4>

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
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { usePostStore } from '@/stores/post'
import axios from 'axios'

const router = useRouter()
const route = useRoute()

const title = ref('')
const content = ref('')
const datetime = ref('')

const bookId = Number(route.params.bookId)
const postId = Number(route.params.postId)

// 제출 버튼 클릭 시
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

   axios.put(`http://localhost:8000/api/v1/books/${bookId}/posts/${postId}/update/`, payload)
    .then(() => {
      alert('수정 완료되었습니다.')
      router.push({ name: 'posts-detail', params: { postId } })
    })
    .catch((err) => {
      console.error('❌ 수정 실패:', err)
      alert('수정에 실패했습니다.')
    })
}

// 취소 버튼 클릭 시
const handleCancel = () => {
  router.back()
}

// 마운트 시
onMounted(() => {
  axios.get(axios.get(`http://localhost:8000/api/v1/books/${bookId}/posts/${postId}/`)
  .then((res) => {
    const post = res.data
    title.value = post.title
    content.value = post.content
    datetime.value = post.created_at
  })
  .catch((err) => {
    console.error('❌ 포스트 정보 불러오기 실패:', err)
    alert('포스트 정보를 불러오지 못했습니다.')
    router.back()
  }))
})
</script>

<style scoped>

</style>
