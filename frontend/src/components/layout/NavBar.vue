<template>
  <nav class="navbar navbar-expand-lg bg-white shadow-sm fixed-top py-3">
    <div class="container">
      <!-- 로고 -->
      <RouterLink class="navbar-brand fw-bold text-dark fs-4" :to="{ name: 'landing' }">
        Bookie
      </RouterLink>

      <!-- 모바일 토글 버튼 -->
      <button
        class="navbar-toggler border-0"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
      >
        <i class="bi bi-list fs-2 text-dark"></i>
      </button>

      <!-- 네브바 메뉴 -->
      <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
        <ul class="navbar-nav align-items-center gap-3">
          <li class="nav-item">
            <RouterLink class="nav-link text-dark fw-semibold" :to="{ name: 'books' }">Books</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link text-dark fw-semibold" :to="{ name: 'posts' }">Posts</RouterLink>
          </li>

          <template v-if="!userStore.isLogin">
            <li class="nav-item">
              <RouterLink class="btn btn-sm btn-outline-dark rounded-pill px-3" :to="{ name: 'signup' }">
                Sign Up
              </RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="btn btn-sm btn-dark rounded-pill px-3" :to="{ name: 'login' }">
                Login
              </RouterLink>
            </li>
          </template>

          <template v-else>
            <li class="nav-item">
              <RouterLink class="nav-link text-dark fw-semibold" :to="{ name: 'mypage' }">
                My Page
              </RouterLink>
            </li>
            <li class="nav-item">
              <button class="btn btn-sm btn-outline-secondary rounded-pill px-3" @click="logOut">
                Logout
              </button>
            </li>
          </template>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useRouter, RouterLink } from 'vue-router'
import { useUserStore } from '@/stores/users'

const userStore = useUserStore()
const router = useRouter()

const logOut = () => {
  userStore.logOut()
  router.push({ name: 'landing' })
}
</script>