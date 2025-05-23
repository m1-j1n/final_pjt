// 로그인, 회원정보, 선호 장르 등 회원 정보 관리
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useUserStore = defineStore('user', () => {
  const ACCOUNT_API_URL = 'http://127.0.0.1:8000/accounts'
  const token = ref('')

  // 회원가입
  const signUp = function (userInfo) {
    return axios({
      method: 'POST',
      url: `${ACCOUNT_API_URL}/signup/`,
      data: userInfo
    })
  }

  // 로그인
  const logIn = function ({ username, password }) {
    return axios({
      method: 'POST',
      url: `${ACCOUNT_API_URL}/login/`,
      data: { username, password }
    })
      .then(res => {
        token.value = res.data.key
        localStorage.setItem('token', res.data.key)
        console.log('로그인 성공')
      })
      .catch(err => console.log('로그인 실패', err))
  }

  // 로그아웃
  const logOut = function () {
    token.value = ''
    localStorage.removeItem('token')
    console.log('로그아웃 완료')
  }

  // 로그인 여부
  const isLogin = computed(() => {
    return token.value !== ''
  })

  return { signUp, logIn, logOut, isLogin }
}, { persist: true })
