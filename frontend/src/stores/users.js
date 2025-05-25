// stores/users.js
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useUserStore = defineStore('user', () => {
  const ACCOUNT_API_URL = 'http://127.0.0.1:8000/accounts'
  // persisted 상태에서 불러오거나, 없으면 빈 문자열
  const token = ref(localStorage.getItem('token') || '')
  const username = ref(localStorage.getItem('username') || '')

  // 앱 시작 시 토큰이 있으면 axios 기본 헤더에 세팅
  if (token.value) {
    axios.defaults.headers.common.Authorization = `Token ${token.value}`
  }

  // 회원가입 (가입 후 자동 로그인)
  const signUp = async (userInfo) => {
    const res = await axios.post(`${ACCOUNT_API_URL}/signup/`, userInfo)
    const newKey = res.data.key
    token.value = newKey
    localStorage.setItem('token', newKey)
    axios.defaults.headers.common.Authorization = `Token ${newKey}`
    console.log('회원가입 및 자동 로그인 완료')
    return res
  }
  
    // username 따로 저장
    // 로그인 이후 사용자 정보 가져오기
    const fetchUserProfile = async () => {
      try {
        const res = await axios.get(`${ACCOUNT_API_URL}/profile/`, {
          headers: {
            Authorization: `Token ${token.value}`,
          }
        })
        username.value = res.data.username
        localStorage.setItem('username', res.data.username)
      } catch (err) {
        console.error('❌ 사용자 정보 불러오기 실패:', err)
      }
    }

  // 로그인
  const logIn = async ({ username, password }) => {
    const res = await axios.post(`${ACCOUNT_API_URL}/login/`, { username, password })
    const key = res.data.key
    token.value = key
    localStorage.setItem('token', key)
    axios.defaults.headers.common.Authorization = `Token ${key}`
    await fetchUserProfile()
    console.log('로그인 성공')
    return res
  }

  // 로그아웃
  const logOut = () => {
    token.value = ''
    localStorage.removeItem('token')
    delete axios.defaults.headers.common.Authorization
    console.log('로그아웃 완료')
  }

  // 로그인 여부
  const isLogin = computed(() => !!token.value)

  return { signUp, logIn, logOut, isLogin, token, username }
}, {
  persist: true
})
