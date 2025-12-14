import { createRouter, createWebHashHistory, createWebHistory } from 'vue-router'

import Students from '@/components/Students.vue';
import Tests from '@/components/Tests.vue';
import TestQuestions from '@/components/TestQuestions.vue';
import Results from '@/components/Results.vue';
import AdminView from '@/components/AdminView.vue'; 
import Tutor from '@/components/Tutor.vue'; 

import LoginView from '@/components/LoginView.vue';
import { useUserInfoStore } from '@/stores/user_store';

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView 
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminView 
    },
    {
      path: '/tutor',
      name: 'tutor',
      component: Tutor
    },
    {
      path: '/students',
      name: 'Students',
      component: Students
    },
    {
      path: '/tests',
      name: 'Tests', 
      component: Tests
    },
    {
      path: '/test-questions',
      name: 'TestQuestions',
      component: TestQuestions
    },
    {
      path: '/results',
      name: 'Results',
      component: Results
    },
    {
      path: '/',
      name: 'home',
      component: Students
    }
  ],
})

router.beforeEach((to, from) => {
  const userInfoStore = useUserInfoStore();
  if (userInfoStore.is_authenticated == false && to.name != 'Login') {
      return { name: 'Login' }
  }
})


export default router