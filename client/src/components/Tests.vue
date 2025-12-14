<script setup>
import { onBeforeMount, ref } from 'vue';
import axios from "axios";
import Cookies from "js-cookie";

const tests = ref([]);
const testToAdd = ref({ name: '' });
const testToEdit = ref({});
const loading = ref(false);

async function fetchTests(){
  loading.value = true;
  try {
    const r = await axios.get("/api/tests");
    tests.value = r.data;
  } catch (error) {
    console.error('Ошибка загрузки:', error);
  } finally {
    loading.value = false;
  }
}

async function onRemoveClick(test) {
  if (confirm(`Удалить тест "${test.name}"?`)) {
    await axios.delete(`/api/tests/${test.id}/`);
    await fetchTests();
  }
}

async function onTestAdd(){
  await axios.post("/api/tests/", testToAdd.value);
  testToAdd.value = { name: '' };
  await fetchTests();
}

async function onTestEditClick(test) {
  testToEdit.value = { ...test };
}

async function onUpdateTest() {
  await axios.put(`/api/tests/${testToEdit.value.id}/`, testToEdit.value);
  await fetchTests();
}

onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
  await fetchTests();
})
</script>

<template>
  <div class="container mt-4">
    <h2>Тесты</h2>
    
    <div v-if="loading" class="text-center">Загрузка...</div>

    <form @submit.prevent="onTestAdd" class="mb-4">
      <div class="row">
        <div class="col">
          <div class="form-floating">
            <input
              type="text"
              class="form-control"
              v-model="testToAdd.name"
              placeholder="Название теста"
              required
            />
            <label>Название теста</label>
          </div>
        </div>
        <div class="col-auto">
          <button class="btn btn-primary">Добавить</button>
        </div>
      </div>
    </form>

    <div v-for="item in tests" :key="item.id" class="test-item d-flex justify-content-between align-items-center p-2 border-bottom">
      <div>{{ item.name }}</div>
      <div>
        <button
          class="btn btn-success btn-sm"
          @click="onTestEditClick(item)"
          data-bs-toggle="modal"
          data-bs-target="#editTestModal"
        >
          <i class="bi bi-pen-fill"></i>
        </button>
        <button class="btn btn-danger btn-sm ms-1" @click="onRemoveClick(item)">
          <i class="bi bi-x"></i>
        </button>
      </div>
    </div>

    <div class="modal fade" id="editTestModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Редактировать тест</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="form-floating">
              <input
                type="text"
                class="form-control"
                v-model="testToEdit.name"
                placeholder="Название теста"
              />
              <label>Название теста</label>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdateTest">
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>