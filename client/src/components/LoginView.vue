<script setup>
import {ref} from 'vue';
import {useUserInfoStore} from '@/stores/user_store';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { storeToRefs } from 'pinia';
import Cookies from 'js-cookie';

const username = ref();
const password = ref();

const userInfoStore = useUserInfoStore();

const {
  is_authenticated
}=storeToRefs(userInfoStore)

const router = useRouter();

async function onLoginFormSubmit() {
  const r = await axios.post("/api/users/login/", {
    username: username.value,
    password: password.value,
  })

  password.value = '';
  username.value = '';

 await userInfoStore.fetchUserInfo();
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
  if (is_authenticated.value) {
    router.push("/")
  }
}


</script>

<template>
 <div class="login-container">
  <h2 class="login-title">Вход в систему</h2>
  <form @submit.stop.prevent="onLoginFormSubmit" class = "login-form" 
  style="gap: 8px">
    <input placeholder="логин" class="form-control" type="text" v-model="username">
    <input placeholder="пароль" class="form-control" type="password"v-model="password">
    <button class="btn btn-info">войти</button>
  </form>
</div>
</template>

<style scoped>
.login-container {
  max-width: 350px;
  margin: 100px auto;
  padding: 20px 30px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
  text-align: center;
  background-color: #fff;
}

.login-container h2 {
  margin-bottom: 20px;
  font-family: Arial, sans-serif;
  color: #333;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.login-form input {
  padding: 10px;
  font-size: 14px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.login-form button {
  padding: 10px;
  font-size: 16px;
  background-color: #0d6efd;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.login-form button:hover {
  background-color: #0b5ed7;
}
</style>