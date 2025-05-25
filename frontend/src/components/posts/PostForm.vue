<template>
  <div class="card p-4 shadow">
    <h4 class="mb-4 text-center">📝 새 포스트 작성</h4>

    <div class="mb-3">
      <label class="form-label">제목</label>
      <input v-model="title" class="form-control" />
    </div>

    <div class="mb-3">
      <label class="form-label">내용</label>
      <textarea v-model="content" class="form-control" rows="5"></textarea>
    </div>

    <!-- <div class="mb-3">
      <label class="form-label">읽은 날짜</label>
      <input v-model="datetime" type="datetime-local" class="form-control" />
    </div> -->

    <div class="mb-3">
      <label class="form-label">이미지 업로드</label>
      <input type="file" class="form-control" @change="handleImageUpload" />
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
const imageFile = ref(null)

const store = usePostStore()
const router = useRouter()
const route = useRoute()

const bookId = Number(route.params.bookId)

const handleImageUpload = (e) => {
  imageFile.value = e.target.files[0]
}

const handleSubmit = () => {
  if (!title.value || !content.value) {
    alert('제목과 내용을 모두 입력하세요.')
    return
  }

  const formData = new FormData()
  formData.append('title', title.value)
  formData.append('content', content.value)
  // formData.append('created_at', datetime.value)

  if (imageFile.value) {
    formData.append('cover_img', imageFile.value)
  }

  store.createPost(bookId, formData)
    .then(() => {
      router.push({ name: 'posts' })
    })
    .catch(() => {
      alert('작성에 실패했습니다.')
      
    })
}

const handleCancel = () => {
  router.back()
}
</script>

<style scoped>
textarea.form-control {
  min-height: 200px;
  resize: vertical;
}
</style>