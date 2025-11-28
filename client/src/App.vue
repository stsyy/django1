// App.vue 

<script setup>
import {ref} from "vue";
import {useRouter} from "vue-router";
// Путь '@/stores/user_store' предполагаем правильным
import {useUserStore} from '@/stores/user_store'; 
import {storeToRefs} from "pinia";
import axios from 'axios'; 

// --- Логика Pinia Store и формы ---
const username = ref('');
const password = ref('');

const router = useRouter()
const userStore = useUserStore()
const { userInfo } = storeToRefs(userStore) 

async function onFormSend() {
    await userStore.login(username.value, password.value)
    username.value = '';
    password.value = '';
}

// --- Логика Logout ---
const logoutUser = async () => {
    try {
        // ✅ ИСПРАВЛЕНИЕ: Добавлен withCredentials: true для корректного сброса сессии
        await axios.post('http://127.0.0.1:8000/api/logout/', {}, {
             withCredentials: true 
        }); 
        
        // После выхода обновляем состояние
        await userStore.checkLogin(); 
        // window.location.reload(); // Эту строку можно убрать, если checkLogin корректно обновит UI

    } catch (error) {
        console.error('Ошибка при выходе:', error);
        // Если что-то пошло не так, все равно сбрасываем состояние
        await userStore.checkLogin(); 
        // window.location.reload();
    }
};
</script>