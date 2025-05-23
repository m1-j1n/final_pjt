<template>
  <div class="form-container">
    <h2>회원가입</h2>
    <form @submit.prevent="onSignUp">
      <div class="form-group">
        <label for="username">아이디</label>
        <input type="text" id="username" v-model="username" />
      </div>

      <div class="form-group">
        <label for="name">이름</label>
        <input type="text" id="name" v-model="name" />
      </div>

      <div class="form-group">
        <label for="password1">비밀번호</label>
        <input type="password" id="password1" v-model="password1" />
      </div>

      <div class="form-group">
        <label for="password2">비밀번호 확인</label>
        <input type="password" id="password2" v-model="password2" />
      </div>

      <div class="form-group">
        <label for="gender">성별</label>
        <select id="gender" v-model="gender">
          <option value="M">남성</option>
          <option value="F">여성</option>
        </select>
      </div>

      <div class="form-group">
        <label for="age">나이</label>
        <input type="number" id="age" v-model="age" />
      </div>

      <div class="form-group">
        <label for="weekly">주간 평균 독서 시간 (시간)</label>
        <input type="number" id="weekly" v-model="weekly_avg_reading_time" />
      </div>

      <div class="form-group">
        <label for="annual">연간 독서량 (권)</label>
        <input type="number" id="annual" v-model="annual_reading_amount" />
      </div>

      <div class="form-group">
        <label>관심 장르</label>
        <select multiple v-model="interested_genres">
          <option
            v-for="category in categories"
            :key="category.id"
            :value="category.id"
          >
            {{ category.name }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <input type="submit" value="회원가입" />
      </div>
    </form>
  </div>
</template>


<script setup>
import { onMounted, ref } from "vue";
import { useUserStore } from '@/stores/users.js'
import axios from "axios";

const userStore = useUserStore()

const username = ref('')
const name = ref('')
const password1 = ref('')
const password2 = ref('')
const gender = ref('')
const age = ref(null)
const weekly_avg_reading_time = ref(null)
const annual_reading_amount = ref(null)
const interested_genres = ref([])

const categories = ref([])
const BOOK_API_URL = 'http://127.0.0.1:8000/api/v1'

const onSignUp = function () {
   console.log("✅ 선택된 관심 장르 (원본):", interested_genres.value)       
  console.log("✅ 필터링 후 장르:", (interested_genres.value || []).filter(Boolean))  
  const userInfo = {
    username: username.value,
    name: name.value,
    password1: password1.value,
    password2: password2.value,
    gender: gender.value,
    age: age.value,
    weekly_avg_reading_time: weekly_avg_reading_time.value,
    annual_reading_amount: annual_reading_amount.value,
    interested_genres: (interested_genres.value || []).filter(Boolean),
  }
  userStore.signUp(userInfo)  
}

onMounted(() => {
  axios.get(`${BOOK_API_URL}/categories/`)
  .then(res => {
    categories.value = res.data
    console.log("📚 카테고리 목록 도착:", categories.value) 
  })
  .catch(err => {
      console.log("❌ 카테고리 로드 실패:", err)
    })
  
})
  


</script>

<style scoped>
.form-container {
  max-width: 500px;
  margin: 0 auto;
  padding: 2rem;
  border-radius: 12px;
  background-color: #f7f7f7;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1.2rem;
  display: flex;
  flex-direction: column;
}

label {
  font-weight: bold;
  margin-bottom: 0.4rem;
}

input,
select {
  padding: 0.5rem;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 1rem;
}

input[type="submit"] {
  background-color: #4caf50;
  color: white;
  font-weight: bold;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

input[type="submit"]:hover {
  background-color: #45a049;
}
</style>
