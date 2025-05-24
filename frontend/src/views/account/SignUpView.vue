<template>
  <div class="signup-container">
    <div class="card">
      <h2 class="title">회원가입</h2>
      <form @submit.prevent="onSignUp">
        <div class="form-group">
          <label for="username">아이디</label>
          <input id="username" type="text" v-model="username" required />
        </div>

        <div class="form-group">
          <label for="name">이름</label>
          <input id="name" type="text" v-model="name" required />
        </div>

        <div class="form-group">
          <label for="password1">비밀번호</label>
          <input id="password1" type="password" v-model="password1" required />
        </div>

        <div class="form-group">
          <label for="password2">비밀번호 확인</label>
          <input id="password2" type="password" v-model="password2" required />
        </div>

        <div class="form-group">
          <label for="gender">성별</label>
          <select id="gender" v-model="gender" required>
            <option disabled value="">선택</option>
            <option value="M">남성</option>
            <option value="F">여성</option>
          </select>
        </div>

        <div class="form-group">
          <label for="age">나이</label>
          <input id="age" type="number" v-model.number="age" min="1" required />
        </div>

        <!-- <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p> -->

        <div class="submit-group">
          <input type="submit" value="회원가입" />
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
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

const onSignUp = async () => {
  errorMessage.value = ''

  if (password1.value !== password2.value) {
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
    // 1. 회원가입
    await axios.post('http://127.0.0.1:8000/accounts/signup/', userInfo)

    // 2. 회원가입 성공 → 로그인
    const loginRes = await axios.post('http://127.0.0.1:8000/accounts/login/', {
      username: userInfo.username,
      password: userInfo.password1,
    })

    // 3. 토큰 저장
    const token = loginRes.data.key
    localStorage.setItem('access_token', token)

    // 4. 설문 페이지로 이동
    router.push({ name: 'onboarding-survey' })
  } catch (err) {
    console.error('❌ 에러 응답:', err.response?.data || err)
    errorMessage.value = Object.values(err.response?.data || { error: '오류 발생' }).flat().join(', ')
  }
}
</script>

<style scoped>
.signup-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #f5f5fa;
}
.card {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  width: 100%;
}
.title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  text-align: center;
}
.form-group {
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
}
label {
  font-weight: 600;
  margin-bottom: 0.5rem;
}
input,
select {
  padding: 0.6rem;
  border: 1px solid #ccc;
  border-radius: 0.5rem;
  font-size: 1rem;
}
.error-message {
  color: red;
  text-align: center;
  margin-top: 1rem;
}
.submit-group {
  margin-top: 1.5rem;
  display: flex;
  justify-content: center;
}
input[type="submit"] {
  background: #4caf50;
  color: white;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: bold;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
input[type="submit"]:hover {
  background-color: #388e3c;
}
</style>
