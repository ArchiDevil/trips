import { createI18n } from 'vue-i18n'
import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'

import ruMessages from './locales/ru.json'
import enMessages from './locales/en.json'
import TripApp from './apps/TripApp.vue'

import { library } from '@fortawesome/fontawesome-svg-core'
import {
  faCopy,
  faRoute,
  faPizzaSlice,
  faUsers,
  faInfo,
  faSignOutAlt,
  faPlus,
  faCalendarDay,
  faWalking,
  faPen,
  faShareAlt,
  faArchive,
  faTrash,
  faEraser,
  faEllipsisV,
  faCompressAlt,
  faExpandAlt,
  faShoppingCart,
  faHiking,
  faAngleDoubleRight,
  faTable,
  faSpinner,
  faCookieBite,
  faCubes,
  faPrint,
  faCarrot,
  faFish,
  faCandyCane,
  faClipboardQuestion,
} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { createPinia } from 'pinia'
import { useUserStore } from './stores/user'

library.add(
  faArchive,
  faCopy,
  faRoute,
  faPizzaSlice,
  faUsers,
  faInfo,
  faSignOutAlt,
  faPlus,
  faCalendarDay,
  faWalking,
  faPen,
  faShareAlt,
  faTrash,
  faEraser,
  faEllipsisV,
  faCompressAlt,
  faExpandAlt,
  faShoppingCart,
  faHiking,
  faAngleDoubleRight,
  faTable,
  faSpinner,
  faCookieBite,
  faCubes,
  faClipboardQuestion,
  faPrint,
  faCarrot,
  faFish,
  faCandyCane
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

const MealsApp = () => import('./apps/MealsApp.vue')
const ShoppingApp = () => import('./apps/ShoppingApp.vue')
const PackingApp = () => import('./apps/PackingApp.vue')

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/meals/:uid',
      component: MealsApp,
    },
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

const app = createApp(TripApp)
app.use(pinia)
app.use(i18n)
app.use(router)
app.component('FontAwesomeIcon', FontAwesomeIcon)
app.mount('#trip-app')

useUserStore().fetchUserData()
