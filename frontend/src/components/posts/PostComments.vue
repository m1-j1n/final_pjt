<template>
    <div>
      <h5>💬 댓글</h5>
  
      <form @submit.prevent="submitComment" class="mb-3 d-flex align-items-start gap-2">
        <textarea
          v-model="newComment"
          class="form-control"
          rows="2"
          placeholder="댓글을 입력하세요"
          style="resize: none;"
        />
        <button
          class="btn btn-primary"
          :disabled="!newComment.trim()"
          style="white-space: nowrap;"
        >
          작성
        </button>
      </form>
  
      <ul class="list-group">
        <li v-for="comment in comments" :key="comment.id" class="list-group-item d-flex justify-content-between align-items-start">
          <div class="flex-grow-1">
              <strong>{{ comment.user }}</strong><br />
              {{ comment.content }}
            </div>
            <div class="text-end d-flex flex-column align-items-end">
              <small class="text-muted mb-1">{{ formatDate(comment.created_at) }}</small>
              <button
                v-if="comment.user === userStore.username"
                class="btn btn-sm btn-outline-danger btn-delete"
                @click="deleteComment(comment.id)"
              >
                삭제
              </button>
            </div>
        </li>
      </ul>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  import { useUserStore } from '@/stores/users'
  
  const props = defineProps({ postId: Number })
  const newComment = ref('')
  const comments = ref([])
  const userStore = useUserStore()
  
  // 댓글 정보 가져오기
  const fetchComments = async () => {
    const res = await axios.get(`http://localhost:8000/api/v1/posts/${props.postId}/comments/`)
    comments.value = res.data
  }
  
  // 댓글 제출하기
  const submitComment = async () => {
    await axios.post(
      `http://localhost:8000/api/v1/posts/${props.postId}/comments/create/`,
      { content: newComment.value },
      {
        headers: {
          Authorization: `Token ${userStore.token}`,
        }
      }
    )
    newComment.value = ''
    await fetchComments()
  }
  
  // 댓글 삭제하기
  const deleteComment = async (commentId) => {
  try {
    await axios.delete(`http://localhost:8000/api/v1/comments/${commentId}/delete/`, {
      headers: {
        Authorization: `Token ${userStore.token}`,
      },
    })
    await fetchComments()
  } catch (err) {
    alert('댓글 삭제에 실패했습니다.')
    console.error(err)
  }
}

  const formatDate = (iso) => new Date(iso).toLocaleString()
  
  onMounted(fetchComments)
  </script>