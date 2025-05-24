<template>
  <!-- 모달 코드를 넣어요 -->
  <div class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">📘 독서 상태 기록</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
          <p class="mb-2 small text-muted">독서 상태를 선택해주세요</p>
          <select v-model="status" class="form-select mb-3" id="select-state">
            <option value="done">완독</option>
            <option value="reading">읽는 중</option>
            <option value="stop">중단</option>
          </select>

          <!-- 완독 -->
          <div v-if="status === 'done'">
            <p class="mb-2 small text-muted">책을 읽기 시작한 날짜를 입력하세요</p>
            <input type="date" v-model="startDate" class="form-control mb-2" />

            <p class="mb-2 small text-muted">책을 모두 읽은 날짜를 입력하세요</p>
            <input type="date" v-model="endDate" class="form-control mb-2" />

            <p class="mb-2 small text-muted">한줄평을 남겨주세요 (선택사항)</p>
            <textarea v-model="comment" class="form-control" placeholder="한줄평 작성" />
          </div>

          <!-- 읽는 중 -->
          <div v-if="status === 'reading'">
            <p class="mb-2 small text-muted">책을 읽기 시작한 날짜를 입력하세요</p>
            <input type="date" v-model="startDate" class="form-control mb-2" />

            <p class="mb-2 small text-muted">현재까지 읽은 비율을 입력하세요</p>
            <input type="range" class="form-range mb-1" v-model="progress" min="0" max="100" />
            <div class="text-end mb-2">{{ progress }}%</div>
          </div>

          <!-- 중단 -->
          <div v-if="status === 'stop'">
            <p class="mb-2 small text-muted">책을 읽기 시작한 날짜를 입력하세요</p>
            <input type="date" v-model="startDate" class="form-control mb-2" />

            <p class="mb-2 small text-muted">책을 중단한 날짜를 입력하세요</p>
            <input type="date" v-model="endDate" class="form-control mb-2" />

            <p class="mb-2 small text-muted">중단한 이유를 입력해주세요</p>
            <textarea v-model="stopReason" class="form-control" placeholder="중단한 이유를 적어주세요" />
          </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeModal">닫기</button>
            <button class="btn btn-primary" @click="submitStatus">저장</button>
          </div>
        </div>
      </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  bookId: Number
})

const emit = defineEmits(['close', 'saved'])

const status = ref('done')
const startDate = ref('')
const endDate = ref('')
const comment = ref('')
const progress = ref(0)
const stopReason = ref('')

// 날짜 데이터 처리
const formatDate = (val) => {
  if (!val || val === '') return null
  // string이면 new Date(val), Date 객체면 그대로 사용 가능
  const date = new Date(val)
  if (isNaN(date)) return null
  return date.toISOString().slice(0, 10) // YYYY-MM-DD
}

// 제출 버튼
const submitStatus = () => {
  const payload = {
    status: status.value,
    start_date: formatDate(startDate.value),
    end_date: formatDate(endDate.value),
    comment: comment.value,
    progress: progress.value,
    stop_reason: stopReason.value,
  }

  emit('saved', { bookId: props.bookId, data: payload })
  emit('close')

  status.value = 'done'
  startDate.value = ''
  endDate.value = ''
  comment.value = ''
  progress.value = null
  stopReason.value = ''
}

// 닫기 버튼
const closeModal = () => {
  emit('close')
}
</script>

<style scoped>

</style>