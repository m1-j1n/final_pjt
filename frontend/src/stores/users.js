// 로그인, 회원정보, 선호 장르 등 회원 정보 관리
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useUserStore = defineStore('user', () => {
  const ACCOUNT_API_URL = 'http://127.0.0.1:8000/accounts'
  const token = ref('')
  const signUp = function (userInfo) {
    axios({
      method: 'POST',
      url: `${ACCOUNT_API_URL}/signup/`,
      data: userInfo
    })
      .then(res => {
        console.log(res.data)
        console.log('회원가입 성공!')
      })
      .catch(err => {
        console.log('회원가입 실패:', err.response?.data || err.message)
      })
  }

  const logIn = function ({ username, password }) {
    return axios({
      method: 'POST',
      url: `${ACCOUNT_API_URL}/login/`,
      data: {
        username, password
      }
    })
      .then(res => {
        console.log(res)
        token.value = res.data.key
        localStorage.setItem('token', res.data.key)
      })
      .catch(err => console.log(err))
  }

  return { signUp, logIn }
}, { persist: true })
