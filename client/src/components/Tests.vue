<script setup>
import { onBeforeMount, ref } from 'vue';
import axios from "axios";
import Cookies from "js-cookie";
import * as bootstrap from 'bootstrap';
const tests = ref([]);
const testToAdd = ref({ name: '' });
const testToEdit = ref({});
const loading = ref(false);
const activeTest = ref(null);
const testQuestions = ref([]);
const questionsLoading = ref(false);

async function fetchTests(){
  loading.value = true;
    const r = await axios.get("/api/tests");
    tests.value = r.data;
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
async function openTestModal(test) {
  activeTest.value = test;
  questionsLoading.value = true;

  const r = await axios.get(`/api/test-questions/?test=${test.id}`);
  testQuestions.value = r.data;

  questionsLoading.value = false;

  const modalEl = document.getElementById('testRunModal');
  new bootstrap.Modal(modalEl).show();
}
async function onUpdateTest() {
  await axios.put(`/api/tests/${testToEdit.value.id}/`, testToEdit.value);
  await fetchTests();
}
function goToTestQuestions(testId) {
  window.location.href = `/test-questions`;
}
onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
  await fetchTests();
})
</script>

<template>
  <div class="container mt-4">
    <h2>Тесты</h2>
    


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
        <button class="btn btn-secondary btn-sm ms-1" @click="goToTestQuestions(item.id)">Вопросы</button>
        <button class="btn btn-danger btn-sm ms-1" @click="onRemoveClick(item)">Удалить</button>
        <button class="btn btn-success btn-sm ms-1" @click="openTestModal(item)">Пройти тест</button>
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

 <div class="modal fade" id="testRunModal" tabindex="-1">
  <div class="modal-dialog modal-lg">
    <div class="modal-content">

      <div class="modal-header">
        <h5 class="modal-title">
          {{ activeTest?.name }}
        </h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>

      <div class="modal-body">
        <div v-if="questionsLoading">
          Загрузка вопросов...
        </div>

        <div v-else-if="!testQuestions.length">
          В тесте нет вопросов
        </div>

        <div v-else class="d-flex flex-column gap-3">
          <div
            v-for="(q, index) in testQuestions"
            :key="q.id"
            class="border rounded p-2"
          >
            <div class="fw-bold mb-2">
              {{ index + 1 }}. {{ q.question }}
            </div>

            <div v-if="q.variants" class="d-flex flex-column gap-1">
              <div
                v-for="(v, i) in q.variants.split(',')"
                :key="i"
                class="form-check"
              >
                <input
                  class="form-check-input"
                  type="radio"
                  :name="'question_' + q.id"
                  :id="'q_' + q.id + '_' + i"
                >
                <label
                  class="form-check-label"
                  :for="'q_' + q.id + '_' + i"
                >
                  {{ v.trim() }}
                </label>
              </div>
            </div>

          </div>
        </div>
      </div>

      <div class="modal-footer">
        <button class="btn btn-secondary" data-bs-dismiss="modal">
          Закрыть
        </button>
        <button class="btn btn-primary">
          Завершить тест
        </button>
      </div>

    </div>
  </div>
</div>

</template>