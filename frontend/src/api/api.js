const BASE_URL = import.meta.env.VITE_API_URL

export const API = {
  BOOK: {
    LIST: `${BASE_URL}/api/v1/books/`,
    DETAIL: (bookId) => `${BASE_URL}/api/v1/books/${bookId}/`,
    SEARCH: `${BASE_URL}/api/v1/books/search/`,
    TOGGLE_LIKE: (bookId) => `${BASE_URL}/api/v1/books/${bookId}/like/`,
  },

  CATEGORY: {
    LIST: `${BASE_URL}/api/v1/categories/`,
  },

  POST: {
    LIST: `${BASE_URL}/api/v1/posts/`, // 전체 포스트 (optional)
    BY_BOOK: (bookId) => `${BASE_URL}/api/v1/books/${bookId}/posts/`,
    DETAIL: (bookId, postId) => `${BASE_URL}/api/v1/books/${bookId}/posts/${postId}/`,
    CREATE: (bookId) => `${BASE_URL}/api/v1/books/${bookId}/posts/create/`,
    UPDATE: (bookId, postId) => `${BASE_URL}/api/v1/books/${bookId}/posts/${postId}/update/`,
    DELETE: (bookId, postId) => `${BASE_URL}/api/v1/books/${bookId}/posts/${postId}/delete/`,
  },

  AUTH: {
    LOGIN: `${BASE_URL}/api/v1/auth/login/`,
    LOGOUT: `${BASE_URL}/api/v1/auth/logout/`, // 추후 로그아웃 API가 생길 경우
  },

  ACCOUNT: {
    SIGNUP: `${BASE_URL}/api/v1/accounts/signup/`,
    PROFILE: `${BASE_URL}/api/v1/accounts/profile/`,
  },

  READING: {
    STATUS: (bookId) => `${BASE_URL}/api/v1/books/${bookId}/reading-status/`,
    CREATE: (bookId) => `${BASE_URL}/api/v1/books/${bookId}/reading-status/`,
  },
}