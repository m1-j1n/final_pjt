<template>
  <div class="card p-4 shadow">
    <h4 class="mb-4 text-center">포스트 수정</h4>

    <div class="mb-3">
      <label class="form-label">제목</label>
      <input v-model="title" class="form-control" />
    </div>

    <div class="mb-3">
      <label class="form-label">내용</label>
      <textarea v-model="content" class="form-control" rows="5" />
    </div>

      <!-- 기존 이미지 미리보기 (서버에서 불러온) -->
      <img v-if="existingImageUrl && !previewUrl" :src="existingImageUrl" alt="기존 이미지"
        class="img-thumbnail mb-2 preview-img" />

      <!-- 새로 업로드한 이미지 미리보기 -->
      <img v-if="previewUrl" :src="previewUrl" alt="미리보기"
        class="img-thumbnail mb-2 preview-img" />
      <div class="mb-3">
      <label class="form-label">이미지 수정</label>
      <input type="file" class="form-control" @change="handleImageUpload" />
    </div>

    <div class="d-flex justify-content-center gap-3 mt-4">
      <button class="btn btn-outline-secondary rounded-pill px-4" @click="handleCancel">취소</button>
      <button class="btn bookie-btn rounded-pill px-4" @click="handleSubmit">작성</button>
    </div>
  </div>
</template>

<script setup>
import { API } from '@/api/api.js'
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { usePostStore } from '@/stores/post'
import { useUserStore } from '@/stores/users'
import axios from 'axios'
import Swal from 'sweetalert2'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const title = ref('')
const content = ref('')
const datetime = ref('')
const imageFile = ref(null)

const bookId = Number(route.params.bookId)
const postId = Number(route.params.postId)
const previewUrl = ref(null)

const handleImageUpload = (e) => {
  imageFile.value = e.target.files[0]
  if (imageFile.value) {
    previewUrl.value = URL.createObjectURL(imageFile.value)
  }
}

// 제출 버튼 클릭 시
const handleSubmit = async () => {
  if (!title.value || !content.value) {
    Swal.fire({
      icon: 'info',
      title: '입력 누락',
      text: '제목과 내용을 모두 입력해주세요.',
      confirmButtonText: '확인',
      customClass: {
        confirmButton: 'btn btn-primary rounded-pill px-4',
        popup: 'rounded-4',
      },
      buttonsStyling: false,
    })
    return
  }

  const formData = new FormData()
  formData.append('title', title.value)
  formData.append('content', content.value)
  formData.append('created_at', datetime.value)
  if (imageFile.value) {
    formData.append('cover_img', imageFile.value)
  }

  try {
    await axios.patch(API.POST.UPDATE(bookId, postId), formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Token ${userStore.token}`,
        },
      }
    )

    await Swal.fire({
      icon: 'success',
      title: '수정 완료!',
      text: '포스트가 성공적으로 수정되었습니다.',
      confirmButtonText: '확인',
      customClass: {
        confirmButton: 'btn btn-dark rounded-pill px-4',
        popup: 'rounded-4',
      },
      buttonsStyling: false,
    })

    router.push({ name: 'posts-detail', params: { postId } })

  } catch (err) {
    console.error('❌ 수정 실패:', err)
    Swal.fire({
      icon: 'error',
      title: '수정 실패',
      text: '문제가 발생했습니다. 다시 시도해주세요.',
      confirmButtonText: '확인',
      customClass: {
        confirmButton: 'btn btn-danger rounded-pill px-4',
        popup: 'rounded-4',
      },
      buttonsStyling: false,
    })
  }
}


// 취소 버튼 클릭 시
const handleCancel = () => {
  router.back()
}

const existingImageUrl = ref(null) // 기존 이미지 URL

onMounted(() => {
  axios.get(API.POST.DETAIL(bookId, postId))
    .then((res) => {
      const post = res.data
      title.value = post.title
      content.value = post.content
      datetime.value = post.created_at
      if (post.cover_img) {
        existingImageUrl.value = import.meta.env.VITE_API_URL + post.cover_img
      }
    })
    .catch((err) => {
      console.error('❌ 포스트 정보 불러오기 실패:', err)
      alert('포스트 정보를 불러오지 못했습니다.')
      router.back()
    })
})
</script>

<style scoped>
.preview-img {
  max-height: 300px;
  width: auto;
  display: block;
  margin: 0 auto;
  object-fit: contain;
}

/* 내용 textarea 높이 확장 */
textarea.form-control {
  min-height: 200px;
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
