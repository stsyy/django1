<script setup>
import { onBeforeMount, onMounted, ref } from "vue"; 
import { RouterView, useRouter } from "vue-router"; 
import { useUserInfoStore } from './stores/user_store';
import { storeToRefs } from "pinia";
import axios from 'axios';
import Cookies from "js-cookie";


const router = useRouter();

const userInfoStore = useUserInfoStore();
const {
  is_authenticated,
  can_see_page2,
} = storeToRefs(userInfoStore)

async function onFetchStudents(){
  //let r = await fetch("/api/students.json");
  //let data = await r.json();
  loading.value=true;

  let data = (await axios.get("/api/students.json")).data;
  students.value = data;
  loading.value=false;

  //console.log(r);
}

async function onLogout() {
  const r = await axios.post("/api/users/logout/")
  userInfoStore.fetchUserInfo();
  router.push("/login");
}


</script>

<template>

  <nav class="d-flex" style="padding: 8px; justify-content: space-between;">
   <div class="d-flex" style="gap: 8px">
    <router-link to="/">Главная</router-link>
    <router-link to="/students" v-if="userInfoStore.hasPermission('general.can_see_all_students')">Студенты</router-link>
    <router-link to="/tests" v-if="userInfoStore.hasPermission('general.can_see_test_questions')">Тесты</router-link>
    <router-link to="/test-questions" >Вопросы тестов</router-link>
    <router-link to="/results" v-if="userInfoStore.hasPermission('general.can_see_test_questions_variants')">Результаты</router-link>
    <router-link to="/second-auth">SECOND</router-link>
    <button type="button" class="btn btn-danger" @click="onLogout" v-if="is_authenticated">Выйти</button>
   </div>

    <!--<button class="btn btn-info" @click="onFetchStudents">Показать</button>-->
    
  </nav>
 {{ userInfo }}

 <div>
    <RouterView />
 </div>
  <div>
    <div v-if="loading">Загрузка</div>
    <div v-else v-for="s in students">{{ s.name }}</div>
  </div>
</template> 

<style>
h1 {
  color: rgb(56, 56, 208);
}

.form {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  padding: 8px 0;
}
</style>