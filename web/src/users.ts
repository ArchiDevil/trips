import { createI18n } from 'vue-i18n'
import { createApp } from 'vue'

import { messages } from './strings'
import UsersApp from './apps/UsersApp.vue'

import { library } from '@fortawesome/fontawesome-svg-core'
import {
  faCheck,
  faClipboardQuestion,
  faInfo,
  faPen,
  faPizzaSlice,
  faPlus,
  faRoute,
  faSignOutAlt,
  faTimes,
  faTrash,
  faUsers,
} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { createPinia } from 'pinia'
import { useUserStore } from './stores/user'

library.add(
  faPlus,
  faCheck,
  faTimes,
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

const i18n = createI18n<[typeof messages.ru], 'ru' | 'en'>({
  legacy: false,
  locale: 'ru',
  fallbackLocale: 'en',
  messages: {
    ru: messages.ru,
    en: messages.en,
  },
})

const app = createApp(UsersApp)
app.use(pinia)
app.use(i18n)
app.component('font-awesome-icon', FontAwesomeIcon)
app.mount('#app')

useUserStore().fetchUserData()
