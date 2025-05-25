<template>
  <div class="container py-5" style="max-width: 600px">
    <div class="card p-4 shadow-sm">
      <h3 class="mb-4">내 정보 수정</h3>

      <!-- 1단계: 비밀번호 인증 -->
      <template v-if="!isVerified">
        <div class="form-group mb-3">
          <label for="verify-password">비밀번호 입력</label>
          <input v-model="verifyPassword" type="password" id="verify-password" class="form-control" />
        </div>
        <button @click="verifyUser" class="btn btn-primary">확인</button>
      </template>

      <!-- 2단계: 수정 폼 -->
      <template v-else>
        <!-- 아이디 -->
        <div class="form-group mb-3">
          <label for="username">아이디</label>
          <input v-model="form.username" type="text" id="username" class="form-control" />
        </div>

        <!-- 이름 -->
        <div class="form-group mb-3">
          <label for="name">이름</label>
          <input v-model="form.name" type="text" id="name" class="form-control" />
        </div>

        <!-- 성별 (표시만) -->
        <div class="form-group mb-3">
          <label>성별</label>
          <input :value="form.gender === 'M' ? '남성' : '여성'" class="form-control" disabled />
        </div>

        <!-- 나이 (표시만) -->
        <div class="form-group mb-3">
          <label>나이</label>
          <input :value="form.age" class="form-control" disabled />
        </div>

        <!-- 비밀번호 변경 이건 아직 하지 말고 -->
        <!-- <div class="form-group mb-3">
          <label for="password">새 비밀번호</label>
          <input v-model="form.password" type="password" id="password" class="form-control" />
        </div> -->

        <!-- 프로필 이미지 업로드 -->
        <div class="form-group mb-4">
          <label for="profile_img">프로필 이미지</label>
          <input type="file" @change="onFileChange" accept="image/*" class="form-control" />
        </div>

        <div class="d-flex justify-content-between">
          <button @click="submitEdit" class="btn btn-primary">저장</button>
          <RouterLink :to="{ name: 'mypage' }" class="btn btn-secondary">취소</RouterLink>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const isVerified = ref(false)
const verifyPassword = ref('')

const API_ACCOUNT_URL = 'http://127.0.0.1:8000/api/v1/accounts'

const form = ref({
  username: '',
  name: '',
  age: 0,
  gender: '',
  password: '',
})

const selectedFile = ref(null)

onMounted(async () => {
  try {
    const res = await axios.get(`${API_ACCOUNT_URL}/mypage/`, {
      headers: {
        Authorization: `Token ${localStorage.getItem('access_token')}`
      }
    })
    const data = res.data
    form.value.username = data.username
    form.value.name = data.name
    form.value.age = data.age
    form.value.gender = data.gender
  } catch (err) {
    alert('사용자 정보를 불러오지 못했습니다.')
    console.error(err)
  }
})

const verifyUser = async () => {
  try {
    const res = await axios.post(`${API_ACCOUNT_URL}/verify-password/`, {
      password: verifyPassword.value
    }, {
      headers: {
        Authorization: `Token ${localStorage.getItem('access_token')}`
      }
    })
    if (res.status === 200) isVerified.value = true
  } catch (err) {
    alert('비밀번호가 올바르지 않습니다.')
  }
}

const onFileChange = (event) => {
  selectedFile.value = event.target.files[0]
}

const submitEdit = async () => {
  try {
    const formData = new FormData()
    formData.append('username', form.value.username)
    formData.append('name', form.value.name)
    formData.append('password', form.value.password)
    if (selectedFile.value) {
      formData.append('profile_img', selectedFile.value)
    }

    const res = await axios.patch(`${API_ACCOUNT_URL}/mypage/`, formData, {
      headers: {
        Authorization: `Token ${localStorage.getItem('access_token')}`,
        'Content-Type': 'multipart/form-data'
      }
    })

    alert('✅ 정보가 성공적으로 수정되었습니다.')
    router.push({ name: 'mypage' })
  } catch (err) {
    alert('❌ 수정 실패: ' + JSON.stringify(err.response?.data || err))
  }
}
</script>

<style scoped>
.form-group label {
  font-weight: 600;
}
</style>
