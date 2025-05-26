// stores/users.js
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useUserStore = defineStore('user', () => {
  // ✅ API 경로 분리
  const ACCOUNT_API_URL = 'http://127.0.0.1:8000/api/v1/accounts'
  const AUTH_API_URL = 'http://127.0.0.1:8000/api/v1/auth'

  const token = ref(localStorage.getItem('token') || '')
  const username = ref(localStorage.getItem('username') || '')
  const currName = ref(localStorage.getItem('name') ||'')

  // 앱 시작 시 토큰 있으면 axios 헤더 세팅
  if (token.value) {
    axios.defaults.headers.common.Authorization = `Token ${token.value}`
  }

  // ✅ 회원가입 (가입만 하고 로그인은 별도 처리)
  const signUp = async (userInfo) => {
    const res = await axios.post(`${ACCOUNT_API_URL}/signup/`, userInfo)
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
      currName.value = res.data.name
      localStorage.setItem('username', res.data.username)
    } catch (err) {
      console.error('❌ 사용자 정보 불러오기 실패:', err)
    }
  }

  // ✅ 로그인
  const logIn = async ({ username, password }) => {
    const res = await axios.post(`${AUTH_API_URL}/login/`, { username, password })
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

  return { signUp, logIn, logOut, isLogin, token, username, currName }
}, {
  persist: true
})
