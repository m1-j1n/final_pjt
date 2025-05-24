<template>
    <div>
      <h5>💬 댓글</h5>
  
      <form @submit.prevent="submitComment" class="mb-3">
        <textarea v-model="newComment" class="form-control mb-2" rows="2" placeholder="댓글을 입력하세요" />
        <button class="btn btn-sm btn-primary" :disabled="!newComment.trim()">작성</button>
      </form>
  
      <ul class="list-group">
        <li v-for="comment in comments" :key="comment.id" class="list-group-item d-flex justify-content-between align-items-start">
          <div>
            <strong>{{ comment.user }}</strong><br />
            {{ comment.content }}
          </div>
          <small class="text-muted">{{ formatDate(comment.created_at) }}</small>
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
  
  const formatDate = (iso) => new Date(iso).toLocaleString()
  
  onMounted(fetchComments)
  </script>