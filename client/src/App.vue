<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <router-link to="/" class="navbar-brand">Система тестирования</router-link>

        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNavDropdown"
          aria-controls="navbarNavDropdown"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse justify-content-between" id="navbarNavDropdown">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link to="/students" class="nav-link">Студенты</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/tests" class="nav-link">Тесты</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/test-questions" class="nav-link">Вопросы</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/results" class="nav-link">Результаты</router-link>
            </li>
          </ul>

      <ul class="navbar-nav">
                <li class="nav-item dropdown">
                    <a
                        class="nav-link dropdown-toggle"
                        href="#"
                        role="button"
                        data-bs-toggle="dropdown"
                        aria-expanded="false"
                    >
                        Пользователь
                    </a>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="http://127.0.0.1:8000/admin/" target="_blank">Админка</a></li> 
                        <li><hr class="dropdown-divider"></li>
                        <li><a class="dropdown-item" href="#" @click.prevent="logoutUser">Выйти</a></li> 
                        </ul>
                </li>
            </ul>
        </div>
      </div>
    </nav>

    <div class="container mt-4">
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios';
import { useRouter } from 'vue-router'; // Импортируем роутер для навигации

const router = useRouter(); // Получаем экземпляр роутера

const logoutUser = async () => {
    try {
        // Делаем POST-запрос к твоему Django-эндпоинту.
        // URL должен быть полным, если ты используешь Vite dev server.
        await axios.post('http://127.0.0.1:8000/api/logout/'); 
        
        // Оповещаем пользователя и перенаправляем на главную страницу (или страницу входа)
        console.log('Выход успешен.');
        // router.push('/') перенаправит на /students, согласно твоему роутингу.
        // Если хочешь совсем сбросить страницу, можно просто перезагрузить
        window.location.reload(); 
        
    } catch (error) {
        console.error('Ошибка при выходе:', error);
        // Если это ошибка 401 (Unauthorized), возможно, сессия уже истекла.
        // В любом случае, перенаправляем для сброса состояния.
        window.location.reload(); 
    }
};
</script>

<style>

body {
  background-color: #f8f9fa;
}
</style>
