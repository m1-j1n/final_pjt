<template>
  <div class="edit-container">
    <div class="card shadow p-4">
      <h2 class="form-title">내 정보 수정</h2>

      <!-- 비밀번호 확인 단계 -->
      <div v-if="!verified">
        <div class="form-group">
          <label>현재 비밀번호</label>
          <input type="password" class="form-control" v-model="password" />
        </div>
          <div class="text-center">
            <button class="submit-btn mt-3" @click="verify">비밀번호 확인</button>
          </div>
      </div>

      <!-- 수정 폼 -->
      <form v-else @submit.prevent="submit" class="edit-form">
        <div class="form-group">
          <label>이름</label>
          <input type="text" class="form-control" v-model="form.name" readonly />
        </div>

        <div class="form-group">
          <label>성별</label>
          <input type="text" class="form-control" :value="form.gender === 'M' ? '남성' : '여성'" readonly />
        </div>

        <div class="form-group">
          <label>나이</label>
          <input type="text" class="form-control" :value="form.age + '세'" readonly />
        </div>

        <div class="form-group">
          <label>아이디</label>
          <input type="text" class="form-control" v-model="form.username" required />
        </div>

        <div class="form-group">
          <label>새 비밀번호 (선택)</label>
          <input type="password" class="form-control" v-model="form.password1" />
        </div>

        <div class="form-group">
          <label>새 비밀번호 확인</label>
          <input type="password" class="form-control" v-model="form.password2" />
        </div>

        <div class="form-group">
          <label>프로필 이미지</label>
          <input type="file" class="form-control" @change="handleImage" />
        </div>

        <button type="submit" class="submit-btn mt-4">수정 완료</button>
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
      Authorization: `Token ${localStorage.getItem('token')}`
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
        Authorization: `Token ${localStorage.getItem('token')}`
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
        Authorization: `Token ${localStorage.getItem('token')}`,
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
.edit-container {
  max-width: 480px;
  margin: 80px auto;
  background-color: #fff;
}

.card {
  border-radius: 1rem;
  border: 1px solid #e9ecef;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
}

.form-title {
  font-size: 1.7rem;
  font-weight: 700;
  text-align: center;
  color: #343a40;
  margin-bottom: 2rem;
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 1.3rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  text-align: left;
}

label {
  margin-bottom: 0.4rem;
  font-weight: 500;
  font-size: 0.95rem;
  color: #495057;
}

input[type="text"],
input[type="password"],
input[type="file"] {
  padding: 0.6rem 0.8rem;
  font-size: 1rem;
  border-radius: 0.6rem;
  border: 1px solid #ced4da;
  background-color: #fff;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

input:focus {
  border-color: #74b9ff;
  box-shadow: 0 0 0 0.15rem rgba(116, 185, 255, 0.25);
  outline: none;
}

.submit-btn {
  padding: 0.75rem 2rem;
  font-size: 1rem;
  font-weight: 600;
  background-color: #f8a33b;
  color: #fff;
  border: none;
  border-radius: 999px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
}

.submit-btn:hover {
  background-color: #f29b2f;
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
}
</style>
