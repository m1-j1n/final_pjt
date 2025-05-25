import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useUserStore } from '@/stores/users'

export const usePostStore = defineStore('post', () => {
  const BASE_API_URL = 'http://localhost:8000/api/v1'
  const posts = ref([])
  const selectedPost = ref(null)

  // 📌 전체 포스트
  const fetchPosts = () => {
    return axios.get(`${BASE_API_URL}/posts/`)
      .then((res) => {
        posts.value = res.data
      })
      .catch((err) => {
        console.error('📛 포스트 목록 불러오기 실패:', err)
      })
  }

  // 📌 책 id로 post 찾기
  const fetchPostsByBook = (bookId) => {
    return axios.get(`${BASE_API_URL}/books/${bookId}/posts/`)
      .then((res) => {
        posts.value = res.data
      })
      .catch((err) => {
        console.error('📛 해당 책의 포스트 불러오기 실패:', err)
      })
  }

  // 📌 포스트 하나
  const fetchPostDetail = (bookId, postId) => {
    return axios.get(`${BASE_API_URL}/books/${bookId}/posts/${postId}/`)
      .then((res) => {
        selectedPost.value = res.data
      })
      .catch((err) => {
        console.error('📛 포스트 상세 불러오기 실패:', err)
      })
  }

  // 📌 포스트 생성
  const createPost = (bookId, payload) => {
    const userStore = useUserStore()
    console.log(userStore.token);


    return axios.post(
      `${BASE_API_URL}/books/${bookId}/posts/create/`,
      payload,
      {
        headers: {
          Authorization: `Token ${userStore.token}`,
        },
      }
    ).catch((err) => {
      console.error('📛 포스트 생성 실패:', err)
      console.log(userStore.token);
      
    })
  }

  // 📌 포스트 수정
  const updatePost = (bookId, postId, payload) => {
    return axios.put(`${BASE_API_URL}/books/${bookId}/posts/${postId}/update/`, payload)
      .then(() => fetchPostDetail(bookId, postId))
      .catch((err) => {
        console.error('📛 포스트 수정 실패:', err)
      })
  }

  // 📌 포스트 삭제
  const deletePost = (bookId, postId) => {
    return axios.delete(`${BASE_API_URL}/books/${bookId}/posts/${postId}/delete/`)
      .then(() => fetchPostsByBook(bookId))
      .catch((err) => {
        console.error('📛 포스트 삭제 실패:', err)
      })
  }


  return {
    posts,
    selectedPost,
    fetchPostDetail,
    fetchPostsByBook,
    createPost,
    updatePost,
    deletePost,
    fetchPosts,
  }
})
