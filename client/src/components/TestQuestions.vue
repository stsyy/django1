<script setup>
import { onBeforeMount, ref } from 'vue';
import axios from "axios";
import Cookies from "js-cookie";

const questions = ref([]);
const tests = ref([]);
const questionToAdd = ref({});
const questionToEdit = ref({});
const questionPictureRef = ref();
const questionAddImageUrl = ref();
const loading = ref(false);

const questionEditPictureRef = ref(); 
const questionEditImageUrl = ref(); 
const selectedImageUrl = ref(null); 


async function fetchTests(){
  const r = await axios.get("/api/tests");
  tests.value = r.data;
}

async function fetchQuestions(){
  loading.value = true;
  try {
    const r = await axios.get("/api/test-questions");
    questions.value = r.data;
  } catch (error) {
    console.error('Ошибка загрузки:', error);
  } finally {
    loading.value = false;
  }
}

async function onRemoveClick(question) {
  if (confirm(`Удалить вопрос "${question.question}"?`)) {
    await axios.delete(`/api/test-questions/${question.id}/`);
    await fetchQuestions();
  }
}

function questionAddPictureChange() {
  const file = questionPictureRef.value?.files?.[0];
  if (file) {
    questionAddImageUrl.value = URL.createObjectURL(file);
  }
}

function questionEditPictureChange() {
  const file = questionEditPictureRef.value?.files?.[0];
  if (file) {
    questionEditImageUrl.value = URL.createObjectURL(file);
  } else {
    questionEditImageUrl.value = null;
  }
}

async function onQuestionAdd() {
  const formData = new FormData();
  const file = questionPictureRef.value?.files?.[0];

  if (file) formData.append('picture', file);
  formData.append('test', questionToAdd.value.test || "");
  formData.append('question', questionToAdd.value.question || "");
  formData.append('answer', questionToAdd.value.answer || "");
  formData.append('variants', questionToAdd.value.variants || "");

  await axios.post("/api/test-questions/", formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });

  questionToAdd.value = {};
  questionAddImageUrl.value = null;
  questionPictureRef.value.value = ""; 
  await fetchQuestions();
}

async function onQuestionEditClick(question) {
  questionToEdit.value = { ...question };
  questionEditImageUrl.value = null;
}

async function onUpdateQuestion() {
  const formData = new FormData();
  const file = questionEditPictureRef.value?.files?.[0];

  if (file) {
    formData.append('picture', file);
  }

  formData.append('test', questionToEdit.value.test);
  formData.append('question', questionToEdit.value.question);
  formData.append('answer', questionToEdit.value.answer);
  formData.append('variants', questionToEdit.value.variants);
  
  await axios.patch(`/api/test-questions/${questionToEdit.value.id}/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  
  if (questionEditPictureRef.value) questionEditPictureRef.value.value = "";
  questionEditImageUrl.value = null;

  await fetchQuestions();
}

function onImageClick(url) {
    selectedImageUrl.value = url;
    const modalElement = document.getElementById('imageModal');
    if (modalElement && typeof bootstrap !== 'undefined') {
        new bootstrap.Modal(modalElement).show();
    }
}


onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
  await fetchTests();
  await fetchQuestions();
})
</script>

<template>
  <div class="container mt-4">
    <h2>Вопросы тестов</h2>
    
        <form @submit.prevent="onQuestionAdd" class="mb-4">
      <div class="row g-2">
        <div class="col-12">
          <div class="form-floating">
            <select class="form-select" v-model="questionToAdd.test" required>
              <option value="">Выберите тест</option>
              <option v-for="test in tests" :value="test.id" :key="test.id">{{ test.name }}</option>
            </select>
            <label>Тест</label>
          </div>
        </div>
        <div class="col-12">
          <div class="form-floating">
            <input
              type="text"
              class="form-control"
              v-model="questionToAdd.question"
              placeholder="Вопрос"
              required
            />
            <label>Вопрос</label>
          </div>
        </div>
        <div class="col-12">
          <div class="form-floating">
            <input
              type="text"
              class="form-control"
              v-model="questionToAdd.answer"
              placeholder="Правильный ответ"
              required
            />
            <label>Правильный ответ</label>
          </div>
        </div>
        <div class="col-12">
          <div class="form-floating">
            <textarea
              class="form-control"
              v-model="questionToAdd.variants"
              placeholder="Варианты ответов"
              required
            ></textarea>
            <label>Варианты ответов</label>
          </div>
        </div>
        <div class="col-12">
          <label class="form-label">Изображение для вопроса (опционально)</label>
          <input 
            type="file" 
            class="form-control" 
            ref="questionPictureRef"
            accept="image/*"
            @change="questionAddPictureChange"
          />
        </div>
        <div v-if="questionAddImageUrl" class="col-12">
          <img :src="questionAddImageUrl" style="max-height: 100px;" alt="Превью изображения вопроса" class="mt-2">
        </div>
        <div class="col-12">
          <button class="btn btn-primary">Добавить вопрос</button>
        </div>
      </div>
    </form>
    
        <div v-for="item in questions" :key="item.id" class="question-item border p-3 mb-2">
      <div class="d-flex justify-content-between align-items-start">
        <div>
          <h6>{{ item.question }}</h6>
          <p><strong>Правильный ответ:</strong> {{ item.answer }}</p>
          <p><strong>Варианты:</strong> {{ item.variants }}</p>
          <div v-if="item.picture" class="mt-2">
                        <img 
              :src="item.picture" 
              style="max-height: 100px; cursor: pointer;" 
              alt="Изображение вопроса"
              @click="onImageClick(item.picture)"
            >
          </div>
          <small class="text-muted">Тест: {{ item.test_name }}</small>
        </div>
        <div>
          <button
            class="btn btn-success btn-sm"
            @click="onQuestionEditClick(item)"
            data-bs-toggle="modal"
            data-bs-target="#editQuestionModal"
          >
            <i class="bi bi-pen-fill"></i>
          </button>
          <button class="btn btn-danger btn-sm ms-1" @click="onRemoveClick(item)">
            <i class="bi bi-x"></i>
          </button>
        </div>
      </div>
    </div>

        <div class="modal fade" id="editQuestionModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Редактировать вопрос</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="row g-3">
              
                            <div class="col-12">
                <label class="form-label">Изменить изображение (оставьте пустым, чтобы не менять)</label>
                <input 
                  type="file" 
                  class="form-control" 
                  ref="questionEditPictureRef" 
                  accept="image/*"
                  @change="questionEditPictureChange"
                />
              </div>
              <div v-if="questionEditImageUrl" class="col-12">
                <img :src="questionEditImageUrl" style="max-height: 100px;" alt="Превью нового изображения">
              </div>
              <div v-else-if="questionToEdit.picture" class="col-12">
                <small class="text-muted">Текущее изображение:</small>
                <img :src="questionToEdit.picture" style="max-height: 60px;" alt="Текущее изображение">
              </div>
              
              <div class="col-12">
                <div class="form-floating">
                  <select class="form-select" v-model="questionToEdit.test">
                    <option v-for="test in tests" :value="test.id" :key="test.id">{{ test.name }}</option>
                  </select>
                  <label>Тест</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating">
                  <input type="text" class="form-control" v-model="questionToEdit.question" />
                  <label>Вопрос</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating">
                  <input type="text" class="form-control" v-model="questionToEdit.answer" />
                  <label>Правильный ответ</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating">
                  <textarea class="form-control" v-model="questionToEdit.variants"></textarea>
                  <label>Варианты ответов</label>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdateQuestion">
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>

        <div class="modal fade" id="imageModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Просмотр изображения</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body text-center">
                    <img :src="selectedImageUrl" class="img-fluid" alt="Увеличенное изображение">
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                </div>
            </div>
        </div>
    </div>
  </div>
</template>