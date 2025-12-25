<script setup>
import { onBeforeMount, ref } from 'vue';
import axios from "axios";
import Cookies from "js-cookie";
import { useUserInfoStore } from '@/stores/user_store';
import { storeToRefs } from 'pinia';


const userInfoStore = useUserInfoStore();
const{
  username,
}=storeToRefs(userInfoStore)

const results = ref([]);
const students = ref([]);
const tests = ref([]);
const resultToAdd = ref({});
const resultToEdit = ref({});
const loading = ref(false);

async function fetchStudents(){
  const r = await axios.get("/api/students");
  students.value = r.data;
}

async function fetchTests(){
  const r = await axios.get("/api/tests");
  tests.value = r.data;
}

async function fetchResults(){
  loading.value = true;
    const r = await axios.get("/api/results");
    results.value = r.data;

}

async function onRemoveClick(result) {
  if (confirm('Удалить результат?')) {
    await axios.delete(`/api/results/${result.id}/`);
    await fetchResults();
  }
}

async function onResultAdd(){
  await axios.post("/api/results/", resultToAdd.value);
  resultToAdd.value = {};
  await fetchResults();
}

async function onResultEditClick(result) {
  resultToEdit.value = { ...result };
}

async function onUpdateResult() {
  await axios.put(`/api/results/${resultToEdit.value.id}/`, resultToEdit.value);
  await fetchResults();
}

onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
  await fetchStudents();
  await fetchTests();
  await fetchResults();
})
</script>

<template>
  {{ username }}
  <div class="container mt-4">
    <h2>Результаты тестов</h2>
    
    <form @submit.prevent="onResultAdd" class="mb-4">
      <div class="row g-2">
        <div class="col-md-4">
          <div class="form-floating">
            <select class="form-select" v-model="resultToAdd.student" required>
              <option value="">Выберите студента</option>
              <option v-for="student in students" :value="student.id">{{ student.name }}</option>
            </select>
            <label>Студент</label>
          </div>
        </div>
        <div class="col-md-4">
          <div class="form-floating">
            <select class="form-select" v-model="resultToAdd.test" required>
              <option value="">Выберите тест</option>
              <option v-for="test in tests" :value="test.id">{{ test.name }}</option>
            </select>
            <label>Тест</label>
          </div>
        </div>
        <div class="col-md-2">
          <div class="form-floating">
            <input
              type="number"
              class="form-control"
              v-model="resultToAdd.score"
              placeholder="Баллы"
              required
            />
            <label>Баллы</label>
          </div>
        </div>
        <div class="col-md-2">
          <button class="btn btn-primary h-100">Добавить</button>
        </div>
      </div>
    </form>

  
    <div v-for="item in results" :key="item.id" class="result-item border p-3 mb-2">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <strong>{{ item.student_name }}</strong> - {{ item.test_name }}
          <br>
          <small>Баллы: {{ item.score }} | Дата: {{ new Date(item.date).toLocaleDateString() }}</small>
        </div>
        <div>
          <button
            class="btn btn-success btn-sm"
            @click="onResultEditClick(item)"
            data-bs-toggle="modal"
            data-bs-target="#editResultModal"
          >
            <i class="bi bi-pen-fill"></i>
          </button>
          <button class="btn btn-danger btn-sm ms-1" @click="onRemoveClick(item)">
            <i class="bi bi-x"></i>
          </button>
        </div>
      </div>
    </div>

    <div class="modal fade" id="editResultModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Редактировать результат</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="row g-3">
              <div class="col-12">
                <div class="form-floating">
                  <select class="form-select" v-model="resultToEdit.student">
                    <option v-for="student in students" :value="student.id">{{ student.name }}</option>
                  </select>
                  <label>Студент</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating">
                  <select class="form-select" v-model="resultToEdit.test">
                    <option v-for="test in tests" :value="test.id">{{ test.name }}</option>
                  </select>
                  <label>Тест</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating">
                  <input type="number" class="form-control" v-model="resultToEdit.score" />
                  <label>Баллы</label>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdateResult">
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>