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

    <!-- ✅ 회원가입 링크 추가 -->
    <div class="signup-link mt-2">
      아직 회원이 아니신가요?
      <RouterLink :to="{ name: 'signup' }">회원가입</RouterLink>
    </div>


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
      router.push({ name: 'landing' })
    })
    .catch(() => {
      errorMessages.value = '❌ 아이디 또는 비밀번호를 확인해주세요.'
    })
}
</script>

<style scoped>
.login-container {
  max-width: 460px;
  margin: 100px auto;
  padding: 2.25rem 2rem;
  border-radius: 1rem;
  background-color: #ffffff;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
  border: 1px solid #e9ecef;
}

h2 {
  font-size: 1.7rem;
  font-weight: 700;
  text-align: center;
  color: #343a40;
  margin-bottom: 2rem;
}

.login-form {
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

input {
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

.error-messages {
  color: #d9534f;
  font-size: 0.85rem;
  text-align: left;
  margin-top: -0.5rem;
  margin-bottom: -0.5rem;
}

.login-btn {
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

.login-btn:hover {
  background-color: #f29b2f;
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
}

.signup-link {
  margin-top: 1rem;
  font-size: 0.95rem;
  color: #6c757d;
  text-align: center;
}

.signup-link a {
  color: #f8a33b;
  text-decoration: none;
  font-weight: 600;
  margin-left: 0.25rem;
}

.signup-link a:hover {
  text-decoration: underline;
}

</style>
