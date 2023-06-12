import { createI18n } from 'vue-i18n'
import { createApp } from 'vue'

import { messages } from './strings'
import ProductsApp from './apps/ProductsApp.vue'

import { library } from '@fortawesome/fontawesome-svg-core'
import {
  faRoute,
  faPizzaSlice,
  faUsers,
  faTerminal,
  faInfo,
  faSignOutAlt,
  faPlus,
  faSearch,
  faPen,
  faArchive,
  faArrowLeft,
  faArrowRight,
} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(
  faRoute,
  faPizzaSlice,
  faUsers,
  faTerminal,
  faInfo,
  faSignOutAlt,
  faPlus,
  faSearch,
  faPen,
  faArchive,
  faArrowLeft,
  faArrowRight
)

const i18n = createI18n({
  locale: 'ru',
  fallbackLocale: 'en',
  messages,
})

const productsApp = createApp(ProductsApp)
productsApp.use(i18n)
productsApp.component('font-awesome-icon', FontAwesomeIcon)
productsApp.mount('#products-app')
