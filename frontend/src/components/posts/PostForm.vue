<template>
  <div class="post-form-wrapper container py-5" style="max-width: 640px">
    <div class="card-section shadow-block p-5">
      <h4 class="fw-bold text-center mb-4">새 포스트 작성</h4>

      <div class="mb-3">
        <label class="form-label fw-semibold">제목</label>
        <input v-model="title" class="form-control input-rounded" placeholder="예: 인생 책을 소개해보세요" />
      </div>

      <div class="mb-3">
        <label class="form-label fw-semibold">내용</label>
        <textarea v-model="content" class="form-control input-rounded" rows="6" placeholder="책을 읽고 느낀 점을 자유롭게 작성해주세요 :)"></textarea>
      </div>

      <div class="mb-3">
        <label class="form-label fw-semibold">이미지 업로드</label>
        <input type="file" class="form-control input-rounded" @change="handleImageUpload" />
      </div>

      <div class="d-flex justify-content-center gap-3 mt-4">
        <button class="btn btn-outline-secondary rounded-pill px-4" @click="handleCancel">취소</button>
        <button class="btn bookie-btn rounded-pill px-4" @click="handleSubmit">작성</button>
      </div>
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
.card-section {
  background-color: #ffffff;
  border-radius: 1.25rem;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
  border: 1px solid #dee2e6;
}

.input-rounded {
  border-radius: 12px;
  font-size: 0.95rem;
  padding: 0.6rem 0.9rem;
  border: 1px solid #ced4da;
}

.input-rounded:focus {
  border-color: #f8a33b;
  box-shadow: 0 0 0 0.15rem rgba(248, 163, 59, 0.25);
  outline: none;
}

.form-label {
  font-size: 0.9rem;
  color: #495057;
}

textarea.form-control {
  resize: vertical;
}

.bookie-btn {
  background-color: #f8a33b;
  color: #fff;
  font-weight: 600;
  border: none;
  transition: background-color 0.3s ease, transform 0.2s ease;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

.bookie-btn:hover {
  background-color: #f29b2f;
  transform: translateY(-1px);
  box-shadow: 0 6px 14px rgba(0, 0, 0, 0.1);
}
</style>