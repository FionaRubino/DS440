import { createRouter, createWebHistory } from 'vue-router'
import LandingView from '../views/LandingView.vue'
import ModelPage from '../views/ModelPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: LandingView,
    },
    {
      path: '/model',          // <-- new route URL
      name: 'model',
      component: ModelPage,    // <-- now this import is used
    }
  ],
})

export default router
