<template>
  <div class="app-wrapper">
    <header>
      <NavBar />
    </header>
    <main class="pt-5">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import NavBar from '@/components/layout/NavBar.vue'
import { RouterLink, RouterView } from 'vue-router'


</script>

<style scoped>
.app-wrapper {
  padding-top: 72px;
}
</style>