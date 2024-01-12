import { createI18n } from 'vue-i18n'
import { createApp } from 'vue'

import { messages } from './strings'
import MealsApp from './apps/MealsApp.vue'

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
  faCubes
)

const pinia = createPinia()

const i18n = createI18n({
  legacy: false,
  locale: 'ru',
  fallbackLocale: 'en',
  messages,
})

const app = createApp(MealsApp)
app.use(pinia)
app.use(i18n)
app.component('font-awesome-icon', FontAwesomeIcon)
app.mount('#meals-app')

useUserStore().fetchUserData()
