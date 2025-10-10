<script setup>
import { onBeforeMount } from "vue";
import axios from "axios";
import Cookies from "js-cookie";

const students = ref([]);
const studentToAdd = ref({});
const studentToEdit = ref({});

import {conputed, onBeforeMount, ref} from 'vue';
const list =ref([4,2,7,1,2])

function onButtonClick(){
  c.value = a.value + b.value;
}
async function fetchStudents(){
  loading.value=true;
  const r = await axios.get("/api/students");
  console.log(r.data)
  students.value = r.data;
  loading.value=false;
}

async function onRemoveClick(student) {
  await axios.delete(`/api/students/${student.id}/`);
  await fetchStudents(); // переподтягиваю
}

async function onLoadClick(){
  await fetchStudents()
}

async function onStudentAdd(){
  await axios.post("/api/students", {
    ...studentToAdd.value,
  })
  await fetchStudents()
}

onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

</script>

<template>
<div v-for="item in students">
  {{ item.name }}
</div>
<button @click="onLoadClick">Загрузить</button>

<form @submit.prevent.stop="onStudentAdd">
  <div class="row">
    <div class="col">
      <div class="form-floating">
        <!-- ТУТ ПОДКЛЮЧИЛ studentToAdd.name -->
        <input
          type="text"
          class="form-control"
          v-model="studentToAdd.name"
          required
        />
        <label for="floatingInput">Фио</label>
      </div>
    </div>
    <div class="col-auto">
        <!-- А ТУТ ПОДКЛЮЧИЛ К select -->
      <div class="form-floating">
        <select class="form-select" v-model="studentToAdd.group" required>
          <option :value="g.id" v-for="g in groups">{{ g.name }}</option>
        </select>
        <label for="floatingInput">Группа</label>
      </div>
    </div>
    <div class="col-auto">
      <button class="btn btn-primary">
        Добавить
      </button>
    </div>
  </div>
</form>

<div v-for="item in students" class="student-item">
  <div>{{ item.name }}</div>
  <button class="btn btn-danger" @click="onRemoveClick(item)">
    <i class="bi bi-x"></i>
  </button>
</div>

</template>

<style scoped>

</style>
