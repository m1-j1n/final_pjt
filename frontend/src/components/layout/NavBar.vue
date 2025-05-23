<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <RouterLink class="navbar-brand" :to="{ name: 'landing' }">Main</RouterLink>

      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <RouterLink class="nav-link active" :to="{ name: 'books' }">Book</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link active" :to="{ name: 'posts' }">Post</RouterLink>
          </li>
        </ul>

        <!-- 🔒 로그인 상태에 따라 버튼 달라짐 -->
        <div class="d-flex align-items-center gap-2">
          <template v-if="!userStore.isLogin">
            <RouterLink class="btn btn-outline-primary" :to="{ name: 'signup' }">SignUp</RouterLink>
            <RouterLink class="btn btn-outline-success" :to="{ name: 'login' }">Login</RouterLink>
          </template>
          <template v-else>
            <RouterLink class="btn btn-outline-info" :to="{ name: 'mypage' }">My Page</RouterLink>
            <button class="btn btn-outline-danger" @click="logOut">Logout</button>
          </template>
        </div>

      </div>
    </div>
  </nav>
</template>

<script setup>
import { RouterLink, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/users'

const userStore = useUserStore()
const router = useRouter()

const logOut = () => {
  userStore.logOut() // 로그아웃 처리: 토큰 삭제 등
  router.push({ name: 'landing' }) // 메인으로 이동
}
</script>

<style scoped></style>
