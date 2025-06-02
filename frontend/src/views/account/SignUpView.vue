<template>
  <div class="signup-container">
    <div class="card">
      <h2 class="title">회원가입</h2>
      <form @submit.prevent="onSignUp">
        <!-- 아이디 (이메일) -->
        <div class="form-group">
          <label for="username">이메일</label>
          <input id="username" type="text" v-model="username" required />
          <span v-if="username && !isEmailValid" class="error-message">❌ 유효한 이메일 형식이 아닙니다.</span>
        </div>

        <!-- 이름 -->
        <div class="form-group">
          <label for="name">이름</label>
          <input id="name" type="text" v-model="name" required />
        </div>

        <!-- 비밀번호 -->
        <div class="form-group">
          <label for="password1">비밀번호</label>
          <input id="password1" type="password" v-model="password1" required />
        </div>

        <!-- 비밀번호 확인 -->
        <div class="form-group">
          <label for="password2">비밀번호 확인</label>
          <input id="password2" type="password" v-model="password2" required />
          <span v-if="passwordMismatch" class="error-message">❌ 비밀번호가 일치하지 않습니다.</span>
        </div>

        <!-- 성별 -->
        <div class="form-group">
          <label for="gender">성별</label>
          <select id="gender" v-model="gender" required>
            <option disabled value="">선택</option>
            <option value="M">남성</option>
            <option value="F">여성</option>
          </select>
        </div>

        <!-- 나이 -->
        <div class="form-group">
          <label for="age">나이</label>
          <input id="age" type="number" v-model.number="age" min="1" required />
        </div>

        <!-- 서버 응답 에러 메시지 -->
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

        <div class="submit-group">
          <input type="submit" value="회원가입" />
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const username = ref('')
const name = ref('')
const password1 = ref('')
const password2 = ref('')
const gender = ref('')
const age = ref(0)
const errorMessage = ref('')

// 이메일 유효성 검사
const isEmailValid = computed(() => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(username.value)
})

// 비밀번호 불일치 검사
const passwordMismatch = computed(() => {
  return password1.value !== password2.value && password2.value !== ''
})

const onSignUp = async () => {
  errorMessage.value = ''

  if (!isEmailValid.value) {
    errorMessage.value = '❌ 이메일 형식이 올바르지 않습니다.'
    return
  }

  if (passwordMismatch.value) {
    errorMessage.value = '❌ 비밀번호가 일치하지 않습니다.'
    return
  }

  if (!age.value || age.value <= 0) {
    errorMessage.value = '❌ 나이를 올바르게 입력해주세요.'
    return
  }

  const userInfo = {
    username: username.value,
    name: name.value,
    password1: password1.value,
    password2: password2.value,
    gender: gender.value,
    age: Number(age.value),
  }

  try {
  
    const ACCOUNT_API_URL = 'http://13.124.181.201:8000/api/v1/accounts'
    // 회원가입 요청
    await axios.post( `${ACCOUNT_API_URL}/signup/`, userInfo)

    // 회원가입 성공 후 로그인 시도
    const loginRes = await axios.post('http://13.124.181.201:8000/api/v1/auth/login/', {
      username: userInfo.username,
      password: userInfo.password1,
    })

    // 토큰 저장
    const token = loginRes.data.key
    localStorage.setItem('token', token)

    // 설문 페이지로 이동
    router.push({ name: 'onboarding-survey' })

  } catch (err) {
    console.error('❌ 에러 응답:', err.response?.data || err)
    // errorMessage.value = Object.values(err.response?.data || { error: '오류 발생' }).flat().join(', ')
  }
}
</script>

<style scoped>
.signup-container {
  display: flex;
  justify-content: center;
  min-height: 65vh;
  background-color: #f8f9fa;
  padding: 2rem 1rem;
}

.card {
  background: #ffffff;
  padding: 2.5rem 2rem;
  border-radius: 1rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
  max-width: 500px;
  width: 100%;
  border: 1px solid #e9ecef;
}

.title {
  font-size: 1.7rem;
  font-weight: 700;
  text-align: center;
  color: #343a40;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.3rem;
  display: flex;
  flex-direction: column;
}

label {
  font-weight: 500;
  font-size: 0.95rem;
  color: #495057;
  margin-bottom: 0.4rem;
}

input,
select {
  padding: 0.6rem 0.8rem;
  border: 1px solid #ced4da;
  border-radius: 0.6rem;
  font-size: 1rem;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  background-color: #fff;
}

input:focus,
select:focus {
  border-color: #74b9ff;
  box-shadow: 0 0 0 0.15rem rgba(116, 185, 255, 0.25);
  outline: none;
}

.error-message {
  color: #d9534f;
  font-size: 0.85rem;
  margin-top: 0.3rem;
}

.submit-group {
  margin-top: 2rem;
  display: flex;
  justify-content: center;
}

input[type="submit"] {
  background-color: #f8a33b;
  color: #fff;
  padding: 0.75rem 2rem;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: 999px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
}

input[type="submit"]:hover {
  background-color: #f29b2f;
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
}

</style>
