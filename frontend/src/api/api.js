const BASE_URL = import.meta.env.VITE_API_URL

export const API = {
  BOOK: {
    LIST: `${BASE_URL}/api/v1/books/`,
    DETAIL: (bookId) => `${BASE_URL}/api/v1/books/${bookId}/`,
    SEARCH: `${BASE_URL}/api/v1/books/search/`,
    TOGGLE_LIKE: (bookId) => `${BASE_URL}/api/v1/books/${bookId}/like/`,
    CATEGORY: (categoryId, page) => `${BASE_URL}/books/category/${categoryId}/?page=${page}`,
    BY_PAGE: (page) => `${BASE_URL}/books/?page=${page}`,
    RANDOM: (count = 3) => `${BASE_URL}/books/random/?count=${count}`,
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
    RECOMMEND: `${BASE_URL}/post/recommend/`,
  },

  AUTH: {
    LOGIN: `${BASE_URL}/api/v1/auth/login/`,
    LOGOUT: `${BASE_URL}/api/v1/auth/logout/`, // 추후 로그아웃 API가 생길 경우
  },

  ACCOUNT: {
    SIGNUP: `${BASE_URL}/api/v1/accounts/signup/`,
    PROFILE: `${BASE_URL}/api/v1/accounts/profile/`,
    LIFESTYLES: `${BASE_URL}/api/v1/accounts/lifestyles/`,
    READING_STYLES: `${BASE_URL}/api/v1/accounts/readingstyles/`,
    AVOIDED_KEYWORDS: `${BASE_URL}/api/v1/accounts/avoided-keywords/`,
    PREFERENCE: `${BASE_URL}/api/v1/accounts/preference/`,
    PROFILE_BY_ID: (userId) => `${BASE_URL}/api/v1/accounts/${userId}/profile/`,
    FOLLOW: (userId) => `${BASE_URL}/api/v1/accounts/${userId}/follow/`,
    FOLLOW_STATUS: (userId) => `${BASE_URL}/api/v1/accounts/${userId}/follow-status/`,
    VERIFY_PASSWORD: `${BASE_URL}/api/v1/accounts/verify-password/`,
  },

  READING: {
    STATUS: (bookId) => `${BASE_URL}/api/v1/books/${bookId}/reading-status/`,
    CREATE: (bookId) => `${BASE_URL}/api/v1/books/${bookId}/reading-status/`,
  },

  COMMENT: {
  LIST: (postId) => `${BASE_URL}/api/v1/posts/${postId}/comments/`,
  CREATE: (postId) => `${BASE_URL}/api/v1/posts/${postId}/comments/create/`,
  DELETE: (commentId) => `${BASE_URL}/api/v1/comments/${commentId}/delete/`,
  },

  RECOMMEND: {
    BASIC: `${BASE_URL}/recommend/basic/`,
    CONTENT_BASED: `${BASE_URL}/api/v1/recommend/content-based/`,
    DROPPED_BOOKS: `${BASE_URL}/api/v1/recommend/dropped-books/`,
    PERSONAL: `${BASE_URL}/api/v1/recommend/personal/`,
  },

  getMediaUrl: (path) => {
    if (!path) return ''
    if (path.startsWith('http')) return path
    return `https://bookchat.kr/media/${path.replace(/^\/?media\//, '')}`
  },
}