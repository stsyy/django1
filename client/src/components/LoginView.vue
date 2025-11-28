<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header">
            <h3 class="text-center">Авторизация в МедЦентре</h3>
          </div>
          <div class="card-body">
            <form @submit.prevent="handleLogin">
              <div class="mb-3">
                <label for="username" class="form-label">Имя пользователя</label>
                <input
                  type="text"
                  class="form-control"
                  id="username"
                  v-model="username"
                  placeholder="Введите имя пользователя"
                  required
                >
              </div>
              
              <div class="mb-3">
                <label for="password" class="form-label">Пароль</label>
                <input
                  type="password"
                  class="form-control"
                  id="password"
                  v-model="password"
                  placeholder="Введите пароль"
                  required
                >
              </div>
              
              <button type="submit" class="btn btn-primary w-100" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                {{ loading ? 'Вход...' : 'Войти' }}
              </button>
              
              <div v-if="errorMessage" class="alert alert-danger mt-3">
                {{ errorMessage }}
              </div>

              <div class="mt-3 text-center">
                <small class="text-muted">
                  
                </small>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user_store'

const router = useRouter()
const userStore = useUserStore()

const username = ref('')
const password = ref('')
const errorMessage = ref('')
const loading = ref(false)

async function handleLogin() {
  loading.value = true
  errorMessage.value = ''

  try {
    const result = await userStore.login(username.value, password.value)
    
    if (result && result.success) {
      router.push('/')
    } else {
      errorMessage.value = result?.error || 'Ошибка авторизации. Проверьте логин и пароль.'
    }
  } catch (error) {
    console.error('Login error:', error)
    errorMessage.value = 'Произошла ошибка при входе в систему'
  } finally {
    loading.value = false
  }
}

// Если пользователь уже авторизован, перенаправляем на главную
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'

const { userInfo } = storeToRefs(userStore)

onMounted(() => {
  if (userInfo.value.is_authenticated) {
    router.push('/')
  }
})
</script>

<style scoped>
.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  border: 1px solid rgba(0, 0, 0, 0.125);
}
</style>