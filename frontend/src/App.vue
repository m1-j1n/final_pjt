<template>
  <div class="app-wrapper">
    <header>
      <NavBar />
    </header>
    <main class="pt-5">
      <RouterView />
    </main>
    <footer>
    <Footer/>
  </footer>
  </div>
</template>

<script setup>
import NavBar from '@/components/layout/NavBar.vue'
import { RouterLink, RouterView } from 'vue-router'
import Footer from '@/components/layout/Footer.vue'


</script>

<style scoped>
.app-wrapper {
  padding-top: 72px;
}
</style>