async function onLoadClick(){
  axios.get("/api/students")
}

<script setup>
import {ref} from 'vue';
const a = ref(13);
const b = ref(23);
const c = ref(0);

function onButtonClick(){
  c.value = a.value + b.value;
}

</script>

<template>
<div>
  <input type="number" v-model="a"><br>
  <input type="number" v-model="b"><br>
<b>{{a}}+{{b}}</b><span>={{c}}</span>

<button @click="onButtonClick">Кнопка</button>
</div>

</template>

<style scoped>

</style>
