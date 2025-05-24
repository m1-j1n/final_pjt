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
import ReadingStateView from '@/views/recommend/ReadingStateView.vue'

const requireAuth = async (to, from, next) => {
  try {
    const res = await axios.get('/accounts/profile/', { withCredentials: true })
    if (res.status === 200) {
      next()
    } else {
      next({ name: 'landing' })
    }
  } catch (err) {
    next({ name: 'landing' })  // 로그인 안 되어 있으면 홈으로
  }
}


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



export default router
