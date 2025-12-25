<script  setup>
import axios from 'axios';
import {onBeforeMount, ref} from 'vue';

const students = ref([])

async function fetchStudents() {
    students.value = (await axios.get("/api/students/")).data;
}

async function onCreateStudentClick() {
    await axios.post("/api/students/create-custom/")
    await fetchStudents();
}

onBeforeMount(fetchStudents)

</script>

<template>
    Страница 1
    <button @click="onCreateStudentClick">Создать студента</button>

    <div v-for="s in students">
    {{ s.id }}
    </div>
</template>

<style></style>