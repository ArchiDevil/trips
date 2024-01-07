import { createI18n } from 'vue-i18n'
import { createApp } from 'vue'

import { messages } from './strings'
import TripsApp from './apps/TripsApp.vue'

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
  faShareAlt
)

const pinia = createPinia()

const i18n = createI18n({
  legacy: false,
  locale: 'ru',
  fallbackLocale: 'en',
  messages,
})

const tripsApp = createApp(TripsApp)
tripsApp.use(pinia)
tripsApp.use(i18n)
tripsApp.component('font-awesome-icon', FontAwesomeIcon)
tripsApp.mount('#trips-app')

useUserStore().fetchUserData()
