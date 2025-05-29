<template>
  <form @submit.prevent="login">
    <input v-model="username" placeholder="Логин" required />
    <input v-model="password" type="password" placeholder="Пароль" required />
    <button type="submit">Войти</button>
    <p v-if="error" style="color:red">{{ error }}</p>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import api, { setAuthToken } from '../api'
import { useRouter } from 'vue-router'

const router = useRouter()

const username = ref('')
const password = ref('')
const error = ref('')

const login = async () => {
  try {
    const res = await api.post('user/login/', {
      username: username.value,
      password: password.value
    })

    const token = res.data.access
    setAuthToken(token)
    localStorage.setItem('token', token)
    error.value = ''

    router.push('/')
  } catch (e) {
    error.value = 'Неверный логин или пароль'
  }
}
</script>
