import { createI18n } from 'vue-i18n'
import { createApp } from 'vue'

import ruMessages from './locales/ru.json'
import enMessages from './locales/en.json'
import UsersApp from './apps/UsersApp.vue'

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
} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { createPinia } from 'pinia'
import { useUserStore } from './stores/user'

library.add(
  faPlus,
  faTrash,
  faPen,
  faRoute,
  faPizzaSlice,
  faUsers,
  faInfo,
  faClipboardQuestion,
  faSignOutAlt
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

const app = createApp(UsersApp)
app.use(pinia)
app.use(i18n)
app.component('FontAwesomeIcon', FontAwesomeIcon)
app.mount('#app')

useUserStore().fetchUserData()
