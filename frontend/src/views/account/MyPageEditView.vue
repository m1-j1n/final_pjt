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
        <!-- 기본 정보 -->
        <div class="form-group mb-3">
          <label for="username">아이디</label>
          <input v-model="form.username" type="text" id="username" class="form-control" />
        </div>

        <div class="form-group mb-3">
          <label for="name">이름</label>
          <input v-model="form.name" type="text" id="name" class="form-control" />
        </div>

        <div class="form-group mb-3">
          <label>성별</label>
          <input :value="form.gender === 'M' ? '남성' : '여성'" class="form-control" disabled />
        </div>

        <div class="form-group mb-3">
          <label>나이</label>
          <input :value="form.age" class="form-control" disabled />
        </div>

        <div class="form-group mb-4">
          <label for="profile_img">프로필 이미지</label>
          <input type="file" @change="onFileChange" accept="image/*" class="form-control" />
        </div>

        <!-- 설문 정보 수정 -->
        <div class="form-group mb-3">
          <label>라이프스타일</label>
          <select v-model="preference.lifestyle" class="form-control">
            <option v-for="item in lifestyles" :key="item.id" :value="item.id">{{ item.name }}</option>
          </select>
        </div>

        <div class="form-group mb-3">
          <label>독서 스타일</label>
          <select v-model="preference.preferred_reading_style" class="form-control">
            <option v-for="item in readingStyles" :key="item.id" :value="item.id">{{ item.name }}</option>
          </select>
        </div>

        <div class="form-group mb-3">
          <label>기피 키워드</label>
          <input v-model="preference.avoided_keywords" type="text" class="form-control" />
        </div>

        <div class="form-group mb-3">
          <label>주간 평균 독서 시간</label>
          <input v-model="preference.weekly_avg_reading_time" type="number" class="form-control" />
        </div>

        <div class="form-group mb-4">
          <label>연간 독서량</label>
          <input v-model="preference.annual_reading_amount" type="number" class="form-control" />
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

const preference = ref({
  lifestyle: null,
  preferred_reading_style: null,
  avoided_keywords: '',
  weekly_avg_reading_time: 0,
  annual_reading_amount: 0,
})

const lifestyles = ref([])
const readingStyles = ref([])

onMounted(async () => {
  try {
    const [userRes, prefRes, lifeRes, styleRes] = await Promise.all([
      axios.get(`${API_ACCOUNT_URL}/mypage/`, {
        headers: { Authorization: `Token ${localStorage.getItem('access_token')}` }
      }),
      axios.get(`${API_ACCOUNT_URL}/preference/`, {
        headers: { Authorization: `Token ${localStorage.getItem('access_token')}` }
      }),
      axios.get(`${API_ACCOUNT_URL}/lifestyles/`),
      axios.get(`${API_ACCOUNT_URL}/readingstyles/`),
    ])

    const user = userRes.data
    form.value.username = user.username
    form.value.name = user.name
    form.value.age = user.age
    form.value.gender = user.gender

    Object.assign(preference.value, prefRes.data)
    lifestyles.value = lifeRes.data
    readingStyles.value = styleRes.data
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
    if (selectedFile.value) {
      formData.append('profile_img', selectedFile.value)
    }

    await axios.patch(`${API_ACCOUNT_URL}/mypage/`, formData, {
      headers: {
        Authorization: `Token ${localStorage.getItem('access_token')}`,
        'Content-Type': 'multipart/form-data'
      }
    })

    const cleanedPreference = {
      lifestyle: preference.value.lifestyle,
      preferred_reading_style: preference.value.preferred_reading_style,
      avoided_keywords: preference.value.avoided_keywords,
      weekly_avg_reading_time: preference.value.weekly_avg_reading_time,
      annual_reading_amount: preference.value.annual_reading_amount,
    }

    await axios.put(`${API_ACCOUNT_URL}/preference/`, cleanedPreference, {
      headers: {
        Authorization: `Token ${localStorage.getItem('access_token')}`
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
