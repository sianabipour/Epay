import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import FactorView from '../views/FactorView.vue'
import FactorsView from '../views/FactorsView.vue'
import DoneView from '../views/DoneView.vue'
import FactorEditView from '../views/FactorEditView.vue'
import BankData from '../views/BankData.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/factor/:id', name: 'factor', component: FactorView },
  { path: '/factor/edit/:id', name: 'factor_edit', component: FactorEditView },
  { path: '/factors', name: 'factors', component: FactorsView },
  { path: '/done/:id', name: 'done', component: DoneView },
  { path: '/bank-data', name: 'bank_data', component: BankData }
]

const router = createRouter({
  scrollBehavior (to, from, savedPosition) {
    return { top: 0 }
  },
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
