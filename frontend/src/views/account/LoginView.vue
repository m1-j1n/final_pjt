<!-- views/LoginView.vue -->

<template>
  <div>
    <form @submit.prevent="onLogIn">
      <label for="username">username: </label>
      <input type="text" id="username" v-model="username">

      <label for="password">password: </label>
      <input type="password" id="password" v-model="password">

      <input type="submit" value="login">
    </form>  
  </div>
</template>

<script setup>
  import { ref } from 'vue'
  import { useUserStore } from '@/stores/users.js'
  import { useRouter } from 'vue-router'

  const userStore = useUserStore()
  const router = useRouter()

  const username = ref('')
  const password = ref('')
  
  const onLogIn = function () {
    const userInfo = {
      username: username.value,
      password: password.value
    }
    userStore.logIn(userInfo)
     .then(() => {
      router.push({ name: 'landing' }) 
    })
  }
</script>

<style>

</style>
