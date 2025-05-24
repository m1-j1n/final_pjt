<template>
  <div class="login-container">
    <h2>로그인</h2>
    <form @submit.prevent="onLogIn" class="login-form">
      <div class="form-group">
        <label for="username">아이디</label>
        <input type="text" id="username" v-model="username" placeholder="아이디를 입력하세요" />
      </div>

      <div class="form-group">
        <label for="password">비밀번호</label>
        <input type="password" id="password" v-model="password" placeholder="비밀번호를 입력하세요" />
      </div>

      <!--로그인 실패 메시지-->
      <p v-if="errorMessages" class="error-messages">{{ errorMessages }}</p>

      <button type="submit" class="login-btn">로그인</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/users.js'
import { useRouter } from 'vue-router'


const userStore = useUserStore()
const router = useRouter()

const username = ref('')
const password = ref('')
const errorMessages = ref('')

const onLogIn = function () {
  const userInfo = {
    username: username.value,
    password: password.value
  }

  errorMessages.value = ''

  userStore.logIn(userInfo)
    .then(() => {
      alert('로그인 성공!')
      router.push({ name: 'landing' })
    })
    .catch(() => {
      errorMessages.value = '❌ 아이디 또는 비밀번호를 확인해주세요.'
    })
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 100px auto;
  padding: 2rem;
  border-radius: 12px;
  background-color: #f2f2f2;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  text-align: left;
}

label {
  margin-bottom: 0.3rem;
  font-weight: bold;
}

input {
  padding: 0.6rem;
  font-size: 1rem;
  border-radius: 6px;
  border: 1px solid #ccc;
}

.login-btn {
  padding: 0.7rem;
  font-size: 1rem;
  font-weight: bold;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.login-btn:hover {
  background-color: #45a049;
}
</style>
