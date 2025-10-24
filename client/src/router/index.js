import { createRouter, createWebHistory } from 'vue-router'
import Students from '../components/Students.vue'
import Tests from '../components/Tests.vue'
import TestQuestions from '../components/TestQuestions.vue'
import Results from '../components/Results.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
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
      redirect: '/students'
    }
  ],
})

export default router