import { createI18n } from 'vue-i18n'
import { createApp } from 'vue'

import { messages } from './strings'
import ShoppingApp from './apps/ShoppingApp.vue'

import { library } from '@fortawesome/fontawesome-svg-core'
import {
  faCopy,
  faRoute,
  faPizzaSlice,
  faUsers,
  faTerminal,
  faInfo,
  faSignOutAlt,
  faPlus,
  faCalendarDay,
  faWalking,
  faPen,
  faShareAlt,
  faArchive,
  faPrint,
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
  faTerminal,
  faInfo,
  faSignOutAlt,
  faPlus,
  faCalendarDay,
  faWalking,
  faPen,
  faShareAlt,
  faPrint
)

const pinia = createPinia()

const i18n = createI18n({
  legacy: false,
  locale: 'ru',
  fallbackLocale: 'en',
  messages,
})

const app = createApp(ShoppingApp)
app.use(pinia)
app.use(i18n)
app.component('font-awesome-icon', FontAwesomeIcon)
app.mount('#shopping-app')

useUserStore().fetchUserData()
