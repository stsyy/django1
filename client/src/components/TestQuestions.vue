<script setup>
import { onBeforeMount, ref } from 'vue';
import axios from "axios";
import Cookies from "js-cookie";
import * as bootstrap from 'bootstrap'
const questions = ref([]);
const tests = ref([]);
const questionToAdd = ref({
  test: null,
  question: '',
  correct_answer: '',
  wrong_answers: ['', '', '']
})
const questionToEdit = ref({
  id: null,
  test: null,
  question: '',
  correct_answer: '',
  wrong_answers: ['', '', '']
})
const questionPictureRef = ref();
const questionAddImageUrl = ref();
const loading = ref(false);

const questionEditPictureRef = ref(); 
const questionEditImageUrl = ref(); 
const selectedImageUrl = ref(null); 


const stats = ref({});

async function fetchTests(){
  const r = await axios.get("/api/tests");
  tests.value = r.data;
}

async function fetchQuestions(testId = null) {
  loading.value = true;
  let url = "/api/test-questions/";
  if (testId) url += `?test=${testId}`;
  const r = await axios.get(url);
  questions.value = r.data;
  loading.value = false;
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
  const formData = new FormData()
  const file = questionPictureRef.value?.files?.[0]

  if (file) formData.append('picture', file)

  formData.append('test', Number(questionToAdd.value.test))
  formData.append('question', questionToAdd.value.question)

  const qRes = await axios.post('/api/test-questions/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })

  const questionId = qRes.data.id
  const variants = []


  if (questionToAdd.value.correct_answer && questionToAdd.value.correct_answer.trim()) {
    variants.push({
      test_question: questionId,
      text: questionToAdd.value.correct_answer,
      is_correct: true
    })
  }


  for (let i = 0; i < 3; i++) {
    const wrong = questionToAdd.value.wrong_answers[i]
    if (wrong && wrong.trim()) {
      variants.push({
        test_question: questionId,
        text: wrong,
        is_correct: false
      })
    }
  }


  for (let i = 0; i < variants.length; i++) {
    await axios.post('/api/test-question-variants/', variants[i])
  }

  questionToAdd.value = {
    test: null,
    question: '',
    correct_answer: '',
    wrong_answers: ['', '', '']
  }

  questionPictureRef.value.value = ''
  questionAddImageUrl.value = null

  await fetchQuestions()
}


async function onQuestionEditClick(q) {
  let correct = ''
  let wrongs = []

  if (q.variants && q.variants.length) {
    for (const v of q.variants) {
      if (v.is_correct) {
        correct = v.text
      } else {
        wrongs.push(v.text)
      }
    }
  }

  while (wrongs.length < 3) {
    wrongs.push('')
  }

  if (wrongs.length > 3) {
    wrongs = wrongs.slice(0, 3)
  }

  questionToEdit.value = {
    id: q.id,
    test: q.test,
    question: q.question,
    correct_answer: correct,
    wrong_answers: wrongs
  }
}
function editQuestion(item) {
    onQuestionEditClick(item);
    const modalEl = document.getElementById('editQuestionModal');
    if (modalEl && typeof bootstrap !== 'undefined') {
        const modal = new bootstrap.Modal(modalEl);
        modal.show();
    }
}

async function onUpdateQuestion() {
  const formData = new FormData();

  formData.append('test', questionToEdit.value.test);
  formData.append('question', questionToEdit.value.question);

  await axios.patch(
    `/api/test-questions/${questionToEdit.value.id}/`,
    formData,
    { headers: { 'Content-Type': 'multipart/form-data' } }
  );

  const original = questions.value.find(q => q.id === questionToEdit.value.id);
  if (original?.variants?.length) {
    for (const v of original.variants) {
      await axios.delete(`/api/test-question-variants/${v.id}/`);
    }
  }

  const newVariants = [];

  if (questionToEdit.value.correct_answer.trim()) {
    newVariants.push({
      test_question: questionToEdit.value.id,
      text: questionToEdit.value.correct_answer,
      is_correct: true
    });
  }

  for (const w of questionToEdit.value.wrong_answers) {
    if (w && w.trim()) {
      newVariants.push({
        test_question: questionToEdit.value.id,
        text: w,
        is_correct: false
      });
    }
  }

  for (const v of newVariants) {
    await axios.post('/api/test-question-variants/', v);
  }

  const modalEl = document.getElementById('editQuestionModal');
  bootstrap.Modal.getInstance(modalEl)?.hide();

  await fetchQuestions();
}

function onImageClick(url) {
    selectedImageUrl.value = url;
    const modalElement = document.getElementById('imageModal');
    if (modalElement && typeof bootstrap !== 'undefined') {
        new bootstrap.Modal(modalElement).show();
    }
}
function openEditModal() {
    const modalEl = document.getElementById('editQuestionModal');
    if (modalEl && typeof bootstrap !== 'undefined') {
        const modal = new bootstrap.Modal(modalEl);
        modal.show();
    }
}

async function fetchStats() {
  //await userStore.fetchUserInfo();
  const response = await axios.get('/api/test-question-variants/stats/', {
    withCredentials: true
  });
  
  stats.value = response.data;
}

onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
  await fetchTests();
  await fetchQuestions();
  await fetchStats();
})
</script>

<template>
  <div>
      <button 
        @click="fetchStats" 
       
        class="btn btn-primary mb-3"
      >
        Показать статистику
      </button>
      <div v-if="stats">
        <h3>Статистика:</h3>
        <p>Количество вопросов: {{ stats.count }}</p>
      </div>
    </div>
  <div class="container mt-4">
    <h2>Вопросы тестов</h2>
    <div class="mb-4">
      <div class="form-floating">
        <select class="form-select" v-model="selectedTest" @change="fetchQuestions(selectedTest)">
          <option value="">Все тесты</option>
          <option v-for="test in tests" :value="test.id" :key="test.id">{{ test.name }}</option>
        </select>
        <label>Фильтр по тесту</label>
      </div>
    </div>
    <form @submit.prevent="onQuestionAdd" class="mb-4">
      <div class="row g-2">
        <div class="col-12">
          <div class="form-floating mb-3">
            <select class="form-select" v-model="questionToAdd.test" required>
              <option value="" disabled>Выберите тест</option>
              <option v-for="test in tests" :value="test.id" :key="test.id">{{ test.name }}</option>
            </select>
            <label>Тест</label>
          </div>
        </div>
        <div class="col-12">
          <div class="form-floating">
            <input type="text" class="form-control" v-model="questionToAdd.question" placeholder="Вопрос" required />
            <label>Вопрос</label>
          </div>
        </div>
        <div class="col-12">
          <div class="form-floating">
            <input class="form-control" v-model="questionToAdd.correct_answer" placeholder="Правильный ответ" required />
            <label>Правильный ответ</label>
          </div>
        </div>
        <div class="col-12" v-for="(ans, i) in questionToAdd.wrong_answers" :key="i">
          <div class="form-floating">
            <input class="form-control" v-model="questionToAdd.wrong_answers[i]" :placeholder="`Неправильный ответ ${i + 1}`" />
            <label>Неправильный ответ {{ i + 1 }}</label>
          </div>
        </div>
        <div class="col-12">
          <label class="form-label">Изображение для вопроса (опционально)</label>
          <input type="file" class="form-control" ref="questionPictureRef" accept="image/*" @change="questionAddPictureChange" />
        </div>
        <div v-if="questionAddImageUrl" class="col-12">
          <img :src="questionAddImageUrl" style="max-height: 100px;" alt="Превью изображения вопроса" class="mt-2" />
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
          <p><strong>Правильный ответ:</strong> {{ item.variants.find(v => v.is_correct)?.text }}</p>
          <p><strong>Варианты:</strong>
            <span v-for="(v, i) in item.variants || []" :key="v.id">
              {{ v.text }}<span v-if="!v.is_correct"> (неправильный)</span><span v-if="i < item.variants.length - 1">, </span>
            </span>
          </p>
          <div v-if="item.picture" class="mt-2">
            <img :src="item.picture" style="max-height: 100px; cursor: pointer;" alt="Изображение вопроса" @click="onImageClick(item.picture)" />
          </div>
          <small class="text-muted">Тест: {{ item.test_name }}</small>
        </div>
        <div>
          <button class="btn btn-success btn-sm" @click="editQuestion(item)">
              <i class="bi bi-pen-fill">Редактировать</i>
          </button>
          <button class="btn btn-danger btn-sm ms-1" @click="onRemoveClick(item)">
            <i class="bi bi-x">Удалить</i>
          </button>
        </div>
      </div>
    </div>
  </div>

  <div class="modal fade" id="editQuestionModal" tabindex="-1">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Редактировать вопрос</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body">
        <div class="mb-3">
          <label class="form-label">Вопрос</label>
          <input type="text" class="form-control" v-model="questionToEdit.question" />
        </div>
        <div class="mb-3">
          <label class="form-label">Правильный ответ</label>
          <input type="text" class="form-control" v-model="questionToEdit.correct_answer" />
        </div>
        <div v-for="(ans, i) in questionToEdit.wrong_answers" :key="i" class="mb-3">
          <label class="form-label">Неправильный ответ {{ i+1 }}</label>
          <input type="text" class="form-control" v-model="questionToEdit.wrong_answers[i]" />
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
        <button type="button" class="btn btn-primary" @click="onUpdateQuestion">Сохранить</button>
      </div>
    </div>
  </div>
</div>
</template>
