import { createI18n } from 'vue-i18n'
import { createApp } from 'vue'

import { library } from '@fortawesome/fontawesome-svg-core'
import {
  faClipboardQuestion,
  faInfo,
  faPen,
  faPizzaSlice,
  faPlus,
  faRoute,
  faSignOutAlt,
  faTrash,
  faUsers,
  faToolbox,
} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { createPinia } from 'pinia'
import { useUserStore } from './stores/user'
import { createWebHistory, createRouter } from 'vue-router'

import ruMessages from './locales/ru.json'
import enMessages from './locales/en.json'
import AdminApp from './apps/AdminApp.vue'
import UsersApp from './apps/UsersApp.vue'
import MaintenanceApp from './apps/MaintenanceApp.vue'

library.add(
  faPlus,
  faTrash,
  faPen,
  faRoute,
  faPizzaSlice,
  faUsers,
  faInfo,
  faClipboardQuestion,
  faSignOutAlt,
  faToolbox
)

const pinia = createPinia()

const i18n = createI18n<[typeof ruMessages], 'ru' | 'en'>({
  legacy: false,
  locale: 'ru',
  fallbackLocale: 'en',
  messages: {
    ru: ruMessages,
    en: enMessages,
  },
})

const router = createRouter({
  history: createWebHistory('/admin'),
  routes: [
    {
      path: '/',
      redirect: '/users/',
    },
    {
      path: '/users/',
      component: UsersApp,
    },
    {
      path: '/maintenance/',
      component: MaintenanceApp,
    },
  ],
})

const app = createApp(AdminApp)
app.use(pinia)
app.use(i18n)
app.use(router)
app.component('FontAwesomeIcon', FontAwesomeIcon)
app.mount('#app')

useUserStore().fetchUserData()
