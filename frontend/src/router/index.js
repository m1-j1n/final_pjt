import { createRouter, createWebHistory } from 'vue-router'
import LandingView from '@/views/LandingView.vue'
import ThreadsListView from '@/views/threads/ThreadsListView.vue'
import ThreadsDeatilView from '@/views/threads/ThreadsDeatilView.vue'
import ThreadsWriteView from '@/views/threads/ThreadsWriteView.vue'
import BooksListView from '@/views/book/BooksListView.vue'
import BookDetailView from '@/views/book/BookDetailView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: LandingView,
    },
    {
      path: '/threads',
      name: 'threads',
      component: ThreadsListView,
    },
    {
      path: '/threads/:threadId',
      name: 'threads-detail',
      component: ThreadsDeatilView,
    },
    {
      path: '/threads/:bookId/write',
      name: 'threads-write',
      component: ThreadsWriteView,
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
  ],
})

export default router
