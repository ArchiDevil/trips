import { createI18n } from 'vue-i18n'
import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'

import { messages } from './strings'
import ShoppingApp from './apps/ShoppingApp.vue'
import PackingApp from './apps/PackingApp.vue'

import { library } from '@fortawesome/fontawesome-svg-core'
import {
  faRoute,
  faPizzaSlice,
  faUsers,
  faInfo,
  faSignOutAlt,
  faPrint,
} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { createPinia } from 'pinia'
import { useUserStore } from './stores/user'
import ReportsApp from './apps/ReportsApp.vue'

library.add(faRoute, faPizzaSlice, faUsers, faInfo, faSignOutAlt, faPrint)

const pinia = createPinia()

const i18n = createI18n({
  legacy: false,
  locale: 'ru',
  fallbackLocale: 'en',
  messages,
})

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/reports/shopping/:uid',
      component: ShoppingApp,
    },
    {
      path: '/reports/packing/:uid',
      component: PackingApp,
    },
  ],
})

const app = createApp(ReportsApp)
app.use(pinia)
app.use(i18n)
app.use(router)
app.component('font-awesome-icon', FontAwesomeIcon)
app.mount('#reports-app')

useUserStore().fetchUserData()