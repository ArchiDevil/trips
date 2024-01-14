import { createI18n } from 'vue-i18n'
import { createApp } from 'vue'

import { messages } from './strings'
import ProductsApp from './apps/ProductsApp.vue'

import { library } from '@fortawesome/fontawesome-svg-core'
import {
  faRoute,
  faPizzaSlice,
  faUsers,
  faInfo,
  faSignOutAlt,
  faPlus,
  faSearch,
  faPen,
  faArchive,
  faArrowLeft,
  faArrowRight,
  faClipboardQuestion,
} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { createPinia } from 'pinia'
import { useUserStore } from './stores/user'

library.add(
  faRoute,
  faPizzaSlice,
  faUsers,
  faInfo,
  faSignOutAlt,
  faPlus,
  faSearch,
  faPen,
  faArchive,
  faArrowLeft,
  faArrowRight,
  faClipboardQuestion
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

const app = createApp(ProductsApp)
app.use(pinia)
app.use(i18n)
app.component('font-awesome-icon', FontAwesomeIcon)
app.mount('#products-app')

useUserStore().fetchUserData()
