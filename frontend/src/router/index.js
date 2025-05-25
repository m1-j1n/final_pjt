// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import axios from 'axios'

import LandingView from '@/views/LandingView.vue'
import PostsListView from '@/views/posts/PostsListView.vue'
import PostsDetailView from '@/views/posts/PostsDetailView.vue'
import PostsWriteView from '@/views/posts/PostsWriteView.vue'
import PostUpdateView from '@/views/posts/PostUpdateView.vue'
import BooksListView from '@/views/book/BooksListView.vue'
import BookDetailView from '@/views/book/BookDetailView.vue'
import SignUpView from '@/views/account/SignUpView.vue'
import LoginView from '@/views/account/LoginView.vue'
import MyPageView from '@/views/account/MyPageView.vue'
import OnboardingSurveyView from '@/views/account/OnboardingSurveyView.vue'
import ReadingStateView from '@/views/recommend/ReadingStateView.vue'

// 인증이 필요한 라우트용 가드
const requireAuth = async (to, from, next) => {
  try {
    const res = await axios.get('/accounts/profile/', { withCredentials: true })
    if (res.status === 200) {
      next()
    } else {
      next({ name: 'landing' })
    }
  } catch (err) {
    next({ name: 'landing' })
  }
}

const routes = [
  {
    path: '/',
    name: 'landing',
    component: LandingView,
  },
  {
    path: '/posts',
    name: 'posts',
    component: PostsListView,
  },
  {
    path: '/posts/:postId',
    name: 'posts-detail',
    component: PostsDetailView,
  },
  {
    path: '/posts/:bookId/write',
    name: 'posts-write',
    component: PostsWriteView,
    beforeEnter: requireAuth,
  },
  {
    path: '/books/:bookId/posts/:postId/update',
    name: 'post-update',
    component: PostUpdateView,
    beforeEnter: requireAuth,
  },
  {
    path: '/books',
    name: 'books',
    component: BooksListView,
  },
  {
    path: '/books/:bookId',
    name: 'books-detail',
    component: BookDetailView,
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignUpView,
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
  },
  {
    path: '/mypage',
    name: 'mypage',
    component: MyPageView,
    beforeEnter: requireAuth,
  },
  {
    path: '/onboarding',
    name: 'onboarding-survey',
    component: OnboardingSurveyView,
  },
  {
    path: '/recommend/reading',
    name: 'recommend-reading',
    component: ReadingStateView,
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes, // 👈 명시적으로 유지
})

// 전역 가드: meta.requiresAuth 사용 시 처리
router.beforeEach((to, from, next) => {
  const requiresAuth = to.meta.requiresAuth === true
  const isAuth = !!axios.defaults.headers.common.Authorization

  if (requiresAuth && !isAuth) {
    return next({ name: 'login' })
  }
  next()
})

export default router