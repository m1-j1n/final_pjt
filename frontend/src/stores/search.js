import axios from 'axios'
import { useUserStore } from '@/stores/users'

const BASE_API_URL = 'http://localhost:8000'

export const searchBooks = async (query) => {
  const userStore = useUserStore()

  try {
    const response = await axios({
      method: 'GET',
      url: `${BASE_API_URL}/api/v1/books/search/`,
      params: { query },
    })

    return response.data
  } catch (err) {
    console.error('🔍 검색 실패:', err)
    return []
  }
}