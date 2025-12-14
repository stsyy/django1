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

  <form @submit.stop.prevent="onLoginFormSubmit" class = "form d-flex flex-column p-3" 
  style="gap: 8px">
    <input placeholder="логин" class="form-control" type="text" v-model="username">
    <input placeholder="пароль" class="form-control" type="password"v-model="password">
    <button class="btn btn-info">войти</button>
  </form>
  
</template>


<style>

</style>