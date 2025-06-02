import axios from 'axios'
import { API } from '@/api/api'

export const searchBooks = async (query) => {
  try {
    const response = await axios({
      method: 'GET',
      url: API.BOOK.SEARCH,
      params: { query },
    })

    return response.data
  } catch (err) {
    console.error('🔍 검색 실패:', err)
    return []
  }
}