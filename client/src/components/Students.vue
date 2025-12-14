<script setup>
import { onBeforeMount, ref } from 'vue';
import axios from "axios";
import Cookies from "js-cookie";
import * as bootstrap from 'bootstrap'; 

const students = ref([]);
const studentToAdd = ref({});
const studentToEdit = ref({});
const studentsPictureRef = ref();
const studentAddImageUrl = ref();
const tests = ref([]);
const loading = ref(false);

const studentEditPictureRef = ref(); 
const studentEditImageUrl = ref(); 
const selectedImageUrl = ref(null); 

async function fetchTests() {
  const r = await axios.get("/api/tests");
  tests.value = r.data;
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
  await fetchStudents();
}

async function onLoadClick(){
  await fetchStudents()
}

function studentEditPictureChange() {
  const file = studentEditPictureRef.value?.files?.[0];
  if (file) {
    studentEditImageUrl.value = URL.createObjectURL(file);
  } else {
    studentEditImageUrl.value = null;
  }
}

function studentsAddPictureChange() {
  const file = studentsPictureRef.value?.files?.[0];
  if (file) {
    studentAddImageUrl.value = URL.createObjectURL(file);
  }
}

async function onStudentAdd() {
  const formData = new FormData();
  const file = studentsPictureRef.value?.files?.[0];

  if (file) formData.append('picture', file);
  formData.append('name', studentToAdd.value.name || "");
  formData.append('login', studentToAdd.value.login || "");
  formData.append('password', studentToAdd.value.password || "");
  formData.append('level', studentToAdd.value.level || "");
  formData.append('progress', studentToAdd.value.progress || 0);

  await axios.post("/api/students/", formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });

  studentToAdd.value = {};
  studentAddImageUrl.value = null;
  studentsPictureRef.value.value = ""; 
  await fetchStudents();
}

async function onStudentEditClick(student) {
  studentToEdit.value = { ...student };
}

async function onUpdateStudent() {
  const formData = new FormData();
  const file = studentEditPictureRef.value?.files?.[0];

  if (file) {
    formData.append('picture', file);
  }

  formData.append('name', studentToEdit.value.name);
  formData.append('login', studentToEdit.value.login);
  formData.append('password', studentToEdit.value.password);
  formData.append('level', studentToEdit.value.level);
  formData.append('progress', studentToEdit.value.progress);

  await axios.patch(`/api/students/${studentToEdit.value.id}/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });

  if (studentEditPictureRef.value) studentEditPictureRef.value.value = "";
  studentEditImageUrl.value = null;

  await fetchStudents();
}

function onImageClick(url) {
    selectedImageUrl.value = url;
    
    setTimeout(() => {
        const modalElement = document.getElementById('imageModal');
        if (modalElement) {
            const modal = new bootstrap.Modal(modalElement);
            modal.show();
        }
    }, 100);
}

onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
  await fetchTests();
  await fetchStudents(); 
})
</script>

<template>
  <div class="container mt-4">
    <h2>Студенты</h2>
    
    <div v-if="loading" class="text-center">Загрузка...</div>

        <div class="mb-3">
      <label class="form-label">Загрузить изображение студента</label>
      <input 
        type="file" 
        class="form-control" 
        ref="studentsPictureRef"
        accept="image/*"
        @change="studentsAddPictureChange"
      />
    </div>

    <div v-if="studentAddImageUrl" class="col-auto mb-3">
        <img :src="studentAddImageUrl" style="max-height: 60px;" alt="Превью">
      </div>

        <form @submit.prevent.stop="onStudentAdd" class="mt-3 mb-4">
      <div class="row">
        <div class="col">
          <div class="form-floating">
            <input
              type="text"
              class="form-control"
              v-model="studentToAdd.name"
              placeholder="ФИО"
              required
            />
            <label>ФИО</label>
          </div>
        </div>
        <div class="col">
          <div class="form-floating">
            <input
              type="text"
              class="form-control"
              v-model="studentToAdd.login"
              placeholder="Логин"
              required
            />
            <label>Логин</label>
          </div>
        </div>
        <div class="col">
          <div class="form-floating">
            <input
              type="password"
              class="form-control"
              v-model="studentToAdd.password"
              placeholder="Пароль"
              required
            />
            <label>Пароль</label>
          </div>
        </div>
        <div class="col">
          <div class="form-floating">
            <select class="form-select" v-model="studentToAdd.level" required>
              <option value="">Выберите уровень</option>
              <option value="Начальный">Начальный</option>
              <option value="Средний">Средний</option>
              <option value="Продвинутый">Продвинутый</option>
            </select>
            <label>Уровень</label>
          </div>
        </div>
        <div class="col-auto">
          <button class="btn btn-primary">
            Добавить
          </button>
        </div>
      </div>
    </form>
    
    <button @click="onLoadClick" class="btn btn-secondary mb-3">Загрузить</button>

        <div v-for="item in students" :key="item.id" class="student-item">
        <div v-if="item.picture">
            <img 
                :src="item.picture" 
                style="max-height: 60px; cursor: pointer;"
                @click="onImageClick(item.picture)" 
                alt="Фото студента"
            >
        </div>
        
        <div>{{ item.name }}</div>
        <div>Уровень: {{ item.level }}</div>
        <div>Прогресс: {{ item.progress }}%</div>
        
        <button
          class="btn btn-success"
          @click="onStudentEditClick(item)"
          data-bs-toggle="modal"
          data-bs-target="#editStudentModal"
        >
          <i class="bi bi-pen-fill"></i>Редактировать
        </button>
        <button class="btn btn-danger" @click="onRemoveClick(item)">
          <i class="bi bi-x"></i>Удалить
        </button>
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

        <div class="modal fade" id="editStudentModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать студента</h1>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <div class="row g-3">
              
                            <div class="col-12">
                <label class="form-label">Изменить фото (оставьте пустым, чтобы не менять)</label>
                <input 
                    type="file" 
                    class="form-control" 
                    ref="studentEditPictureRef" 
                    accept="image/*"
                    @change="studentEditPictureChange"
                />
              </div>
              <div v-if="studentEditImageUrl" class="col-12">
                  <img :src="studentEditImageUrl" style="max-height: 100px;" alt="Превью нового фото">
              </div>
              <div v-else-if="studentToEdit.picture" class="col-12">
                  <small class="text-muted">Текущее фото:</small>
                  <img :src="studentToEdit.picture" style="max-height: 60px;" alt="Текущее фото">
              </div>
              
                            <div class="col-12">
                <div class="form-floating">
                  <input
                    type="text"
                    class="form-control"
                    v-model="studentToEdit.name"
                    placeholder="ФИО"
                  />
                  <label>ФИО</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating">
                  <input
                    type="text"
                    class="form-control"
                    v-model="studentToEdit.login"
                    placeholder="Логин"
                  />
                  <label>Логин</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating">
                  <input
                    type="password"
                    class="form-control"
                    v-model="studentToEdit.password"
                    placeholder="Пароль"
                  />
                  <label>Пароль</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating">
                  <select class="form-select" v-model="studentToEdit.level">
                    <option value="Начальный">Начальный</option>
                    <option value="Средний">Средний</option>
                    <option value="Продвинутый">Продвинутый</option>
                  </select>
                  <label>Уровень</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating">
                  <input
                    type="number"
                    class="form-control"
                    v-model="studentToEdit.progress"
                    placeholder="Прогресс"
                    min="0"
                    max="100"
                  />
                  <label>Прогресс (%)</label>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Закрыть
            </button>
            <button
              data-bs-dismiss="modal"
              type="button"
              class="btn btn-primary"
              @click="onUpdateStudent"
            >
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.student-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border-bottom: 1px solid #eee;
}
</style>