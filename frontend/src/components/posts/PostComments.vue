<template>
  <div class="comment-wrapper mt-4">
    <h5 class="fw-bold mb-3">댓글</h5>

    <!-- 댓글 작성 -->
    <form @submit.prevent="submitComment" class="d-flex align-items-start gap-2 mb-4">
      <textarea
        v-model="newComment"
        class="form-control rounded-3 shadow-sm"
        rows="2"
        placeholder="댓글을 입력하세요"
        style="resize: none;"
      />
      <button
        class="btn btn-comment-submit"
        :disabled="!newComment.trim()"
      >
        작성
      </button>
    </form>

    <!-- 댓글 리스트 -->
    <ul class="list-unstyled">
      <li
        v-for="comment in comments"
        :key="comment.id"
        class="comment-item mb-3 p-3 rounded-4 border bg-white shadow-sm"
      >
        <div class="d-flex justify-content-between align-items-start">
          <div class="flex-grow-1">
            <strong class="text-dark">{{ comment.user }}</strong>
            <p class="mb-1 mt-1 text-body">{{ comment.content }}</p>
          </div>
          <div class="text-end d-flex flex-column align-items-end">
            <small class="text-muted mb-1">{{ formatDate(comment.created_at) }}</small>
            <button
              v-if="comment.user === userStore.username"
              class="btn btn-delete-comment"
              @click="deleteComment(comment.id)"
            >
              삭제
            </button>
          </div>
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

<style scoped>
.btn-comment-submit {
  background-color: #f8a33b;
  color: #fff;
  font-weight: 600;
  padding: 0.55rem 1.4rem;
  font-size: 0.95rem;
  border: none;
  border-radius: 0.75rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
  white-space: nowrap;         /* ✅ 줄바꿈 방지 */
  min-width: 64px;             /* ✅ 최소 너비 지정 */
  text-align: center;
  align-self: stretch;     
}

.btn-comment-submit:hover {
  background-color: #f29b2f;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.12);
}

.btn-delete-comment {
  background-color: #f1f3f5;
  color: #6c757d;
  font-size: 0.85rem;
  padding: 0.4rem 0.9rem;
  border: 1px solid #ced4da;
  border-radius: 0.6rem;
  transition: background-color 0.2s ease, color 0.2s ease;
}

.btn-delete-comment:hover {
  background-color: #e9ecef;
  color: #495057;
}

.comment-item {
  transition: box-shadow 0.2s ease;
}

.comment-item:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.05);
}
</style>