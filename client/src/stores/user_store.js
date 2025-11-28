// src/store/user_store.ts

import {defineStore} from "pinia";
import {onBeforeMount, ref} from "vue";
import axios from "axios";

// Определяем Store с именем "userStore"
export const useUserStore = defineStore("userStore", () => {
    
    // Состояние, хранящее информацию о пользователе
    const userInfo = ref({
        is_authenticated: false,
        username: 'Гость',
        is_superuser: false,
        // Здесь будут храниться все данные из /api/user/
    })

    // Функция для проверки текущего статуса авторизации
    async function checkLogin() {
        try {
            // ✅ ИСПРАВЛЕНИЕ: Добавлен withCredentials: true
            let r = await axios.get("http://127.0.0.1:8000/api/user/status", { 
                withCredentials: true 
            })
            userInfo.value = r.data;
        } catch (error) {
            // Если запрос провалился (например, CORS или нет ответа), 
            // сбрасываем состояние на анонима
            console.error("Ошибка при проверке статуса авторизации:", error);
            userInfo.value = {
                is_authenticated: false,
                username: 'Гость',
                is_superuser: false,
            };
        }
    }


    // Функция для входа в систему
    async function login(username, password) {
        try {
            // ✅ POST-запрос к эндпоинту, который мы создали
        await axios.post("http://127.0.0.1:8000/api/login/", {
                username: username,
                password: password,
            }, { withCredentials: true })
            // Если вход успешен, обновляем данные пользователя
            await checkLogin();
        } catch (error) {
            console.error("Ошибка входа:", error);
            alert("Неверный логин или пароль.");
        }
    }

    // Вызываем checkLogin перед монтированием приложения, чтобы сразу проверить сессию
    onBeforeMount(async () => {
        await checkLogin();
    })

    // Возвращаем состояние и методы для использования в компонентах
    return {
        userInfo,
        checkLogin,
        login,
    }
})