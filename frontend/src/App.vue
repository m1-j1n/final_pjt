<template>
  <header>
    <nav>
      <RouterLink :to="{name: 'signup'}">SingUp</RouterLink> |
      <RouterLink :to="{name: 'login'}">Login</RouterLink>
    </nav>
  </header>

  <!--NavBar-->
  <NavBar />
  <RouterView />
</template>

<script setup>
import NavBar from '@/components/layout/NavBar.vue'
import { RouterLink, RouterView } from 'vue-router'


</script>

<style scoped></style>