<template>
  <div class="container py-5" style="max-width: 600px">
    <div class="card shadow p-4">
      <h4 class="mb-4 text-center">내 정보 수정</h4>

      <!-- 비밀번호 확인 단계 -->
      <div v-if="!verified">
        <label class="form-label">현재 비밀번호</label>
        <input type="password" class="form-control mb-3" v-model="password" />

        <button class="btn btn-dark w-100" @click="verify">비밀번호 확인</button>
      </div>

      <!-- 수정 폼 -->
      <form v-else @submit.prevent="submit">
        <div class="mb-3">
          <label class="form-label">이름</label>
          <input type="text" class="form-control" v-model="form.name" readonly />
        </div>

        <div class="mb-3">
          <label class="form-label">성별</label>
          <input type="text" class="form-control" :value="form.gender === 'M' ? '남성' : '여성'" readonly />
        </div>

        <div class="mb-3">
          <label class="form-label">나이</label>
          <input type="text" class="form-control" :value="form.age + '세'" readonly />
        </div>

        <div class="mb-3">
          <label class="form-label">아이디</label>
          <input type="text" class="form-control" v-model="form.username" required />
        </div>

        <div class="mb-3">
          <label class="form-label">새 비밀번호 (선택)</label>
          <input type="password" class="form-control" v-model="form.password1" />
        </div>

        <div class="mb-3">
          <label class="form-label">새 비밀번호 확인</label>
          <input type="password" class="form-control" v-model="form.password2" />
        </div>

        <div class="mb-3">
          <label class="form-label">프로필 이미지</label>
          <input type="file" class="form-control" @change="handleImage" />
        </div>

        <button class="btn btn-primary w-100" type="submit">수정 완료</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const API_URL = 'http://127.0.0.1:8000/api/v1/accounts'

const verified = ref(false)
const password = ref('')
const profileImg = ref(null)

const form = ref({
  name: '',
  username: '',
  gender: '',
  age: '',
  password1: '',
  password2: ''
})

onMounted(() => {
  axios.get(`${API_URL}/mypage/`, {
    headers: {
      Authorization: `Token ${localStorage.getItem('access_token')}`
    }
  }).then(res => {
    const data = res.data
    form.value.name = data.name
    form.value.username = data.username
    form.value.gender = data.gender
    form.value.age = data.age
  })
})

const verify = async () => {
  try {
    await axios.post(`${API_URL}/verify-password/`, { password: password.value }, {
      headers: {
        Authorization: `Token ${localStorage.getItem('access_token')}`
      }
    })
    verified.value = true
  } catch (err) {
    alert('비밀번호가 일치하지 않습니다.')
  }
}

const handleImage = (e) => {
  profileImg.value = e.target.files[0]
}

const submit = async () => {
  const formData = new FormData()
  formData.append('name', form.value.name)
  formData.append('username', form.value.username)
  if (form.value.password1) {
    formData.append('password1', form.value.password1)
    formData.append('password2', form.value.password2)
  }
  if (profileImg.value) {
    formData.append('profile_img', profileImg.value)
  }

  try {
    await axios.patch(`${API_URL}/mypage/`, formData, {
      headers: {
        Authorization: `Token ${localStorage.getItem('access_token')}`,
        'Content-Type': 'multipart/form-data'
      }
    })
    alert('정보가 수정되었습니다.')
    router.push({ name: 'mypage' })
  } catch (err) {
    alert('수정 실패')
  }
}
</script>

<style scoped>
input {
  font-size: 0.95rem;
}
</style>
