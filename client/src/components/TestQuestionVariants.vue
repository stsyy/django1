<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'

const variants = ref([])

async function fetchVariants() {
  variants.value = (await axios.get("/api/test-question-variants/")).data
}

onBeforeMount(fetchVariants)
</script>

<template>
  <div>
    <h2>Варианты вопросов</h2>

    <div v-for="v in variants" :key="v.id">
      {{ v.text }}
    </div>
  </div>
</template>
