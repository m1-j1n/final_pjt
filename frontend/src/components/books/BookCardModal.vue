<template>
  <div class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 rounded-4 shadow fixed-modal">
        <div class="modal-header border-0 pb-2">
          <h5 class="modal-title fw-bold">독서 상태 기록</h5>
          <button type="button" class="btn-close" @click="closeModal"></button>
        </div>

        <div class="modal-body pt-0">
          <p class="small text-muted mb-3">현재 책의 독서 상태를 선택해주세요.</p>
          <div class="btn-group w-100 mb-4" role="group">
            <input type="radio" class="btn-check" id="btn-done" value="done" v-model="status" autocomplete="off" />
            <label class="btn btn-outline-secondary rounded-start-pill" for="btn-done">완독</label>

            <input type="radio" class="btn-check" id="btn-reading" value="reading" v-model="status" autocomplete="off" />
            <label class="btn btn-outline-secondary" for="btn-reading">읽는 중</label>

            <input type="radio" class="btn-check" id="btn-stop" value="stop" v-model="status" autocomplete="off" />
            <label class="btn btn-outline-secondary rounded-end-pill" for="btn-stop">중단</label>
          </div>

          <!-- ✅ 완독 -->
          <div v-if="status === 'done'" class="mb-3">
            <label class="form-label small text-muted">시작일</label>
            <input type="date" v-model="startDate" class="form-control mb-3" />

            <label class="form-label small text-muted">완독일</label>
            <input type="date" v-model="endDate" class="form-control mb-3" />

            <label class="form-label small text-muted">한줄평 (선택)</label>
            <textarea v-model="comment" class="form-control" rows="3" placeholder="예: 몰입감 넘치는 이야기였습니다." />
          </div>

          <!-- ✅ 읽는 중 -->
          <div v-if="status === 'reading'" class="mb-3">
            <label class="form-label small text-muted">시작일</label>
            <input type="date" v-model="startDate" class="form-control mb-3" />

            <label class="form-label small d-flex justify-content-between align-items-center mb-2 text-secondary">
              <span class="fw-medium">읽은 비율</span>
              <span class="badge bg-light text-dark border">{{ progress }}%</span>
            </label>
            <input
              type="range"
              class="form-range progress-range"
              v-model="progress"
              min="0"
              max="100"
            />
          </div>

          <!-- ✅ 중단 -->
          <div v-if="status === 'stop'" class="mb-3">
            <label class="form-label small text-muted">시작일</label>
            <input type="date" v-model="startDate" class="form-control mb-3" />

            <label class="form-label small text-muted">중단일</label>
            <input type="date" v-model="stopDate" class="form-control mb-3" />

            <label class="form-label small text-muted">중단한 이유</label>
            <textarea v-model="stopReason" class="form-control" rows="3" placeholder="예: 흥미가 가지 않았어요." />
          </div>
        </div>

        <div class="modal-footer border-0 pt-0">
          <button class="btn btn-outline-dark rounded-pill px-4" @click="closeModal">닫기</button>
          <button class="btn btn-dark rounded-pill px-4" @click="submitStatus">저장</button>
        </div>
      </div>
    </div>
  </div>
</template>



<script setup>
import { ref } from 'vue'
import Swal from 'sweetalert2'

const props = defineProps({
  bookId: Number
})

const emit = defineEmits(['close', 'saved'])

const status = ref('done')
const startDate = ref('')
const endDate = ref('')
const stopDate = ref('')
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
  // 유효성 검사
  if (status.value === 'done') {
    if (!startDate.value || !endDate.value) {
      Swal.fire({
        icon: 'info',
        title: '입력이 필요합니다',
        text: '완독 상태를 저장하려면 시작일과 완독일을 모두 입력해주세요.',
        confirmButtonText: '확인',
      })
      return
    }
  } else if (status.value === 'reading') {
    if (!startDate.value) {
      Swal.fire({
        icon: 'info',
        title: '입력이 필요합니다',
        text: '읽는 중 상태를 저장하려면 시작일을 입력해주세요.',
        confirmButtonText: '확인',
      })
      return
    }
  } else if (status.value === 'stop') {
    if (!startDate.value || !stopDate.value) {
      Swal.fire({
        icon: 'info',
        title: '입력이 필요합니다',
        text: '중단 상태를 저장하려면 시작일과 중단일을 모두 입력해주세요.',
        confirmButtonText: '확인',
      })
      return
    }
  }

  // 유효하면 저장 진행
  const payload = {
    status: status.value,
    start_date: formatDate(startDate.value),
    end_date: formatDate(endDate.value),
    stop_date: formatDate(stopDate.value),
    comment: comment.value,
    progress: progress.value,
    stop_reason: stopReason.value,
  }

  emit('saved', { bookId: props.bookId, data: payload })
  emit('close')

  // 초기화
  status.value = 'done'
  startDate.value = ''
  endDate.value = ''
  stopDate.value = ''
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
.fixed-modal {
  height: 550px;
  display: flex;
  max-height: 90vh;
  flex-direction: column;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
}

/* 선택 UI를 자연스럽게 보이도록 */
.state-button-group {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  gap: 0.5rem;
}

.state-button-group button {
  flex: 1;
}

.reading-progress {
  padding: 0.5rem 0;
}

.custom-range {
  accent-color: #198754; /* Bootstrap success 색상 */
  height: 6px;
  border-radius: 3px;
  background-color: #e9ecef;
}
</style>