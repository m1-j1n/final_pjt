import { createRouter, createWebHistory } from 'vue-router'
import LandingView from '@/views/LandingView.vue'
import PostsListView from '@/views/posts/PostsListView.vue'
import PostsDetailView from '@/views/posts/PostsDetailView.vue'
import PostsWriteView from '@/views/posts/PostsWriteView.vue'
import BooksListView from '@/views/book/BooksListView.vue'
import BookDetailView from '@/views/book/BookDetailView.vue'
import SignUpView from '@/views/account/SignUpView.vue'
import LoginView from '@/views/account/LoginView.vue'

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
      component: SignUpView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
  ],
})

export default router
