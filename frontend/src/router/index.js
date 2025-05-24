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

const routes = [
  {
    path: '/',
    name: 'landing',
    component: LandingView
  },
  {
    path: '/posts',
    name: 'posts',
    component: PostsListView
  },
  {
    path: '/posts/:postId',
    name: 'posts-detail',
    component: PostsDetailView
  },
  {
    path: '/posts/:bookId/write',
    name: 'posts-write',
    component: PostsWriteView,
    meta: { requiresAuth: true }
  },
  {
    path: '/books/:bookId/posts/:postId/update',
    name: 'post-update',
    component: PostUpdateView,
    meta: { requiresAuth: true }
  },
  {
    path: '/books',
    name: 'books',
    component: BooksListView
  },
  {
    path: '/books/:bookId',
    name: 'books-detail',
    component: BookDetailView
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignUpView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/mypage',
    name: 'mypage',
    component: MyPageView,
    meta: { requiresAuth: true }
  },
  {
    path: '/onboarding',
    name: 'onboarding-survey',
    component: OnboardingSurveyView
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
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
      path: '/recommend/reading',
      name: 'recommend-reading',
      component: ReadingStateView,
    },
  ],
})

// 전역 가드: meta.requiresAuth 체크
router.beforeEach((to, from, next) => {
  const requiresAuth = to.meta.requiresAuth === true
  const isAuth = !!axios.defaults.headers.common.Authorization

  if (requiresAuth && !isAuth) {
    return next({ name: 'login' })
  }
  next()
})

export default router
