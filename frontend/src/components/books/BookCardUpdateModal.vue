<template>
  <div class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content fixed-modal">
        <div class="modal-header">
          <h5 class="modal-title">📘 독서 상태 수정</h5>
          <button type="button" class="btn-close" @click="closeModal"></button>
        </div>
        <div class="modal-body">
          <!-- 상태 선택 -->
          <p class="mb-2 small text-muted">독서 상태를 선택해주세요</p>
          <div class="btn-group w-100 mb-3" role="group">
            <input type="radio" class="btn-check" id="btn-done" value="done" v-model="status" autocomplete="off" />
            <label class="btn btn-outline-primary" for="btn-done">✅ 완독</label>

            <input type="radio" class="btn-check" id="btn-reading" value="reading" v-model="status" autocomplete="off" />
            <label class="btn btn-outline-success" for="btn-reading">📖 읽는 중</label>

            <input type="radio" class="btn-check" id="btn-stop" value="stop" v-model="status" autocomplete="off" />
            <label class="btn btn-outline-danger" for="btn-stop">⛔ 중단</label>
          </div>

          <!-- 상태별 입력 필드 -->
          <div v-if="status === 'done'">
            <input type="date" v-model="startDate" class="form-control mb-2" placeholder="시작일" />
            <input type="date" v-model="endDate" class="form-control mb-2" placeholder="종료일" />
            <textarea v-model="comment" class="form-control" placeholder="한줄평 (선택)" />
          </div>

          <div v-if="status === 'reading'">
            <input type="date" v-model="startDate" class="form-control mb-2" placeholder="시작일" />
            <label class="form-label">읽은 비율: {{ progress }}%</label>
            <input type="range" v-model="progress" class="form-range" min="0" max="100" />
          </div>

          <div v-if="status === 'stop'">
            <input type="date" v-model="startDate" class="form-control mb-2" placeholder="시작일" />
            <input type="date" v-model="stopDate" class="form-control mb-2" placeholder="중단일" />
            <textarea v-model="stopReason" class="form-control" placeholder="중단 이유를 적어주세요" />
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-outline-danger me-auto" @click="deleteStatus">삭제</button>
          <button class="btn btn-secondary" @click="closeModal">닫기</button>
          <button class="btn btn-primary" @click="submitStatus">수정 저장</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Swal from 'sweetalert2'
import { useUserStore } from '@/stores/users'

const props = defineProps({
  bookId: Number,
  initialData: Object,
})

const emit = defineEmits(['close', 'updated', 'deleted'])

const userStore = useUserStore()

const status = ref('done')
const startDate = ref('')
const endDate = ref('')
const stopDate = ref('')
const comment = ref('')
const progress = ref(0)
const stopReason = ref('')

onMounted(() => {
  if (props.initialData) {
    status.value = props.initialData.status || 'done'
    startDate.value = props.initialData.start_date || ''
    endDate.value = props.initialData.end_date || ''
    stopDate.value = props.initialData.stop_date || ''
    comment.value = props.initialData.comment || ''
    progress.value = props.initialData.progress ?? 0
    stopReason.value = props.initialData.stop_reason || ''
  }
})

const formatDate = (val) => {
  if (!val) return null
  const date = new Date(val)
  return isNaN(date) ? null : date.toISOString().slice(0, 10)
}

const submitStatus = () => {
  const payload = {
    status: status.value,
    start_date: formatDate(startDate.value),
    end_date: formatDate(endDate.value),
    stop_date: formatDate(stopDate.value),
    comment: comment.value,
    progress: progress.value,
    stop_reason: stopReason.value,
  }

  emit('updated', {
    bookId: props.bookId,
    data: payload,
    mode: 'edit',
  })
  emit('close')
}

const deleteStatus = async () => {
  const confirmed = await Swal.fire({
    icon: 'warning',
    title: '정말 삭제하시겠어요?',
    text: '기록이 완전히 삭제됩니다.',
    showCancelButton: true,
    confirmButtonText: '삭제',
    cancelButtonText: '취소',
  })

  if (confirmed.isConfirmed) {
    try {
      await axios.delete(`http://localhost:8000/api/v1/books/${props.bookId}/reading-status/`, {
        headers: {
          Authorization: `Token ${userStore.token}`,
        },
      })
      emit('deleted')
      emit('close')
    } catch (err) {
      console.error('삭제 실패:', err)
    }
  }
}

const closeModal = () => {
  emit('close')
}
</script>

<style scoped>
.fixed-modal {
  min-height: 480px;
  display: flex;
  flex-direction: column;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
}

.form-range {
  accent-color: #198754;
}
</style>
