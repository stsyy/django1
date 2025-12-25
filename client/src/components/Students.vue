<script setup>
import { onBeforeMount, ref } from 'vue';
import axios from "axios";
import Cookies from "js-cookie";
import * as bootstrap from 'bootstrap';
import { useUserInfoStore } from '@/stores/user_store';
const students = ref([]);
const studentToAdd = ref({});
const studentToEdit = ref({});
const studentsPictureRef = ref();
const studentAddImageUrl = ref();
const tests = ref([]);
const loading = ref(false);
const tutors = ref([]);
const selectedTutor = ref({});
const studentEditPictureRef = ref(); 
const studentEditImageUrl = ref(); 
const selectedImageUrl = ref(null); 
const userStore = useUserInfoStore();
const selectedTests = ref({});
const stats = ref({});
async function fetchStudents(){
  loading.value=true;
  const r = await axios.get("/api/students");
  console.log(r.data)
  students.value = r.data;
  loading.value=false;
}
async function fetchTutors() {
  const r = await axios.get("/api/users/tutors/");
  tutors.value = r.data;
}
async function onRemoveClick(student) {
  await axios.delete(`/api/students/${student.id}/`);
  await fetchStudents();
}
async function fetchTests() {
  const r = await axios.get("/api/tests/"); 
  tests.value = r.data;
}
function hasSecondFactor() {
  return userStore.second && userStore.second.active;
}

async function fetchStats() {
  await userStore.fetchUserInfo();
  if (!hasSecondFactor()) {
    alert('Для просмотра статистики требуется двухфакторная аутентификация!');
    return;
  }
  const response = await axios.get('/api/students/stats/', {
    withCredentials: true
  });
  
  stats.value = response.data;
}

//async function onLoadClick(){
  //await fetchStudents()
//}

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
async function assignTutor(studentId) {
  const tutorId = selectedTutor.value[studentId];
  if (!tutorId) return alert("Выберите преподавателя");

  await axios.post(`/api/students/${studentId}/assign-tutor/`, { tutor_id: tutorId });
  await fetchStudents();
  alert("Преподаватель назначен");
}
async function assignTests(studentId) {
  const testIds = selectedTests.value[studentId] || [];
  await axios.post(`/api/students/${studentId}/assign-tests/`, {assigned_tests: testIds});
  await fetchStudents();
  alert("Тесты назначены");
}
async function onStudentAdd() {
  const formData = new FormData();
  formData.append('picture', studentsPictureRef.value.files[0]);
  formData.set('name', studentToAdd.value.name);
  formData.append('login', studentToAdd.value.login || "");
  formData.append('password', studentToAdd.value.password || "");
  formData.append('level', studentToAdd.value.level || "");
  formData.append('progress', studentToAdd.value.progress || 0);
  await axios.post("/api/students/", formData, {
    headers:{
      'Content-Type': 'multipart/form-data'
    }

  });
  await fetchStudents(); // переподтягиваю
  studentToAdd.value={};

}

async function showStsts() {
  
}

/*async function onStudentAdd() {
  const formData = new FormData();
  const file = studentsPictureRef.value?.files?.[0];

  if (file) formData.append('picture', file);
  formData.append('name', studentToAdd.value.name || "");
  formData.append('login', studentToAdd.value.login || "");
  formData.append('password', studentToAdd.value.password || "");
  formData.append('level', studentToAdd.value.level || "");
  formData.append('progress', studentToAdd.value.progress || 0);

  await axios.post("/api/students/create-custom/", formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });

  studentToAdd.value = {};
  studentAddImageUrl.value = null;
  studentsPictureRef.value.value = ""; 
  await fetchStudents();
}*/

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

async function exportStudents() {
  const response = await axios.get(
    '/api/students/export/',
    {
      responseType: 'blob'
    }
  )

  const blob = new Blob(
    [response.data],
    { type: response.headers['content-type'] }
  )

  const url = window.URL.createObjectURL(blob)

  const link = document.createElement('a')
  link.href = url
  link.download = 'students.xlsx'
  link.click()

  window.URL.revokeObjectURL(url)
}

onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
  await userStore.fetchUserInfo();
  await fetchStudents(); 
  await fetchTutors();
  await fetchTests();
  if (hasSecondFactor()) {
    await fetchStats();
  }
  
})
</script>

<template>
  <div class="container mt-4">
    <h2>Студенты</h2>
    
    <div v-if="loading" class="text-center">Загрузка...</div>

    <div>
      <button 
        @click="fetchStats" 
        :disabled="!hasSecondFactor"
        class="btn btn-primary mb-3"
      >
        {{ hasSecondFactor() ? 'Показать статистику' : 'Требуется двухфакторная аутентификация' }}
      </button>
      <div v-if="stats && hasSecondFactor">
        <h3>Статистика студентов:</h3>
        <p>Количество: {{ stats.count }}</p>
        <p>Средний прогресс: {{ stats.avg }}</p>
        <p>Максимальный прогресс: {{ stats.max }}</p>
        <p>Минимальный прогресс: {{ stats.min }}</p>
      </div>
    </div>
    <button class="btn btn-outline-success mb-3" @click="exportStudents">
      Экспорт в Excel
    </button>
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

    <form @submit.prevent.stop="onStudentAdd" class="mb-4">
      <div class="row g-2 align-items-end">
        <div class="col">
          <div class="form-floating">
            <input type="text" class="form-control" v-model="studentToAdd.name" placeholder="ФИО" required />
            <label>ФИО</label>
          </div>
        </div>
        <div class="col">
          <div class="form-floating">
            <input type="text" class="form-control" v-model="studentToAdd.login" placeholder="Логин" required />
            <label>Логин</label>
          </div>
        </div>
        <div class="col">
          <div class="form-floating">
            <input type="password" class="form-control" v-model="studentToAdd.password" placeholder="Пароль" required />
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
          <button class="btn btn-primary">Добавить</button>
        </div>
      </div>
    </form>

    <div v-for="item in students" :key="item.id" class="student-item d-flex align-items-center justify-content-between flex-wrap mb-3 p-2 border rounded">
      <div class="d-flex align-items-center gap-3 flex-wrap">
        <img v-if="item.picture" :src="item.picture" style="max-height: 60px; cursor: pointer;" @click="onImageClick(item.picture)" alt="Фото студента">
        <div>
          <div><strong>{{ item.name }}</strong></div>
          <div>Уровень: {{ item.level }}</div>
          <div>Прогресс: {{ item.progress }}%</div>
        </div>
      </div>

      <div class="d-flex gap-2 flex-wrap align-items-center">
        <div>
          <select v-model="selectedTutor[item.id]" class="form-select form-select-sm">
            <option value="">Выберите преподавателя</option>
            <option v-for="tutor in tutors" :key="tutor.id" :value="tutor.id">{{ tutor.name }}</option>
          </select>
          <button class="btn btn-sm btn-primary mt-1 w-100" @click="assignTutor(item.id)">Назначить тьютора</button>
          <div>Тьютор: {{ item.tutor_name || "Не назначен" }}</div>
        </div>

        <div>
          <label>Назначить тесты</label>
          <select v-model="selectedTests[item.id]" class="form-select form-select-sm" multiple>
            <option v-for="test in tests" :key="test.id" :value="test.id">{{ test.name }}</option>
          </select>
          <button class="btn btn-sm btn-primary mt-1 w-100" @click="assignTests(item.id)">Сохранить тесты</button>
          <div>
            Назначенные тесты: 
            <span v-if="item.assigned_tests_info && item.assigned_tests_info.length">
              {{ item.assigned_tests_info.map(t => t.name).join(', ') }}
            </span>
            <span v-else>Нет</span>
          </div>
        </div>

        <div class="d-flex flex-column gap-1">
          <button class="btn btn-success btn-sm" @click="onStudentEditClick(item)" data-bs-toggle="modal" data-bs-target="#editStudentModal">
            <i class="bi bi-pen-fill"></i> Редактировать
          </button>
          <button class="btn btn-danger btn-sm" @click="onRemoveClick(item)">
            <i class="bi bi-x"></i> Удалить
          </button>
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

    <div class="modal fade" id="editStudentModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Редактировать студента</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="row g-3">
              <div class="col-12 col-md-3">
                <label class="form-label">Фото</label>
                <input type="file" class="form-control" ref="studentEditPictureRef" accept="image/*" @change="studentEditPictureChange" />
                <div v-if="studentEditImageUrl" class="mt-2">
                  <img :src="studentEditImageUrl" style="max-height: 100px;" alt="Превью">
                </div>
                <div v-else-if="studentToEdit.picture" class="mt-2">
                  <small class="text-muted">Текущее фото:</small>
                  <img :src="studentToEdit.picture" style="max-height: 60px;" alt="Текущее фото">
                </div>
              </div>

              <div class="col-12 col-md-9 d-flex flex-column gap-2">
                <div class="form-floating">
                  <input type="text" class="form-control" v-model="studentToEdit.name" placeholder="ФИО" />
                  <label>ФИО</label>
                </div>
                <div class="form-floating">
                  <input type="text" class="form-control" v-model="studentToEdit.login" placeholder="Логин" />
                  <label>Логин</label>
                </div>
                <div class="form-floating">
                  <input type="password" class="form-control" v-model="studentToEdit.password" placeholder="Пароль" />
                  <label>Пароль</label>
                </div>
                <div class="form-floating">
                  <select class="form-select" v-model="studentToEdit.level">
                    <option value="Начальный">Начальный</option>
                    <option value="Средний">Средний</option>
                    <option value="Продвинутый">Продвинутый</option>
                  </select>
                  <label>Уровень</label>
                </div>
                <div class="form-floating">
                  <input type="number" class="form-control" v-model="studentToEdit.progress" placeholder="Прогресс" min="0" max="100" />
                  <label>Прогресс (%)</label>
                </div>

                <label class="mt-2">Назначенные тесты</label>
                <select v-model="selectedTests[studentToEdit.id]" class="form-select" multiple>
                  <option v-for="test in tests" :key="test.id" :value="test.id">{{ test.name }}</option>
                </select>
                <button class="btn btn-sm btn-primary mt-1" @click="assignTests(studentToEdit.id)">Сохранить тесты</button>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
            <button type="button" class="btn btn-primary" @click="onUpdateStudent" data-bs-dismiss="modal">Сохранить</button>
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
  justify-content: space-between;
  gap: 15px;
  padding: 10px;
  border: 1px solid #eee;
  border-radius: 8px;
  flex-wrap: wrap;
}
</style>
