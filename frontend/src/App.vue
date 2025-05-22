<template>


  <!--NavBar-->
  <NavBar />
  <RouterView />
</template>

<script setup>
import NavBar from '@/components/layout/NavBar.vue'
import { RouterLink, RouterView } from 'vue-router'


</script>

<style scoped></style>