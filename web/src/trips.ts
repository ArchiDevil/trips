import { createI18n } from 'vue-i18n'
import { createApp } from 'vue'

import ruMessages from './locales/ru.json'
import enMessages from './locales/en.json'
import TripsApp from './apps/TripsApp.vue'

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
  faEyeSlash,
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
  faEyeSlash,
  faClipboardQuestion
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

const app = createApp(TripsApp)
app.use(pinia)
app.use(i18n)
app.component('FontAwesomeIcon', FontAwesomeIcon)
app.mount('#trips-app')

useUserStore().fetchUserData()
